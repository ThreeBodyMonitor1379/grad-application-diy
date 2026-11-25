#!/bin/sh
set -eu
base=$(CDPATH= cd -P "$(dirname "$0")" && pwd)
exec /bin/sh "$base/install.sh" "$@"
