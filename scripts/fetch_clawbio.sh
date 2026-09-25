#!/usr/bin/env bash
# Clone ClawBio into vendor/ClawBio and check out the pinned commit (CLAWBIO_REF in mise.toml).
set -euo pipefail

REPO="${CLAWBIO_REPO:-https://github.com/ClawBio/ClawBio.git}"
REF="${CLAWBIO_REF:?CLAWBIO_REF not set — run via 'mise run setup'}"
DEST="vendor/ClawBio"

if [ ! -d "$DEST/.git" ]; then
  echo "Cloning ClawBio into $DEST..."
  mkdir -p vendor
  git clone --quiet "$REPO" "$DEST"
fi

current="$(git -C "$DEST" rev-parse HEAD)"
if [ "$current" != "$REF" ]; then
  if ! git -C "$DEST" diff --quiet || ! git -C "$DEST" diff --cached --quiet; then
    echo "vendor/ClawBio has local changes; not switching to $REF. Commit/stash them first." >&2
    exit 1
  fi
  git -C "$DEST" fetch --quiet origin
  git -C "$DEST" -c advice.detachedHead=false checkout --quiet "$REF"
fi
echo "ClawBio at $(git -C "$DEST" rev-parse --short HEAD)"
