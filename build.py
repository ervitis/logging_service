# -*- coding: utf-8 -*-

import os

import sh
from logging_service import __version__ as version


def open_file(path):
    return open(path, 'r+')


def get_git(repo_path):
    return sh.git.bake(_cwd=repo_path)


def main():
    file_build = open_file('build_version')
    lines = file_build.readlines()
    build_version_old = lines[0]
    build_version_new = str(int(build_version_old) + 1)
    lines = [line.replace(build_version_old, build_version_new) for line in lines]
    file_build.seek(0)
    file_build.writelines(lines)
    file_build.close()

    repo_path = os.path.abspath(os.path.dirname(__file__))
    git = get_git(repo_path)
    new_tag_version = version + '-' + build_version_new
    git('tag', new_tag_version)
    git('push', 'origin', '--tags')


if __name__ == '__main__':
    main()
