#!/usr/bin/env python3
# Copyright (c) 2020 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

import git
import sys

def main(argv):
    print("::set-output name=release-notes::Arguments: {}".format(argv))

if __name__ == '__main__':
    main(sys.argv)
