import atexit
import functools
import logging
import os
import shutil
import tempfile

import appdirs
import joblib


appname = "AvidaScripts"
appauthor = "mmore500"

cachedir = appdirs.user_cache_dir(appname, appauthor)
os.makedirs(cachedir, exist_ok=True)

memory = joblib.Memory(cachedir, verbose=0)

default_avida_revision = "2f2fb6df42325a40ae13a0b8bbefb305aa08841b"


@memory.cache
def get_avida_executable_data(revision: str = default_avida_revision) -> bytes:
    """Build binary executable data for Avida from source."""

    # log building avida from source, this may take a minute
    logging.info("building avida from source, this may take a minute")

    tmpdir = tempfile.mkdtemp()
    command = f"""
    cd {tmpdir}
    git init
    git remote add origin https://github.com/devosoft/Avida.git
    git fetch --depth 1 origin {revision}
    git checkout FETCH_HEAD
    git submodule update --init --recursive --depth 1 -j 4
    ./build_avida -j 8
    """
    os.system(command)

    compiled_avida_executable_path = f"{tmpdir}/cbuild/work/avida"
    with open(compiled_avida_executable_path, "rb") as avida_executable_file:
        binary_data = avida_executable_file.read()

    shutil.rmtree(tmpdir)

    return binary_data


@functools.lru_cache(maxsize=None)
def get_avida_executable_path(revision: str = default_avida_revision) -> str:
    """Get path to the binary Avida executable corresponding to the provided
    the SHA revision.

    Uses cached data, if available. Otherwise, builds from source.
    """

    avida_executable_data = get_avida_executable_data(revision)

    # Write binary data to output file
    fd, tmpfile = tempfile.mkstemp()
    os.close(fd)
    with open(tmpfile, "wb") as file:
        file.write(avida_executable_data)

    # Mark executable
    os.chmod(tmpfile, 0o755)

    # Register for cleanup
    atexit.register(lambda: os.remove(tmpfile))

    return tmpfile
