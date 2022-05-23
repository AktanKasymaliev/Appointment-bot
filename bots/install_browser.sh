#!/usr/bin/bash

echo "Downloading Chrome version 843831"
mkdir -p "/opt/chrome/843831"
curl -Lo "/opt/chrome/843831/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F843831%2Fchrome-linux.zip?alt=media"
unzip -q "/opt/chrome/843831/chrome-linux.zip" -d "/opt/chrome/843831/"
mv /opt/chrome/843831/chrome-linux/* /opt/chrome/843831/
rm -rf /opt/chrome/843831/chrome-linux "/opt/chrome/843831/chrome-linux.zip"
