#!/bin/bash
# This script installs or upgrades the Flatpak package of TrackMyPrompt.

set -e

# Ask user for the path to the TrackMyPrompt Flatpak file
if [ -z "$1" ]; then
    echo "Please provide the path to the TrackMyPrompt Flatpak file."
    echo "Usage: $0 /path/to/trackmyprompt.flatpak"
    exit 1
fi
TRACKMYPROMPT_FLATPAK_PATH="$1"
# Check if the provided file exists
if [ ! -f "$TRACKMYPROMPT_FLATPAK_PATH" ]; then
    echo "The specified Flatpak file does not exist: $TRACKMYPROMPT_FLATPAK_PATH"
    exit 1
fi

# Check if Flatpak is installed
if ! command -v flatpak &> /dev/null; then
    echo "Flatpak is not installed. Please install Flatpak first."
    echo "You can find installation instructions at https://flatpak.org/setup/"
    exit 1
fi
# Add the Flathub repository if it is not already added
if ! flatpak remote-list | grep -q "flathub"; then
    echo "Adding Flathub repository..."
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
fi

# Check if the runtime is installed, otherwise install it
if ! flatpak list --runtime | grep -q "org.freedesktop.Platform.*24.08"; then
    echo "Installing org.freedesktop.Platform//24.08 runtime..."
    flatpak install -y flathub org.freedesktop.Platform//24.08
fi

# # Get the download link for the Flatpak package
# DOWNLOAD_LINK=$(curl -s "https://forgens.univ-ubs.fr/gitlab/api/v4/projects/1557/releases" | jq -r '.[0].assets.links[0].url')
#
# # Download the Flatpak package
# echo "Downloading TrackMyPrompt Flatpak package..."
# echo "Download link: $DOWNLOAD_LINK"
# curl -L -o /tmp/trackmyprompt.flatpak "$DOWNLOAD_LINK"
# # Install the Flatpak package
# echo "Installing TrackMyPrompt Flatpak package..."
# flatpak install -y --reinstall /tmp/trackmyprompt.flatpak
# # Clean up the downloaded file
# rm -f /tmp/trackmyprompt.flatpak

# Install the Flatpak package
echo "Installing TrackMyPrompt Flatpak package..."
flatpak install -y --reinstall "$TRACKMYPROMPT_FLATPAK_PATH"
# Provide instructions for running the application
echo "TrackMyPrompt has been installed successfully."
echo "You can run it using the following command:"
echo "flatpak run org.trackmyprompt.TrackMyPrompt"
echo "Or you can find it in your application menu. (If it doesn't appear, try logging out and back in.)"