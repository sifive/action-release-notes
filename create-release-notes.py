#!/usr/bin/env python3
# Copyright (c) 2020 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

import git
import jinja2
import sys

def parse_args(argv):
    if len(argv) < 3:
        sys.stderr.write("ERROR: 'release' is a required argument")
        sys.exit(1)

    project_name = argv[1]

    release = argv[2]

    output_path = None
    if len(argv) >= 4:
        output_path = argv[3]
        print("Will generate output in {}".format(output_path))

    return project_name, release, output_path


def get_repo():
    return git.Repo()


def get_template():
    env = jinja2.Environment(
        loader=jinja2.PackageLoader(__name__, "templates"),
        trim_blocks=True, lstrip_blocks=True,
    )
    return env.get_template("notes.md")


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
    project_name, release, output_path = parse_args(argv)

    repo = get_repo()
    
    release_commit = get_release_commit(repo, release)

    values = {
        'project_name': project_name,
        'release': release,
    }

    release_notes = get_template().render(values)

    if output_path != None:
        with open(output_path, 'w') as output_file:
            output_file.write(release_notes)

    release_notes.replace("\n", "%0A")

    print("::set-output name=release-notes::{}".format(release_notes))

if __name__ == '__main__':
    main(sys.argv)
