# -*- coding: utf-8 -*-

from __future__ import print_function
import os

import sh

from logging_service import __version__ as version


def get_path():
    return os.path.abspath(os.path.dirname(__file__))


def get_git(git_path_home_project):
    return sh.git.bake(_cwd=git_path_home_project)


def open_file():
    return open('build_version', 'w+')


def main():
    path = get_path()
    git = get_git(path)

    build_file = open_file()
    build_version = int(build_file.readlines()[0])
    build_version += 1
    build_file.write(str(build_version))
    build_file.close()

    build_version = version + '-' + str(build_version)
    git('tag', build_version)
    git('push', 'origin', '--tags')


if __name__ == '__main__':
    main()
