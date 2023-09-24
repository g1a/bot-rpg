#!/bin/bash

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DEVOPSDIR="$(dirname $SCRIPTDIR)"
PROJECTDIR="$(dirname $DEVOPSDIR)"

TARGETDIR="/usr/local/bin"
TARGET="$TARGETDIR/bot-rpg"

cat << __EOT__ > $TARGET
cd "$PROJECTDIR"
python3 -m src.main
__EOT__

chmod +x $TARGET

