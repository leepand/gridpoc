"""
Utilities for validating user inputs such as metric names and parameter names.
"""
import os.path
import re

# Regex for valid run IDs: must be a 32-character hex string.
_RUN_ID_REGEX = re.compile(r"^[0-9a-f]{32}$")
def _validate_run_id(run_id):
    """Check that `run_id` is a valid run ID and raise an exception if it isn't."""
    if _RUN_ID_REGEX.match(run_id) is None:
        raise Exception("Invalid run ID: '%s'" % run_id)


def _validate_experiment_id(exp_id):
    """Check that `experiment_id`is a valid integer and raise an exception if it isn't."""
    try:
        int(exp_id)
    except ValueError:
        raise Exception("Invalid experiment ID: '%s'" % exp_id)