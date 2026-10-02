"""`python -m silicat {serve,verify,train}` — command line entry point."""
from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    p = argparse.ArgumentParser(prog="python -m silicat", description="Silicat: serve, verify or train.")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("serve", help="launch the chat server (default)")
    s.add_argument("--host", default=None)
    s.add_argument("--port", type=int, default=None)
    s.add_argument("--ckpt", default=None, help="checkpoint path or name (default: best available)")
    sub.add_parser("verify", help="run the canned-prompt check (args: see silicat.verify --help)", add_help=False)
    sub.add_parser("train", help="run training (args: see silicat.train --help)", add_help=False)
    if not argv:
        argv = ["serve"]
    if argv[0] in ("verify", "train"):
        rest = argv[1:]
        if argv[0] == "verify":
            from .verify import main as vmain
            return vmain(rest)
        from . import train
        sys.argv = ["silicat.train", *rest]
        train._cli()
        return 0
    args = p.parse_args(argv)
    from .server import main as smain
    smain(args.host, args.port, args.ckpt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
