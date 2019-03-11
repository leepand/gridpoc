import os
import yaml
import shutil

ENCODING = "utf-8"


def is_directory(name):
    return os.path.isdir(name)


def is_file(name):
    return os.path.isfile(name)


def exists(name):
    return os.path.exists(name)

def build_path(*path_segments):
    """ Returns the path formed by joining the passed-in path segments. """
    return os.path.join(*path_segments)


def mkdir(root, name=None):  # noqa
    """
    Make directory with name "root/name", or just "root" if name is None.
    :param root: Name of parent directory
    :param name: Optional name of leaf directory
    :return: Path to created directory
    """
    target = os.path.join(root, name) if name is not None else root
    try:
        if not exists(target):
            os.makedirs(target)
            return target
    except OSError as e:
        raise e
def list_all(root, filter_func=lambda x: True, full_path=False):
    """
    List all entities directly under 'dir_name' that satisfy 'filter_func'
    :param root: Name of directory to start search
    :param filter_func: function or lambda that takes path
    :param full_path: If True will return results as full path including `root`
    :return: list of all files or directories that satisfy the criteria.
    """
    if not is_directory(root):
        raise Exception("Invalid parent directory '%s'" % root)
    matches = [x for x in os.listdir(root) if filter_func(os.path.join(root, x))]
    return [os.path.join(root, m) for m in matches] if full_path else matches


def list_subdirs(dir_name, full_path=False):
    """
    Equivalent to UNIX command:
      ``find $dir_name -depth 1 -type d``
    :param dir_name: Name of directory to start search
    :param full_path: If True will return results as full path including `root`
    :return: list of all directories directly under 'dir_name'
    """
    return list_all(dir_name, os.path.isdir, full_path)


def list_files(dir_name, full_path=False):
    """
    Equivalent to UNIX command:
      ``find $dir_name -depth 1 -type f``
    :param dir_name: Name of directory to start search
    :param full_path: If True will return results as full path including `root`
    :return: list of all files directly under 'dir_name'
    """
    return list_all(dir_name, os.path.isfile, full_path)

def find(root, name, full_path=False):
    """
    Search for a file in a root directory. Equivalent to:
      ``find $root -name "$name" -depth 1``
    :param root: Name of root directory for find
    :param name: Name of file or directory to find directly under root directory
    :param full_path: If True will return results as full path including `root`
    :return: list of matching files or directories
    """
    path_name = os.path.join(root, name)
    return list_all(root, lambda x: x == path_name, full_path)
        
        
def write_yaml(root, file_name, data, overwrite=False):
    """
    Write dictionary data in yaml format.
    :param root: Directory name.
    :param file_name: Desired file name. Will automatically add .yaml extension if not given
    :param data: data to be dumped as yaml format
    :param overwrite: If True, will overwrite existing files
    """
    if not exists(root):
        raise MissingConfigException("Parent directory '%s' does not exist." % root)

    file_path = os.path.join(root, file_name)
    yaml_file_name = file_path if file_path.endswith(".yaml") else file_path + ".yaml"

    if exists(yaml_file_name) and not overwrite:
        raise Exception("Yaml file '%s' exists as '%s" % (file_path, yaml_file_name))

    try:
        with open(yaml_file_name, 'w') as yaml_file:
            yaml.safe_dump(data, yaml_file, default_flow_style=False, allow_unicode=True)
    except Exception as e:
        raise e


def read_yaml(root, file_name):
    """
    Read data from yaml file and return as dictionary
    :param root: Directory name
    :param file_name: File name. Expects to have '.yaml' extension
    :return: Data in yaml file as dictionary
    """
    if not exists(root):
        raise MissingConfigException(
            "Cannot read '%s'. Parent dir '%s' does not exist." % (file_name, root))

    file_path = os.path.join(root, file_name)
    if not exists(file_path):
        raise MissingConfigException("Yaml file '%s' does not exist." % file_path)

    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise e
def mv(target, new_parent):
    shutil.move(target, new_parent)
    
def write_to(filename, data):
    with codecs.open(filename, mode="w", encoding=ENCODING) as handle:
        handle.write(data)


def append_to(filename, data):
    with open(filename, "a") as handle:
        handle.write(data)


def make_tarfile(output_filename, source_dir, archive_name, custom_filter=None):
    # Helper for filtering out modification timestamps
    def _filter_timestamps(tar_info):
        tar_info.mtime = 0
        return tar_info if custom_filter is None else custom_filter(tar_info)

    unzipped_filename = tempfile.mktemp()
    try:
        with tarfile.open(unzipped_filename, "w") as tar:
            tar.add(source_dir, arcname=archive_name, filter=_filter_timestamps)
        # When gzipping the tar, don't include the tar's filename or modification time in the
        # zipped archive (see https://docs.python.org/3/library/gzip.html#gzip.GzipFile)
        with gzip.GzipFile(filename="", fileobj=open(output_filename, 'wb'), mode='wb', mtime=0)\
                as gzipped_tar, open(unzipped_filename, 'rb') as tar:
            gzipped_tar.write(tar.read())
    finally:
        os.remove(unzipped_filename)


def _copy_project(src_path, dst_path=""):
    """
    Internal function used to copy MLflow project during development.
    Copies the content of the whole directory tree except patterns defined in .dockerignore.
    The MLflow is assumed to be accessible as a local directory in this case.
    :param dst_path: MLflow will be copied here
    :return: name of the MLflow project directory
    """

    def _docker_ignore(mlflow_root):
        docker_ignore = os.path.join(mlflow_root, '.dockerignore')
        patterns = []
        if os.path.exists(docker_ignore):
            with open(docker_ignore, "r") as f:
                patterns = [x.strip() for x in f.readlines()]

        def ignore(_, names):
            import fnmatch
            res = set()
            for p in patterns:
                res.update(set(fnmatch.filter(names, p)))
            return list(res)

        return ignore if patterns else None

    mlflow_dir = "arthur-project"
    # check if we have project root
    assert os.path.isfile(os.path.join(src_path, "setup.py")), "file not found " + str(
        os.path.abspath(os.path.join(src_path, "setup.py")))
    shutil.copytree(src_path, os.path.join(dst_path, mlflow_dir),
                    ignore=_docker_ignore(src_path))
    return mlflow_dir


def _copy_file_or_tree(src, dst, dst_dir=None):
    """
    :return: The path to the copied artifacts, relative to `dst`
    """
    dst_subpath = os.path.basename(os.path.abspath(src))
    if dst_dir is not None:
        dst_subpath = os.path.join(dst_dir, dst_subpath)
    dst_path = os.path.join(dst, dst_subpath)

    dst_dirpath = os.path.dirname(dst_path)
    if not os.path.exists(dst_dirpath):
        os.makedirs(dst_dirpath)

    if os.path.isfile(src):
        shutil.copy(src=src, dst=dst_path)
    else:
        shutil.copytree(src=src, dst=dst_path)
    return dst_subpath


def get_parent_dir(path):
    return os.path.abspath(os.path.join(path, os.pardir))

def list_all_filepaths(absolute_dirpath):
    """Returns all filepaths within dir relative to dir root"""
    return [
        os.path.relpath(os.path.join(dirpath, file), absolute_dirpath)
        for (dirpath, dirnames, filenames) in os.walk(absolute_dirpath)
        for file in filenames
    ]