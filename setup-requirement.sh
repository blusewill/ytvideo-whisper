#!/bin/bash

python3 -m venv ./.virtualenv

source ./.virtualenv/bin/activate

pip3 install -r ./requirement.txt
