#!/bin/bash

# Bitbucket credentials
BITBUCKET_USER="your_bitbucket_username"
BITBUCKET_APP_PASSWORD="your_bitbucket_app_password"

# GitHub Enterprise credentials
GITHUB_ORG="your_github_org"
GITHUB_USER="your_github_username"
GITHUB_TOKEN="your_github_token"

# Test one specific repo
REPO="repo-name-you-want-to-test"

echo "Migrating $REPO..."

# Clone the Bitbucket repository
git clone https://"$BITBUCKET_USER":"$BITBUCKET_APP_PASSWORD"@bitbucket.org/"$BITBUCKET_USER"/"$REPO".git

# Create the repository on GitHub Enterprise
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

echo "✅ Migration of $REPO completed."
