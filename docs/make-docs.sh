#!/bin/bash

sphinx-apidoc -e -o source-code/modules ./../geowatchutil/
make html
