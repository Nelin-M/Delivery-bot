#!/bin/bash

# Check if login and token were provided
if [ $# -ne 2 ]
then
  echo "Error: 2 parameters are required (login and token), but $# were provided."
  echo "Usage: fetch_dev.sh [login] [token]"
  exit 1
fi

# Get login and token
login=$1
token=$2

# Get remote URL and repository path
remote_url=$(git remote -v | grep -m1 '^origin.*(fetch)' | awk '{print $2}')
repo_path=${remote_url#*://github.com/}

# Fetch the "dev" branch using the login and token
git -c http.https://github.com/.extraheader="Authorization: token $token" fetch https://$login:$token@github.com/$repo_path dev

# Exit the script
exit 0