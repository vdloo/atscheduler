#!/usr/bin/env bash
set -e

function rm_pyc {
    find . -type f -name *.pyc -delete
}

rm_pyc
nosetests tests/
rm_pyc
