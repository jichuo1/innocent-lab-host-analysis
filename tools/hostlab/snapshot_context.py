"""Capture current production evidence; importing this module performs no I/O."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import hostlab
import source_snapshot


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=hostlab.ROOT)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("production-context.json"))
    args = parser.parse_args(argv)
    ctx = source_snapshot.capture(args.root)
    raw = source_snapshot.serialize(ctx)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=args.output.parent, prefix="." + args.output.name + ".",
                                     suffix=".tmp", delete=False) as stream:
        temp = Path(stream.name)
        stream.write(raw)
    try:
        temp.replace(args.output)
    finally:
        if temp.exists():
            temp.unlink()
    print(json.dumps({"output": str(args.output.resolve()), "source_records": len(ctx["source_records"]),
                      "snapshot_sha256": hashlib.sha256(raw).hexdigest(),
                      "source_tree_sha256": ctx["source_tree_sha256"], "repository_head": ctx["repository_head"],
                      "captured_at": ctx["captured_at"], "dirty": ctx["working_tree_dirty"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
