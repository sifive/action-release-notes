# Copyright (c) 2020 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.7

RUN apt update \
 && apt install -y git

COPY . /action-release-notes

RUN python3 -m pip install -r /action-release-notes/requirements.txt

ENTRYPOINT ["entrypoint.sh"]
