#!/bin/bash

# Navigate to your project directory
cd ./ || exit

# Pull the latest changes from the remote repository
git pull origin main || exit

# Add all changes to the staging area
git add .

# Commit the changes with a default message, or use "$1" to specify a message as an argument
commit_message=${1:-"Quick push of current changes"}
git commit -m "$commit_message" || { echo "Commit failed"; exit 1; }

# Push the changes to the remote repository
git push origin main || { echo "Push failed"; exit 1; }
