
class RunStatus(object):
    """Enum for status of an :py:class:`mlflow.entities.Run`."""
    RUNNING, SCHEDULED, FINISHED, FAILED = range(1, 5)
    _STRING_TO_STATUS = {
        "RUNNING": RUNNING,
        "SCHEDULED": SCHEDULED,
        "FINISHED": FINISHED,
        "FAILED": FAILED,
    }
    _STATUS_TO_STRING = {value: key for key, value in _STRING_TO_STATUS.items()}
    _TERMINATED_STATUSES = set([FINISHED, FAILED])

    @staticmethod
    def from_string(status_str):
        if status_str not in RunStatus._STRING_TO_STATUS:
            raise Exception(
                "Could not get run status corresponding to string %s. Valid run "
                "status strings: %s" % (status_str, list(RunStatus._STRING_TO_STATUS.keys())))
        return RunStatus._STRING_TO_STATUS[status_str]

    @staticmethod
    def to_string(status):
        if status not in RunStatus._STATUS_TO_STRING:
            raise Exception("Could not get string corresponding to run status %s. Valid run "
                            "statuses: %s" % (status, list(RunStatus._STATUS_TO_STRING.keys())))
        return RunStatus._STATUS_TO_STRING[status]

    @staticmethod
    def is_terminated(status):
        return status in RunStatus._TERMINATED_STATUSES

class ViewType(object):
    """Enum to filter requested experiment types."""
    ACTIVE_ONLY, DELETED_ONLY, ALL = range(1, 4)
    _VIEW_TO_STRING = {
        ACTIVE_ONLY: "active_only",
        DELETED_ONLY: "deleted_only",
        ALL: "all",
    }
    _STRING_TO_VIEW = {value: key for key, value in _VIEW_TO_STRING.items()}

    @classmethod
    def from_string(cls, view_str):
        if view_str not in cls._STRING_TO_VIEW:
            raise Exception(
                "Could not get valid view type corresponding to string %s. "
                "Valid view types are %s" % (view_str, list(cls._STRING_TO_VIEW.keys())))
        return cls._STRING_TO_VIEW[view_str]

    @classmethod
    def to_string(cls, view_type):
        if view_type not in cls._VIEW_TO_STRING:
            raise Exception(
                "Could not get valid view type corresponding to string %s. "
                "Valid view types are %s" % (view_type, list(cls._VIEW_TO_STRING.keys())))
        return cls._VIEW_TO_STRING[view_type]
#ViewType.ALL
#ViewType._STRING_TO_VIEW
#ViewType.from_string('active_only')
#ViewType.to_string(2)