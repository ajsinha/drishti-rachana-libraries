#!/usr/bin/env python3
# Copyright (c) 2026 Ashutosh Sinha <ajsinha@gmail.com>. All rights reserved.
# Drishti Rachana Libraries. Proprietary: see the LICENSE file at the root of this repository.
"""Builds, tests, signs, packs and verifies the libraries of this repository with the Rachana command line.

    python3 tools/build.py [--update-goldens] [--release] [--rachana-java DIR] [LIBRARY ...]

Steps, for each library under libraries/ (all of them when none is named):

  1. docs     writes libraries/<name>/README.md from the fragment files (the library's front page)
  2. build    rachana lib build: regenerates `exports` in the manifest and MANIFEST.sha384
  3. test     tools/LibCheck.java: every example compiles at language level 1.2 with no problem and no advisory, and its
              ViewModel equals the golden snapshot (--update-goldens rewrites the goldens, then builds again)
  4. sign     rachana lib sign, with the development key (keys/dev.key, created on first use, never committed);
              --release signs with the owner's release key instead: RACHANA_RELEASE_PUBLIC and RACHANA_RELEASE_SEED
  5. pack     rachana lib pack: dist/<name>-<version>.rlib, deterministic, signature required
  6. verify   rachana lib verify of the archive, signed by the key above

The Rachana jars are read from rachana-jars/ (RACHANA_JARS overrides). --rachana-java DIR copies them there from a Rachana
build (DIR is the `java` folder of drishti-rachana after `./mvnw clean package -DskipTests`; nothing is installed).
Java 21 or later: JAVA_HOME, else `java` on the PATH. Exit status 0 when every step passed.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = ("# Copyright (c) 2026 Ashutosh Sinha <ajsinha@gmail.com>. All rights reserved.\n"
          "# Drishti Rachana Libraries. Proprietary: see the LICENSE file at the root of this repository.\n")


def java():
    home = os.environ.get("JAVA_HOME")
    return str(Path(home) / "bin" / "java") if home else (shutil.which("java") or "java")


def jars_dir():
    return Path(os.environ.get("RACHANA_JARS", ROOT / "rachana-jars"))


def copy_jars(src):
    dest = jars_dir()
    dest.mkdir(parents=True, exist_ok=True)
    for module in ("rachana-api", "rachana-core", "rachana-tools", "rachana-cli"):
        found = [j for j in (Path(src) / module / "target").glob("*.jar")
                 if not j.name.endswith(("-sources.jar", "-tests.jar", "-javadoc.jar"))]
        if not found:
            sys.exit(f"no jar of {module} under {src}: build Rachana first (./mvnw clean package -DskipTests)")
        for j in found:
            shutil.copy(j, dest / j.name)


def run(args, **kw):
    return subprocess.run(args, text=True, capture_output=True, **kw)


def cli(*args):
    r = run([java(), "-cp", str(jars_dir() / "*"), "com.ash.rachana.cli.Main", "lib", *args])
    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0:
        print(f"  FAIL rachana lib {' '.join(args)}\n{out}")
        return None
    return out


def dev_key():
    """The development key pair (public, private seed); created on first use under keys/ (git-ignored)."""
    f = ROOT / "keys" / "dev.key"
    if not f.exists():
        out = cli("keygen")
        if out is None:
            return None
        pub = re.search(r"public\s+(\S+)", out).group(1)
        seed = re.search(r"private\s+(\S+)", out).group(1)
        f.parent.mkdir(exist_ok=True)
        f.write_text(f"public {pub}\nprivate {seed}\n")
        f.chmod(0o600)
    t = f.read_text()
    return re.search(r"public (\S+)", t).group(1), re.search(r"private (\S+)", t).group(1)


def read_front(text):
    """The fragment file as a dict, without a YAML library: the keys the front page needs."""
    import yaml  # PyYAML: only the docs step needs it
    return yaml.safe_load(text)


def write_readme(lib):
    manifest = next(lib.glob("*.rachana-lib.yaml")).read_text()
    title = re.search(r"^title: (.+)$", manifest, re.M).group(1)
    summary = re.search(r"^summary: (.+)$", manifest, re.M).group(1)
    version = re.search(r"^version: (.+)$", manifest, re.M).group(1)
    cats = dict(re.findall(r"\{ id: (\S+?),\s+title: (.+?) \}", manifest))
    rows = []
    for f in sorted((lib / "fragments").glob("*.fragment.yaml")):
        d = read_front(f.read_text())
        params = d.get("params", {})
        rows.append((d["doc"].get("category", ""), d["fragment"], d["doc"]["summary"], params, d.get("emits", []), d.get("slots", {})))
    lines = ["---", f"library: {lib.name}", f"version: {version}", f"summary: {summary}", f"fragments: {len(rows)}",
             "language: \"1.2\"", "licence: proprietary (see LICENSE)", "---", "", f"# {title} library", "",
             summary, "", f"{len(rows)} fragments, written as typed fragments (fragments are functions): local parameter and column names,"
             " the caller maps its own data and column names at the use, hermetic, events returned. Each has an example Sutra under"
             " `examples/` and a ViewModel snapshot under `goldens/`.", ""]
    for cat, name in cats.items():
        mine = [r for r in rows if r[0] == cat]
        if not mine:
            continue
        lines += [f"## {name}", ""]
        for _, n, s, params, emits, slots in mine:
            lines += [f"### `{lib.name}/{n}@1`", "", s, "", "| Parameter | Kind | Notes |", "|---|---|---|"]
            for pn, p in params.items():
                kind = p.get("type", "")
                if kind == "table":
                    kind = "table(" + ", ".join(p.get("columns", {}).keys()) + ")"
                note = "required" if p.get("required") else ("optional" if p.get("optional") else f"default {p.get('default')!r}")
                lines.append(f"| `{pn}` | {kind} | {note}. {p.get('doc', '')} |")
            if emits:
                lines += ["", "Events: " + ", ".join(f"`{e['name']}`" for e in emits)]
            if slots:
                lines += ["", "Slots: " + ", ".join(f"`{k}`" for k in slots)]
            lines += ["", f"Example: `examples/{n}.sutra.yaml`.", ""]
    (lib / "README.md").write_text("<!-- Copyright (c) 2026 Ashutosh Sinha <ajsinha@gmail.com>. All rights reserved. -->\n" + "\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("libraries", nargs="*")
    ap.add_argument("--update-goldens", action="store_true")
    ap.add_argument("--release", action="store_true", help="sign with the owner's release key (RACHANA_RELEASE_PUBLIC, RACHANA_RELEASE_SEED)")
    ap.add_argument("--rachana-java", metavar="DIR")
    a = ap.parse_args()
    if a.rachana_java:
        copy_jars(a.rachana_java)
    if not any(jars_dir().glob("rachana-cli-*.jar")):
        sys.exit("no Rachana jars: run with --rachana-java <drishti-rachana>/java (after ./mvnw clean package -DskipTests)")
    libs_root = ROOT / "libraries"
    libs = [libs_root / n for n in a.libraries] if a.libraries else sorted(p for p in libs_root.iterdir() if p.is_dir())
    if a.release:
        pub, seed = os.environ.get("RACHANA_RELEASE_PUBLIC"), os.environ.get("RACHANA_RELEASE_SEED")
        if not pub or not seed:
            sys.exit("--release needs RACHANA_RELEASE_PUBLIC and RACHANA_RELEASE_SEED (the owner's key)")
    else:
        pub, seed = dev_key() or sys.exit(1)
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    for lib in libs:
        print(f"== {lib.name}")
        write_readme(lib)
        if cli("build", str(lib)) is None:
            return 1
        check = [java(), "-cp", str(jars_dir() / "*"), str(ROOT / "tools" / "LibCheck.java"), str(libs_root)]
        if a.update_goldens:
            check.append("--update")
        r = run(check)
        print(r.stdout.rstrip())
        if r.returncode != 0:
            print(r.stderr.rstrip())
            return 1
        if a.update_goldens and cli("build", str(lib)) is None:
            return 1
        if cli("sign", str(lib), pub, seed) is None:
            return 1
        archive = cli("pack", str(lib), "--out", str(dist), "--require-signed", "--publisher", pub)
        if archive is None:
            return 1
        print(f"  packed {archive}")
        if cli("verify", archive.splitlines()[-1], "--require-signed", "--publisher", pub) is None:
            return 1
        print("  verified (signed)")
    print("all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
