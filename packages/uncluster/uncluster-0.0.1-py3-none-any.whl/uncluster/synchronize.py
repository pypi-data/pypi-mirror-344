import datetime
import os
import pathlib
import sys

import pexpect
from dotenv import load_dotenv

load_dotenv()

RSYNC_OPTIONS = [
    "-az",
    "--delete",
]


def _getenv(key: str) -> str:
    """Get an environment variable."""
    value = os.getenv(key, None)
    if value is None:
        sys.exit(f"Environment variable '{key}' not found")
    return value


def synchronize(
    remote_src: str | None = None,
    local_dest: str | None = None,
    verbose: bool = False,
) -> int:
    """Synchronize a remote source directory to a local destination directory via rsync.

    Required environment variables:
    - UNCLUSTER_SSH_HOST: The SSH host.
    - UNCLUSTER_SSH_USER: The SSH user.

    Optional environment variables:
    - UNCLUSTER_SSH_PASSWORD: The SSH password.
    - UNCLUSTER_REMOTE_SRC: The path to the remote source directory.
    - UNCLUSTER_LOCAL_DEST: The path to the local destination directory.

    Args:
        remote_src (str | None): The path to the remote source directory. If None, the remote source directory will be taken from the environment variable UNCLUSTER_REMOTE_SRC.
        local_dest (str | None): The path to the local destination directory. If None, the local destination directory will be the same as the remote source directory but under the current working directory.
        verbose (bool): If True, enable verbosity.

    Returns:
        int: Status code indicating the result of the synchronization operation. 0 indicates success.
    """
    remote_src = remote_src or _getenv("UNCLUSTER_REMOTE_SRC")
    host = _getenv("UNCLUSTER_SSH_HOST")
    user = _getenv("UNCLUSTER_SSH_USER")

    remote_src = remote_src.rstrip("/") + "/"
    local_dest = (
        local_dest
        or os.getenv("UNCLUSTER_LOCAL_DEST", None)
        or pathlib.Path(remote_src).stem + "/"
    )

    options = RSYNC_OPTIONS

    if verbose:
        options.append("-v")
        options.append("--progress")

    options = " ".join(options)

    command = f"rsync {options} {user}@{host}:{remote_src} {local_dest}"

    if verbose:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ▶ {command}")

    child = pexpect.spawn(command, encoding="utf-8")

    if verbose:
        child.logfile_read = sys.stdout
        # child.logfile_send = sys.stderr

    try:
        while True:
            i = child.expect(
                [
                    r"Are you sure you want to continue connecting \(yes/no\)\?",
                    r"[Pp]assword:",
                    pexpect.EOF,
                    pexpect.TIMEOUT,
                ]
            )
            # host-key check
            if i == 0:
                child.sendline("yes")
            # password prompt
            elif i == 1:
                password = _getenv("UNCLUSTER_SSH_PASSWORD")
                child.sendline(password)
            # EOF
            elif i == 2:
                break
            # timeout
            elif i == 3:
                raise RuntimeError("Timeout waiting for rsync")
    finally:
        child.close()

    if verbose:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if child.exitstatus == 0:
            print(f"\n[{timestamp}] ▶ rsync completed")
        else:
            print(
                f"\n[{timestamp}] ▶ rsync exited with code {child.exitstatus}"
            )

    return child.exitstatus or 0
