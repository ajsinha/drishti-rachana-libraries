---
summary: Private companion repository of Drishti Rachana. The prebuilt Sutra fragment libraries (core, later finance, genomics, economy, geo, ops, ai), each a folder of typed fragments with examples and tests, packed as signed .rlib archives.
kind: libraries
libraries: [core]
language: "1.2"
build: python3 tools/build.py
licence: proprietary, all rights reserved (decisions L-11, L-12)
depends-on: drishti-rachana (the compiler and the `rachana lib` commands)
---

<!-- Copyright (c) 2026 Ashutosh Sinha <ajsinha@gmail.com>. All rights reserved. -->

# Drishti Rachana libraries

Fragment libraries for [Drishti Rachana](https://github.com/ajsinha/drishti-rachana): an author builds a screen by choosing
a fragment, naming the data and mapping the columns, instead of writing panels. The libraries are proprietary and live
here, apart from the compiler, which carries only a tiny synthetic `demo` library for its conformance suite.

## The rule: fragments are functions

Every fragment is a function of its inputs (decision L-21): its parameters and its table columns have local names, the
caller maps its own data and column names at the use (`rows: { from: $.positions, columns: { desk: BOOK_DESK, amount: MTM_USD } }`),
the mapping is applied when the Sutra compiles, a fragment reads nothing of the screen it is used on, its events are
returned (read as `@<as>.<event>.<field>`), and `as:` makes two uses of one fragment two instances.

## What is here

| Library | State | Fragments |
|---|---|---|
| `core` | baseline LB1 built | 28 of the 31 planned (figures, records, tables, charts, states, history); 3 waiting on language features, listed in [CHANGELOG](CHANGELOG.md) |

Per library, in `libraries/<name>/`: the manifest `<name>.rachana-lib.yaml`, `fragments/` (one file per fragment major),
`examples/` (a Sutra that uses each fragment with a column mapping, on synthetic data), `goldens/` (the ViewModel snapshot
of each example), `README.md` (generated front page), `LICENSE`, `MANIFEST.sha384` (generated) and, when signed, `SIGNATURE`
(never committed).

## Build, test, pack, verify

Prerequisites: JDK 21, Python 3 with PyYAML, and a Rachana build (never installed: a plain build tree).

```text
cd drishti-rachana/java && ./mvnw clean package -DskipTests      # once, in a clean worktree of the compiler
cd drishti-rachana-libraries
python3 tools/build.py --rachana-java ../drishti-rachana/java    # copies the jars to rachana-jars/ (git-ignored), then:
python3 tools/build.py                                           # docs, build, test, sign, pack, verify
python3 tools/build.py --update-goldens core                     # after a deliberate change to a fragment
```

`tools/build.py` runs the Rachana command line (`rachana lib build`, `sign`, `pack`, `verify`; nothing is reimplemented)
and `tools/LibCheck.java`, the library test: each example compiles at language level 1.2 with no problem and no advisory and
its ViewModel equals the golden (object keys compared in sorted order). The result is `dist/<name>-<version>.rlib`
(deterministic, git-ignored).

## Signing

A local build signs with a **development key** created on first use in `keys/dev.key` (git-ignored; each machine has its own).
**Release signing uses the owner's key**: `RACHANA_RELEASE_PUBLIC=... RACHANA_RELEASE_SEED=... python3 tools/build.py --release`.
Consumers pin the publisher key with `rachana lib verify ... --require-signed --publisher <key>`.

## Conventions

Copyright header on every file that can carry a comment; visible file names only; a library holds only `.yaml`, `.json`,
`.jsonl`, `.md`, `LICENSE`, `MANIFEST.sha384` and `SIGNATURE` (no code, no style, no binary). Released fragment majors are frozen:
a change that moves a screen is a new `.v2` file beside the old one. No tags are made here by tooling; releases are the owner's.
