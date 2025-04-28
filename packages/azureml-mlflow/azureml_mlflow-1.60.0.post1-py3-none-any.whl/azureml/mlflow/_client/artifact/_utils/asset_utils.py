# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os

from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PosixPath, PureWindowsPath
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

DEFAULT_CONNECTION_TIMEOUT = 14400
MAX_CONCURRENCY = 16
PROCESSES_PER_CORE = 2


def upload_directory(
    storage_client: Any,
    source: str,
    dest: str,
    msg: str,
    show_progress: bool,
) -> None:
    source_path = Path(source).resolve()
    prefix = "" if dest == "" else dest + "/"

    upload_paths = []
    size_dict = {}
    total_size = 0
    for root, _, files in os.walk(source_path, followlinks=True):
        upload_paths += list(
            traverse_directory(root, files, source_path, prefix)
        )

    for path, _ in upload_paths:
        if os.path.islink(path):
            path_size = os.path.getsize(
                os.readlink(convert_windows_path_to_unix(path))
            )  # ensure we're counting the size of the linked file
        else:
            path_size = os.path.getsize(path)
        size_dict[path] = path_size
        total_size += path_size

    upload_paths = sorted(upload_paths)
    if len(upload_paths) == 0:
        raise Exception("No files found in the directory to upload.")

    storage_client.total_file_count = len(upload_paths)
    storage_client.indicator_file = upload_paths[0][1]

    num_cores = int(cpu_count()) * PROCESSES_PER_CORE
    with ThreadPoolExecutor(max_workers=num_cores) as ex:
        futures_dict = {  # noqa: F841
            ex.submit(
                upload_file,
                storage_client=storage_client,
                source=src,
                dest=dest,
                size=size_dict.get(src),
                in_directory=True,
                show_progress=show_progress,
            ): (src, dest)
            for (src, dest) in upload_paths
        }

    return prefix


def upload_file(
    storage_client: Any,
    source: str,
    dest: Optional[str] = None,
    msg: Optional[str] = None,
    size: int = 0,
    show_progress: Optional[bool] = None,
    in_directory: bool = False,
    callback: Optional[Any] = None,
) -> None:
    """Upload a single file to remote storage.

    :param storage_client: Storage client object
    :type storage_client: Union[
        azure.ai.ml._artifacts._blob_storage_helper.BlobStorageClient,
        azure.ai.ml._artifacts._gen2_storage_helper.Gen2StorageClient]
    :param source: Local path to project directory
    :type source: str
    :param dest: Remote upload path for project directory (e.g. LocalUpload/<guid>/project_dir)
    :type dest: str
    :param msg: Message to be shown with progress bar (e.g. "Uploading <source>")
    :type msg: str
    :param size: Size of the file in bytes
    :type size: int
    :param show_progress: Whether to show progress bar or not
    :type show_progress: bool
    :param in_directory: Whether the file is part of a directory of files
    :type in_directory: bool
    :param callback: Callback to progress bar
    :type callback: Any
    :return: None
    """
    validate_content = size > 0  # don't do checksum for empty files

    with open(source, "rb") as data:
        storage_client.container_client.upload_blob(
            name=dest,
            data=data,
            validate_content=validate_content,
            overwrite=storage_client.overwrite,
            raw_response_hook=callback,
            max_concurrency=MAX_CONCURRENCY,
            connection_timeout=DEFAULT_CONNECTION_TIMEOUT,
        )

    storage_client.uploaded_file_count += 1


def traverse_directory(
    root: str,
    files: List[str],
    source: str,
    prefix: str,
) -> Iterable[Tuple[str, Union[str, Any]]]:
    # Normalize Windows paths. Note that path should be resolved first as long part will be converted to a shortcut in
    # Windows. For example, C:\Users\too-long-user-name\test will be converted to C:\Users\too-lo~1\test by default.
    # Refer to https://en.wikipedia.org/wiki/8.3_filename for more details.
    root = convert_windows_path_to_unix(Path(root).resolve())
    source = convert_windows_path_to_unix(Path(source).resolve())
    working_dir = convert_windows_path_to_unix(os.getcwd())
    project_dir = root[len(str(working_dir)) :] + "/"
    file_paths = [
        convert_windows_path_to_unix(os.path.join(root, name))
        for name in files
    ]  # get all files not excluded by the ignore file
    file_paths_including_links = {fp: None for fp in file_paths}

    for path in file_paths:
        target_prefix = ""
        symlink_prefix = ""

        # check for symlinks to get their true paths
        if os.path.islink(path):
            target_absolute_path = os.path.join(working_dir, os.readlink(path))
            target_prefix = "/".join([root, str(os.readlink(path))]).replace(
                project_dir, "/"
            )

            # follow and add child links if the directory is a symlink
            if os.path.isdir(target_absolute_path):
                symlink_prefix = path.replace(root + "/", "")

                for r, _, f in os.walk(target_absolute_path, followlinks=True):
                    target_file_paths = {
                        os.path.join(r, name): symlink_prefix
                        + os.path.join(r, name).replace(target_prefix, "")
                        for name in f
                    }  # for each symlink, store its target_path as key and symlink path as value
                    file_paths_including_links.update(
                        target_file_paths
                    )  # Add discovered symlinks to file paths list
            else:
                file_path_info = {
                    target_absolute_path: path.replace(root + "/", "")
                }  # for each symlink, store its target_path as key and symlink path as value
                file_paths_including_links.update(
                    file_path_info
                )  # Add discovered symlinks to file paths list
            del file_paths_including_links[
                path
            ]  # Remove original symlink entry now that detailed entry has been added

    file_paths = sorted(
        file_paths_including_links
    )  # sort files to keep consistent order in case of repeat upload comparisons
    dir_parts = [
        convert_windows_path_to_unix(os.path.relpath(root, source))
        for _ in file_paths
    ]
    dir_parts = [
        "" if dir_part == "." else dir_part + "/" for dir_part in dir_parts
    ]
    blob_paths = []

    for dir_part, name in zip(dir_parts, file_paths):
        if file_paths_including_links.get(
            name
        ):  # for symlinks, use symlink name and structure in directory to create remote upload path
            blob_path = (
                prefix + dir_part + file_paths_including_links.get(name)
            )
        else:
            blob_path = prefix + dir_part + name.replace(root + "/", "")
        blob_paths.append(blob_path)

    return zip(file_paths, blob_paths)


def convert_windows_path_to_unix(path: Union[str, os.PathLike]) -> PosixPath:
    return PureWindowsPath(path).as_posix()


def _build_metadata_dict(name: str, version: str) -> Dict[str, str]:
    """Build metadata dictionary to attach to uploaded data.

    Metadata includes an upload confirmation field, and for code uploads only, the name and version of the code asset
    being created for that data.
    """
    if name:
        linked_asset_arm_id = {"name": name, "version": version}
    else:
        raise Exception("'name' cannot be NoneType for asset artifact upload.")

    metadata_dict = {**{"upload_status": "completed"}, **linked_asset_arm_id}
    return metadata_dict
