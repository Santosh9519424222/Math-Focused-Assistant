#!/bin/bash
set -e

if ! command -v firebase &>/dev/null; then
  echo "Firebase CLI not installed. Install with: npm install -g firebase-tools"; exit 1;
fi

if [ ! -d frontend/build ]; then
  echo "Frontend build not found. Building...";
  (cd frontend && npm install && npm run build);
fi

echo "Deploying to Firebase Hosting..."
firebase deploy --only hosting

