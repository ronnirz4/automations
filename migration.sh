#!/bin/bash

# Bitbucket credentials
BITBUCKET_USER="your_bitbucket_username"
BITBUCKET_APP_PASSWORD="your_bitbucket_app_password"

# GitHub Enterprise credentials
GITHUB_ORG="your_github_org_or_enterprise"
GITHUB_USER="your_github_username"
GITHUB_TOKEN="your_github_token"

# Bitbucket API endpoint
BITBUCKET_API="https://api.bitbucket.org/2.0/repositories/$BITBUCKET_USER?pagelen=100"

# Fetch all repository names from Bitbucket
REPOS=$(curl -s -u "$BITBUCKET_USER:$BITBUCKET_APP_PASSWORD" "$BITBUCKET_API" | jq -r '.values[].slug')

# Loop through each repository
for REPO in $REPOS; do
  echo "Migrating $REPO..."

  # Clone the Bitbucket repository
  git clone https://"$BITBUCKET_USER":"$BITBUCKET_APP_PASSWORD"@bitbucket.org/"$BITBUCKET_USER"/"$REPO".git

  # Create the repository on GitHub Enterprise (requires gh CLI authenticated)
  gh repo create "$GITHUB_ORG/$REPO" --private --confirm

  # Change directory to the repo
  cd "$REPO"

  # Change git remote to GitHub
  git remote set-url origin https://"$GITHUB_USER":"$GITHUB_TOKEN"@github.com/"$GITHUB_ORG"/"$REPO".git

  # Push all branches and tags to GitHub
  git push --mirror

  # Back to parent folder
  cd ..

  # Remove the local copy
  rm -rf "$REPO"

  echo "$REPO migration completed."
done

echo "✅ All migrations completed."
