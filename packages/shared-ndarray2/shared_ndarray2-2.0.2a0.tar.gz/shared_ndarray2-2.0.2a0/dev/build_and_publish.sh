#!/bin/bash
# shellcheck disable=SC1091,SC2015
SCRIPTNAME="$(basename "$0")"
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(realpath -s "$SCRIPTDIR/..")"

log() {
  local msg="${1:-}"
  local loglevel="${2:-INFO}"
  echo "$SCRIPTNAME $loglevel: $msg" >&2
}

die() {
  log "${1:-}" ERROR
  exit "${2:-1}"
}

REPO="${1:-testpypi}"
log "----Publishing to the $REPO repo.----"

REPO_UPPER="$(echo "$REPO" | tr '[:lower:]' '[:upper:]')"

cd "$PROJECT_ROOT" || die "Couldn't cd to project root"
TOKEN_VARNAME=UV_PUBLISH_TOKEN_${REPO_UPPER}
. .env 2>/dev/null && [ -n "${!TOKEN_VARNAME}" ] || die "No .env file or it doesn't export $TOKEN_VARNAME."
export UV_PUBLISH_TOKEN=${!TOKEN_VARNAME}

uv build || die "Problem with build step"
if [ "$REPO" = "pypi" ]; then
  uv publish
else
  uv publish --index "$REPO"
fi
