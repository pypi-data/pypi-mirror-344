#!/bin/bash
set -euo pipefail

# Usage: ./scripts/bump_and_tag_version.sh [patch|minor|major]
# Example: ./scripts/bump_and_tag_version.sh minor

# 1. Ensure you're on main
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "🚫 You are on branch '$CURRENT_BRANCH'. Please switch to 'main' to bump the version."
  exit 1
fi

# 2. Check input
if [[ $# -ne 1 ]]; then
  echo "❌ Missing version bump level. Usage: $0 [patch|minor|major]"
  exit 1
fi

BUMP_LEVEL=$1

# 3. Bump the version using poetry
poetry version "$BUMP_LEVEL"

# 4. Get the new version
VERSION=$(poetry version -s)
echo "🔖 New version is: $VERSION"

# 5. Commit the change
git add pyproject.toml
git commit -m "Bump version to $VERSION"

# 6. Create tag
git tag "$VERSION"

# 7. Prompt to push
echo ""
read -rp "🚀 Do you want to push to origin (main + tag $VERSION)? [y/N] " CONFIRM

if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
  git push origin main
  git push origin "$VERSION"
  echo "✅ Pushed main and tag $VERSION to origin"
else
  echo "❌ Push aborted. To push manually, run:"
  echo "    git push origin main"
  echo "    git push origin $VERSION"
fi
