#!/usr/bin/env python3
# Copyright (c) 2020 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

import git
import sys

def get_repo():
    repo = git.Repo()

def get_release_commit(repo, release_tag):
    tags = [t for t in repo.tags if t.name == release_tag]
    if len(tags) != 0:
        print("Tag {} exists and points at commit {}".format(release_tag, tags[0].commit.hexsha))
        return tags[0].commit
    print("Tag {} does not exist, using HEAD commit {}".format(release_tag, repo.head.commit.hexsha))
    return repo.head.commit

def get_last_release(repo, release_commit):
    pass

def main(argv):
    repo = get_repo()

    if len(argv) < 2:
        sys.stderr.write("ERROR: 'release' is a required argument")
        sys.exit(1)

    release = argv[1]
    print("Generating release notes for release {}")

    if len(argv) >= 3:
        output_path = argv[2]
        print("Will generate output in {}".format(output_path))

    release_commit = get_release_commit(repo, release)

    print("::set-output name=release-notes::Release {} points at commit {}".format(release, release_commit))

if __name__ == '__main__':
    main(sys.argv)
