#!/bin/bash
echo Updating requirements.txt...
pip install pipreqs
pipreqs . --force

sleep .5s