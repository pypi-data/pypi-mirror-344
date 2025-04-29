#!/bin/bash -li
# shellcheck disable=SC1090,SC1091
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
readonly SCRIPTDIR
set -e

envs_dir="$SCRIPTDIR/testenvs"

export POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=true

. "$SCRIPTDIR/test_vers.sh"

die() {
    echo "$SCRIPTNAME Error: ${1:-}" >&2
    exit "${2:-1}"
}

setup_venv() {
    local py_ver="$1"
    local numpy_ver="$2"
    local env_dir="$envs_dir/py${py_ver}_numpy${numpy_ver}"
    uv venv -p "$py_ver" "$env_dir" || die "Coudln't create venv"
    source "$env_dir"/bin/activate
    uv pip install "numpy==$numpy_ver"
    uv pip install -e "$SCRIPTDIR/../" || die "Couldn't install nested-config"
    uv pip install pytest ruff mypy || die "Couldn't install testing dependencies"
    deactivate
}

setup_all() {
    local pair py_ver numpy_ver
    for pair in "${PY_NUMPY_VERS[@]}"; do
        py_ver=$(echo "$pair" | cut -d" " -f1)
        numpy_ver=$(echo "$pair" | cut -d" " -f2);
        setup_venv "$py_ver" "$numpy_ver"
    done
}
setup_all
