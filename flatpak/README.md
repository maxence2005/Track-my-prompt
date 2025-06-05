# Instructions pour construire TrackMyPrompt en Flatpak
sudo apt install flatpak tk-dev flatpak-builder
flatpak remote-info flathub &> /dev/null || flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub org.freedesktop.Sdk//24.08
flatpak install -y flathub org.freedesktop.Platform//24.08
flatpak-builder --repo=flatpak-build/repo-local --force-clean flatpak-build/build-dir flatpak/manifest.json
flatpak build-bundle flatpak-build/repo-local flatpak-build/TrackMyPrompt.flatpak iut.sae.TrackMyPrompt



# Instructions pour installer TrackMyPrompt en Flatpak
## Ajouter Flathub si non présent
flatpak remote-info flathub &> /dev/null || flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

## Installer le runtime requis
flatpak install -y flathub org.freedesktop.Platform//24.08

## Installer l'application depuis un fichier local (ou un repo perso)
flatpak install -y ./TrackMyPrompt.flatpak

## (optionnel) lancer l'application
flatpak run iut.sae.TrackMyPrompt

## Désinstaller l'application
flatpak uninstall --delete-data iut.sae.TrackMyPrompt