#!/bin/bash

here="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)"
cd $here

db="$here/../db/app.db"

rm -f "$db"

echo "Removed $db"