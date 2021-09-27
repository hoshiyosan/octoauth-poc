import argparse
import subprocess
import sys

# Define commands


def run_server(host: str, port: int):
    subprocess.call(
        ["uvicorn", "octoauth.__asgi__:api", "--host", host, "--port", str(port)]
    )


# Define CLI behaviour


def parse_args() -> dict:
    """
    Parse arguments coming from stdin.
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run-server", help="Start octoauth oauth2 server"
    )
    run_parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host name on wich server will respond",
    )
    run_parser.add_argument(
        "--port", type=int, default=7000, help="Port on wich server will listen"
    )

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    return vars(args)


def main():
    """
    Parse arguments to determine command,
    then dispatch command to the appropriate function.
    """
    args = parse_args()
    command = args.pop("command")

    if command == "run-server":
        run_server(**args)


if __name__ == "__main__":
    main()
