import sys,os
def get_filename(backstep=0):
    """
    Get the file name of the current code line.
    :param backstep:
        will go backward (one layer) from the current function call stack
    """
    return os.path.basename(
        sys._getframe(backstep + 1).f_code.co_filename)  # pylint:disable=W0212
print get_filename()