#!/usr/bin/env bash
curl -F "rst=@Documentation.rst" http://api.rst2a.com/1.0/rst2/html?style=voidspace > documentation.html