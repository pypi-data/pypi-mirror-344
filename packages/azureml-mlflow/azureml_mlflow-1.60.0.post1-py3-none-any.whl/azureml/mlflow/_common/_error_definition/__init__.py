# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from .azureml_error import AzureMLError
from .utils.error_decorator import error_decorator

__all__ = [
    'AzureMLError',
    'error_decorator'
]
