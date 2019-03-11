# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
import os

project_root = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(project_root, 'core', 'VERSION')) as file:
    VERSION = file.read()


def walker(base, *paths):
    file_list = set([])
    cur_dir = os.path.abspath(os.curdir)

    os.chdir(base)
    try:
        for path in paths:
            for dname, dirs, files in os.walk(path):
                for f in files:
                    file_list.add(os.path.join(dname, f))
    finally:
        os.chdir(cur_dir)

    return list(file_list)

setup(name='gridpoc',
      version=VERSION,
      description='gridpoc',
      author='Leepand',
      license='Apache-2.0',
      #scripts=['api_server/ABtesting/ABstat/ABtesting-web'],
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      #package_data={
      #    module.__name__: walker(
      #      os.path.dirname(module.__file__),
      #      'templates', 'static'
      #  ),
      #}, 
      #include_package_data=True,
      entry_points={
          'console_scripts': [
              # FIXME: change entry-point name (this name of you main program)
              #'abtesting_web={}.ABtesting_web:main'.format(module.__name__),
              #'apidoc_web={}.apidoc_web:main'.format(apidoc_web.__name__),
              #'apidoc_gen={}.apidoc_gen:main'.format(apidoc_web.__name__),
              #'Arthur=Arthur.cli:commands',
              #'apiserver={}.main:main'.format(apifly.__name__),
              #'thriftserver={}.main:main'.format(thriftfly.__name__),
          ]
      },
      #install_requires=open('requirements.txt').readlines(),
      )