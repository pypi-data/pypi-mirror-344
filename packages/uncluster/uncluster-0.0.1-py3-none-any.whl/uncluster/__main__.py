import argparse
import sys

from .uncluster import uncluster


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="uncluster",
        description="Mirror a remote folder locally via rsync.",
    )
    parser.add_argument(
        "--remote",
        type=str,
        default=None,
        metavar="SRC",
        help="The path to the remote source directory.",
    )
    parser.add_argument(
        "--local",
        type=str,
        default=None,
        metavar="DEST",
        help="The path to the local destination directory.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbosity.",
    )
    args = parser.parse_args()

    try:
        print(
            "Mirror a remote folder locally via rsync.\n\nPress Enter to sync, q + Enter to quit"
        )
        while True:
            if input().lower().strip() == "q":
                break
            uncluster(args.remote, args.local, verbose=args.verbose)
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by Ctrl + c")
    except Exception as e:
        sys.exit(f"An error occurred while synchronization: {e}")


if __name__ == "__main__":
    main()
