"""Offline admission contract for source APKs. No network or account access.

A receipt is an untrusted source assertion; policy must be provisioned separately
from an independently trusted APK. A valid APK signature alone is not identity.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

import hostlab

HEX = re.compile(r"[0-9a-f]{64}")
LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")


def validate_receipt(receipt):
    keys = {"schema", "source", "channel", "version_code", "version_name"}
    if not isinstance(receipt, dict) or set(receipt) != keys:
        raise RuntimeError("Receipt requires only schema, source, channel and version fields")
    if type(receipt["schema"]) is not int or receipt["schema"] != 1 or receipt["source"] != "appshare":
        raise RuntimeError("Unsupported source receipt")
    if not isinstance(receipt["channel"], str) or not LABEL.fullmatch(receipt["channel"]):
        raise RuntimeError("Invalid channel label")
    if type(receipt["version_code"]) is not int or receipt["version_code"] <= 0:
        raise RuntimeError("Invalid expected version code")
    if not isinstance(receipt["version_name"], str) or not LABEL.fullmatch(receipt["version_name"]):
        raise RuntimeError("Invalid expected version name")


def verify(apk, receipt, policy):
    validate_receipt(receipt)
    if not isinstance(policy, dict) or set(policy) != {"schema", "package", "channel", "signer_sets"}:
        raise RuntimeError("Invalid trusted signer policy")
    if type(policy["schema"]) is not int or policy["schema"] != 1 or policy["package"] != "tv.danmaku.bili":
        raise RuntimeError("Unsupported trusted signer policy")
    if policy["channel"] != receipt["channel"]:
        raise RuntimeError("Source channel does not match trusted policy")
    sets = policy["signer_sets"]
    if not isinstance(sets, list) or not sets:
        raise RuntimeError("Trusted signer sets must not be empty")
    for signers in sets:
        if (not isinstance(signers, list) or not signers or
                any(not isinstance(x, str) or not HEX.fullmatch(x) for x in signers) or
                len(set(signers)) != len(signers)):
            raise RuntimeError("Invalid trusted signer set")
    row = hostlab.identity(Path(apk))
    if row["package"] != policy["package"]:
        raise RuntimeError("APK package mismatch")
    if any(row[k] != receipt[k] for k in ("version_code", "version_name")):
        raise RuntimeError("APK version does not match source receipt")
    # Exact signer-set matching: an extra signer is not silently trusted.
    if set(row["certificate_sha256"]) not in [set(s) for s in sets]:
        raise RuntimeError("APK signer set is not trusted")
    return {**row, "source": {"provider": receipt["source"], "channel": receipt["channel"]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    # Never retain a stale successful result after a failed attempt: refuse reuse.
    if args.output.exists():
        raise RuntimeError("Output already exists; select a fresh result path")
    row = verify(args.apk, json.loads(args.receipt.read_text(encoding="utf-8")),
                 json.loads(args.policy.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects concurrent attempts using the same result path.
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(row, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("Source APK admission verified; no upload or download performed")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Subprocess/server diagnostics and source payloads must not reach CI logs.
        print("Admission failed: " + (str(exc) if type(exc) is RuntimeError else type(exc).__name__),
              file=sys.stderr)
        sys.exit(1)
