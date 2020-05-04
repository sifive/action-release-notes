# sifive/action-release-notes

A GitHub Action to generate Markdown-formatted release notes automatically for a project.

## Inputs

### `release`

**REQUIRED** The version string for the release.

If the version string matches an existing tag, that tag will be used. If no tag exists, this action assumes
that the current HEAD commit corresponds to the version.

### `output-file`

**OPTIONAL** A path to write the release notes to.

## Outputs

### `release-notes`

The release notes are always output to an actions output named `release_notes`. Use this to provide the output to another action like [actions/create-release](https://github.com/actions/create-release).
