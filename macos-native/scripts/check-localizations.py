#!/usr/bin/env python3
"""Check that the Vietnamese and English string catalogs stay in step.

Usage: python3 scripts/check-localizations.py

For each catalog pair it fails when a line does not parse, a key repeats, the
two languages have different keys, a translation is empty, or the format
arguments (%@, %ld, %1$@ …) differ. Runs on Linux, so problems show up before
the macOS build.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS = [
    ROOT / "Sources" / "HVNRemoteHub" / "Resources" / "{}.lproj" / "Localizable.strings",
    ROOT / "Resources" / "InfoPlist" / "{}.lproj" / "InfoPlist.strings",
]
ENTRY = re.compile(r'^"((?:[^"\\]|\\.)*)"\s*=\s*"((?:[^"\\]|\\.)*)";$')
FORMAT = re.compile(r"%(?:([1-9][0-9]*)\$)?[-+ #0']*[0-9]*(?:\.[0-9]+)?(hh|ll|[hlLqjzt])?([@diuoxXfFeEgGaAcCsSpn%])")


def arguments(text):
    result, following = [], 1
    for match in FORMAT.finditer(text):
        if match.group(3) == "%":
            continue
        if match.group(1):
            position = int(match.group(1))
        else:
            position, following = following, following + 1
        result.append(f"{position}:{match.group(2) or ''}{match.group(3)}")
    return sorted(result)


def load(path):
    catalog = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("/*") or line.startswith("//"):
            continue
        match = ENTRY.match(line)
        if not match:
            raise SystemExit(f"{path.relative_to(ROOT)}:{number}: cannot parse: {line[:80]}")
        key, value = match.groups()
        if key in catalog:
            raise SystemExit(f"{path.relative_to(ROOT)}:{number}: duplicate key: {key[:80]}")
        catalog[key] = value
    return catalog


def main():
    for pattern in PAIRS:
        vietnamese, english = load(Path(str(pattern).format("vi"))), load(Path(str(pattern).format("en")))
        name = pattern.name
        if set(vietnamese) != set(english):
            raise SystemExit(f"{name}: keys differ: {sorted(set(vietnamese) ^ set(english))[:10]}")
        for key, value in english.items():
            if not vietnamese[key].strip():
                raise SystemExit(f"{name}: empty Vietnamese translation: {key[:80]}")
            if arguments(value) != arguments(vietnamese[key]):
                raise SystemExit(f"{name}: format arguments differ: {key[:80]}")
        print(f"{name}: {len(english)} keys, vi and en match")


if __name__ == "__main__":
    sys.exit(main())
