aiosqlcipher\: encrypted Sqlite for AsyncIO
==============================


aiosqlcipher provides a friendly, async interface to sqlite encrypted databases.
aiosqlcipher is based on the design of aiosqlite , The version of aiosqlite is 0.21.0.



## abort aiosqlite
https://github.com/omnilib/aiosqlite/blob/main/README.rst

# how to use
## install
    uv sync

## .venv
    uv venv .venv

## venv: .venv
    source .venv/bin/activate && make install
    echo 'run `source .venv/bin/activate` to activate virtualenv'

# test
    python -m coverage run -m aiosqlcipher.tests
    python -m coverage report
    python -m mypy -p aiosqlcipher

## perf
    python -m unittest -v aiosqlcipher.tests.perf



## .PHONY: distclean
    distclean: clean
    rm -rf .venv