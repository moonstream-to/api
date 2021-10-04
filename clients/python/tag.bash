#!/usr/bin/env bash
set -e
TAG="clients/python/v$(python setup.py --version)"
read -r -p "Tag: $TAG -- tag and push (y/n)?" ACCEPT
if [ "$ACCEPT" = "y" ]
then
  echo "Tagging and pushing: $TAG..."
  git tag "$TAG"
  git push upstream "$TAG"
else
  echo "noop"
fi
