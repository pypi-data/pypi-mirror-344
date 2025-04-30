from .synchronize import synchronize


def uncluster(
    remote_src: str | None = None,
    local_dest: str | None = None,
    verbose: bool = False,
) -> None:
    """
    Mirror a remote folder locally.

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
        verbose (int): If True, enable verbosity.
    """
    synchronize(remote_src, local_dest, verbose)
