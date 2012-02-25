#!/usr/bin/env bash
# Remove old manifest file, or thing may go horribly wrong
rm MANIFEST
# Create source and windows packages, register and upload to PyPI!
python setup.py register sdist bdist_wininst upload
