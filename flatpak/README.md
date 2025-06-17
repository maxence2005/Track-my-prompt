# Instructions to build TrackMyPrompt in Flatpak
sudo apt install flatpak tk-dev flatpak-builder
flatpak remote-info flathub &> /dev/null || flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub org.freedesktop.Sdk//24.08
flatpak install -y flathub org.freedesktop.Platform//24.08
flatpak-builder --repo=flatpak-build/repo-local --force-clean flatpak-build/build-dir flatpak/manifest.json
flatpak build-bundle flatpak-build/repo-local flatpak-build/TrackMyPrompt.flatpak iut.sae.TrackMyPrompt



# Instructions to install TrackMyPrompt in Flatpak
## Add Flathub if not present
flatpak remote-info flathub &> /dev/null || flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

## Install the required runtime
flatpak install -y flathub org.freedesktop.Platform//24.08

## Install the application from a local file (or a personal repo)
flatpak install -y ./TrackMyPrompt.flatpak

## (optional) launch the application
flatpak run iut.sae.TrackMyPrompt

## Uninstall the application
flatpak uninstall --delete-data iut.sae.TrackMyPrompt