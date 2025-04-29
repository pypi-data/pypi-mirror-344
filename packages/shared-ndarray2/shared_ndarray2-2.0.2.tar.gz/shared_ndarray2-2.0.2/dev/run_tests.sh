#!/bin/bash -li
# shellcheck disable=SC1091
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

. "$SCRIPTDIR/test_vers.sh"

log() {
    echo "$*" >&2
}

die() {
    log "${1:-}"
    exit "${2-1}"
}

test_in_env() {
    local py_ver numpy_ver env_dir
    py_ver="$1"
    numpy_ver="$2"
    env_dir="$SCRIPTDIR/testenvs/py${py_ver}_numpy${numpy_ver}"
    log "--------Testing in $env_dir--------"
    . "$env_dir/bin/activate"
    cd "$SCRIPTDIR/.." || die "couldn't cd"
    log "----pytest----"
    pytest || die "pytest run failed for $env_dir"
    log "----mypy----"
    # shellcheck disable=SC2071

    if [[ $(printf "%s\n%s" "$numpy_ver" "1.23.0" | sort -V | head -n 1) == "$numpy_ver" ]]; then
        #numpy version is < 2.0
        mypy ./tests ./shared_ndarray2 --cache-dir "$env_dir/.mypy_cache" --always-false NUMPY_1_23 || die "mypy failed for $env_dir"
    else
        mypy ./tests ./shared_ndarray2 --cache-dir "$env_dir/.mypy_cache" --always-true NUMPY_1_23 || die "mypy failed for $env_dir"
    fi
    log "----ruff----"
    ruff check ./tests ./shared_ndarray2 --cache-dir "$env_dir/.ruff_cache" || die "ruff failed for $env_dir"
    deactivate
    log "--------DONE with $env_dir--------"
    echo -e "\n\n\n" >&2
}

test_all() {
    local pair py_ver numpy_ver
    for pair in "${PY_NUMPY_VERS[@]}"; do
        py_ver=$(echo "$pair" | cut -d" " -f1)
        numpy_ver=$(echo "$pair" | cut -d" " -f2);
        test_in_env "$py_ver" "$numpy_ver"
    done
}
test_all
