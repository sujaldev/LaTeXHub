# This script defines some bash functions that can be used in your build script.
OWNER="%%USER%%"
REPO="%%REPO%%"
BRANCH="%%BRANCH%%"

GITHUB_TOKEN="%%GITHUB_TOKEN%%"
DEPLOYMENT_ID=""
DEPLOYMENT_URL=""

MARKDOWN_FILE_URLS="%%MARKDOWN_FILE_URLS%%"

create_deployment() {
  DEPLOYMENT_ID=$(curl -s -L -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/$OWNER/$REPO/deployments" \
    -d "{\"ref\":\"$BRANCH\",\"environment\":\"pdf\"}")

  DEPLOYMENT_ID=$(echo "$DEPLOYMENT_ID" | python3 -c "import sys, json; print(json.loads(sys.stdin.read())['id'])")
}

update_deployment() {
  DEPLOYMENT_URL="${2:-$DEPLOYMENT_URL}"
  curl -s -L -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/$OWNER/$REPO/deployments/$DEPLOYMENT_ID/statuses" \
    -d "{\"state\":\"$1\",\"environment_url\":\"$DEPLOYMENT_URL\"}"
}

clear_image_cache() {
  for URL in ${MARKDOWN_FILE_URLS//,/ }; do
    for IMAGE_URL in $(curl -s "$URL" | grep --color=never -Poi "https:\/\/camo[^\"]*"); do
      curl -X PURGE "${IMAGE_URL%\\}"
    done
  done
}

pdf_to_image() {
  DEFAULT_PREFIX="preview"
  PREFIX="${2:-$DEFAULT_PREFIX}"
  pdftoppm "$1" "$PREFIX" -png
}
