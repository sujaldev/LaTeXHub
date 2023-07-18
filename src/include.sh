# This script defines some bash functions that can be used in your build script.
OWNER="%%USER%%"
REPO="%%REPO%%"
BRANCH="%%BRANCH%%"

GITHUB_TOKEN="%%GITHUB_TOKEN%%"
DEPLOYMENT_ID=""

create_deployment() {
  DEPLOYMENT_ID=$(curl -L -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/$OWNER/$REPO/deployments" \
    -d "{\"ref\":\"$BRANCH\",\"environment\":\"pdf\",\"environment_url\":\"$1\"}")

  DEPLOYMENT_ID=$(echo "$DEPLOYMENT_ID" | python -c "import json; print(json.loads(input())['id'])")
}

update_deployment() {
  curl -L -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/$OWNER/$REPO/deployments/$DEPLOYMENT_ID/statuses" \
    -d "{\"state\":\"$1\"}"
}
