#!/usr/bin/env bash
# Builds the site and uploads it to MilesWeb's public_html over FTP.
# Credentials live in .ftp_credentials (untracked, see .gitignore) — never
# committed and never entered into any web login form.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .ftp_credentials ]; then
  echo "Missing .ftp_credentials — see build/deploy_ftp.sh for the expected format." >&2
  exit 1
fi
source .ftp_credentials

python3 build/build.py

REMOTE_BASE="ftp://${FTP_HOST}:${FTP_PORT}/public_html"

find . \
  \( -path './.git' -o -path './.github' -o -path './.claude' -o -path './build' \) -prune -o \
  -type f \
  ! -name '.DS_Store' ! -name '.gitignore' ! -name '.nojekyll' ! -name 'README.md' ! -name '.ftp_credentials' \
  -print |
while IFS= read -r f; do
  rel="${f#./}"
  echo "Uploading $rel"
  curl -s --user "${FTP_USER}:${FTP_PASS}" --ftp-create-dirs -T "$f" "${REMOTE_BASE}/${rel}"
done

echo "Deploy complete: https://dsignzhub.com/"
