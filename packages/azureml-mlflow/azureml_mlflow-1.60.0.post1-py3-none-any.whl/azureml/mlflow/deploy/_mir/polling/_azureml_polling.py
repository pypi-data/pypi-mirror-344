# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azure.mgmt.core.polling.arm_polling import ARMPolling


class AzureMLPolling(ARMPolling):
    """
    A polling class for azure machine learning
    """

    def update_status(self):
        """Update the current status of the LRO."""
        super(ARMPolling, self).update_status()
        print(".", end="", flush=True)
