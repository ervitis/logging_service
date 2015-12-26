# -*- coding: utf-8 -*-

from __future__ import print_function
import os

import sh

from logging_service import __version__ as version


def get_path():
    return os.path.abspath(os.path.dirname(__file__))


def get_git(git_path_home_project):
    return sh.git.bake(_cwd=git_path_home_project)


def open_file(path_file):
    path_file = os.path.join(path_file, 'build_version')
    return open(path_file, 'r+')


def main():
    path = get_path()
    git = get_git(path)

    build_file = open_file(path)
    lines = build_file.readlines()
    build_version_old = int(lines[0])
    build_version = build_version_old + 1
    build_version = str(build_version)
    build_version_old = str(build_version_old)
    lines = [line.replace(build_version_old, build_version) for line in lines]
    build_file.seek(0)
    build_file.writelines(lines)
    build_file.close()

    build_version = version + '-' + build_version
    git('tag', build_version)
    git('push', 'origin', '--tags')


if __name__ == '__main__':
    main()
