#!/bin/bash
# This script renames all files in the lessons/ directory to lowercase only.
# It uses a two-step rename to force git to notice case-only renames on case-insensitive filesystems.
# Now, it does this for every file, even if already lowercase.
# Run this script from the root of the repo.

find "lessons/" -depth -print | while read file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    lowerbase=$(echo "$base" | tr '[:upper:]' '[:lower:]')
    tmpname="$dir/.tmp_rename_$$"
    mv "$file" "$tmpname"
    mv "$tmpname" "$dir/$lowerbase"
done
