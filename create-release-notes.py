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


def merge_base_distance(repo, current_commit, past_commit):
    merge_bases = repo.merge_base(current_commit, past_commit)
    if len(merge_bases) == 0:
        return 1000000000
    merge_base = merge_bases[0]

    if merge_base == current_commit:
        return 0

    return 1 + min([merge_base_distance(repo, parent, past_commit) for parent in current_commit.parents])


def get_oldest_commit(commit):
    if len(commit.parents) == 0:
        return commit
    return get_oldest_commit(commit.parents[0])


def get_last_release(repo, release_commit):
    release_datetime = release_commit.committed_datetime
    past_tags = [t for t in repo.tags if t.commit.committed_datetime < release_datetime \
                                         and "rc" not in t.name \
                                         and "RC" not in t.name]
    if len(past_tags) == 0:
        return "the beginning of time", get_oldest_commit(release_commit)

    past_tags.sort(key=lambda tag: merge_base_distance(repo, release_commit, tag.commit))

    closest_tag = past_tags[0]

    return closest_tag.name, closest_tag.commit


def main(argv):
    project_name, release, output_path = parse_args(argv)

    repo = get_repo()
    
    release_commit = get_release_commit(repo, release)
    last_release, last_release_commit = get_last_release(repo, release_commit)

    num_commits = repo.git.rev_list("--count", "{}..{}".format(last_release_commit, release))
    stats = repo.git.diff("--shortstat", last_release_commit, release).strip()
    authors = [author.split('\t')[1] for author in repo.git.shortlog("-s", "-n", "--no-merges", "{}..{}".format(last_release_commit, release)).split('\n')]
    merges = repo.git.log("--merges", "--pretty=format:\"%h %b\"", "{}..{}".format(last_release_commit, release)).split('\n')

    values = {
        'project_name': project_name,
        'release': release,
        'last_release': last_release,
        'num_commits': num_commits,
        'stats': stats,
        'authors': authors,
        'merges': merges,
    }

    release_notes = get_template().render(values)

    if output_path != None:
        with open(output_path, 'w') as output_file:
            output_file.write(release_notes)

    release_notes.replace("\n", "%0A")

    print("::set-output name=release-notes::{}".format(release_notes))


if __name__ == '__main__':
    main(sys.argv)
