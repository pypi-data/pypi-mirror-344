# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os


def makedirs_for_file_path(file_path):
    """
    :param file_path: relative or absolute path to a file
    """
    parent_path = os.path.join(file_path, os.path.pardir)
    parent_path = os.path.normpath(parent_path)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path, exist_ok=True)
    return True
