#!/bin/bash
# dpkg --add-architecture i386 && apt update && apt install -y python3 python3-pip curl git wine64 unzip xvfb wine32:i386

set -e
cd "$(dirname "$0")"
export DISPLAY=:99

wine-x11-run() {
    Xvfb $DISPLAY &
    tokill=$!
    wine wineboot --init
    waitonprocess wineserver
    "$@"
    retval=$?
    kill -15 $tokill
    wine wineboot --shutdown
    return $retval
}

waitonprocess() {
    COUNT=0
    echo "Start waiting on $@"
    while pgrep "$@" > /dev/null; do 
            echo "waiting ..."
            sleep 1; 
            COUNT=$((COUNT+1))
            if [ $COUNT -eq 60 ]; then
                exit 3;
            fi
    done
    echo "$@ completed"
}

escone() {
    printf %s\\n "$1" | sed "s/'/'\\\\''/g;1s/^/'/;\$s/\$/' \\\\/"
}

winpaths() {
    for arg; do
        if [ -e "$arg" ]; then
            escone "$(winepath -w "$arg")"
        else
            escone "$arg"
        fi
    done
    echo " "
}

winenv() {
    wine cmd /c "echo $1" | tr -d '\r'
}


# --- 1. Cleaning and preparing the 'build' directory ---
echo "Cleaning the existing 'build' directory..."
if [ -d "build" ]; then
    rm -rf "build"
fi

echo "Creating a new 'build' directory..."
mkdir -p "build"
cd build

# --- 2. Downloading and extracting embedded Python ---
PYTHON_URL="https://www.python.org/ftp/python/3.11.1/python-3.11.1-embed-amd64.zip"
PYTHON_ZIP="python-3.11.1-embed-amd64.zip"
PYTHON_DIR="python-3.11.1-embed-amd64"

echo "Downloading Python from $PYTHON_URL..."
curl -o "$PYTHON_ZIP" "$PYTHON_URL"

echo "Extracting $PYTHON_ZIP..."
unzip "$PYTHON_ZIP" -d "$PYTHON_DIR"
cd "$PYTHON_DIR"

# --- 3. Configuring Python and installing pip ---
echo "Configuring Python to include site packages..."
# Add 'import site' to allow pip to find installed modules
echo "import site" >> python311._pth

echo "Downloading get-pip.py..."
curl -O https://bootstrap.pypa.io/get-pip.py

echo "Installing pip using wine..."
wine python.exe get-pip.py

# Cleaning up pip installation files
rm get-pip.py
rm -rf Scripts
rm ../"$PYTHON_ZIP"

# --- 4. Installing Python dependencies ---
echo "Installing basic dependencies (setuptools)..."
wine python.exe -m pip install setuptools

echo "Downloading dependencies with pip on Linux..."
mkdir -p dependencies
python3 -m pip download --no-deps -r ../../../common/no-deps.txt -d dependencies

echo "Installing dependencies in Wine..."
wine python.exe -m pip install --no-deps dependencies/*

echo "Cleaning pip cache..."
wine python.exe -m pip cache purge
rm -rf dependencies
cd ..

# --- 5. Creating batch installation scripts (.bat) ---
echo "Creating .bat installation scripts..."
mkdir -p "scripts"

# Read requirements.txt and create a .bat for each line
index=1
pattern='^[a-zA-Z0-9_.-]+'
while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip empty lines or comments
    if [[ -z "$line" || "$line" == \#* ]]; then
        continue
    fi
    
    if [[ "$line" =~ $pattern ]]; then
        packageName="${BASH_REMATCH[0]}"
    else
        packageName="$line"  # fallback
    fi
    
    batPath="scripts/install$index.bat"
    echo "Creating $batPath for $packageName..."

    # Use a "here document" (cat << EOF) to create the content of the .bat file
    cat > "$batPath" << EOF
rem Installing $packageName
setlocal
set "apppath=%~1"
"%apppath%\python.exe" -m pip install $line
if %ERRORLEVEL% neq 0 (
    exit /b %ERRORLEVEL%
)
endlocal
exit /b 0
EOF

    ((index++))
done < ../../common/requirements.txt

# Create a final script for cache cleanup
batPath="scripts/install$index.bat"
echo "Creating the final cache cleanup script: $batPath"
cat > "$batPath" << EOF
rem Clean cache
setlocal
set "apppath=%~1"
"%apppath%\python.exe" -m pip cache purge
if %ERRORLEVEL% neq 0 (
    exit /b %ERRORLEVEL%
)
endlocal
exit /b 0
EOF

input_folder="../../common/gpu-requirements"
output_folder="gpu-requirements"

mkdir -p "$output_folder"

for req_file in "$input_folder"/*-requirements.txt; do
    filename=$(basename "$req_file" | sed 's/-requirements\.txt$//')
    output_file="$output_folder/$filename.sh"

    pip_args=$(grep -v '^\s*$' "$req_file" | paste -sd' ' -)

    cat > "$output_file" <<EOF
rem Installing Pytorch (Heavy, can take a while)
setlocal
set "apppath=%~1"
"%apppath%\python.exe" -m pip install $pipArgs
if %ERRORLEVEL% neq 0 (
    exit /b %ERRORLEVEL%
)
endlocal
exit /b 0
EOF

    echo "Create: $output_file"
done

cd ..

# --- 6. Compilation with Inno Setup ---
curl -SL "https://files.jrsoftware.org/is/6/innosetup-6.4.2.exe" -o is.exe \
    && wine-x11-run wine is.exe /SP- /VERYSILENT /ALLUSERS /SUPPRESSMSGBOXES /DOWNLOADISCRYPT=1 \
    && rm is.exe

PROGFILES_PATH="$(winepath -u "$(winenv %PROGRAMFILES%)")"

INNO_BIN="Inno Setup 6/ISCC.exe"
INNO_PATH="${PROGFILES_PATH}/${INNO_BIN}"

echo "Starting Inno Setup compilation..."
wine "$INNO_PATH" setup.iss

# --- 7. Final cleanup ---
echo "Cleaning the 'build' directory..."
rm -rf "build"

echo "Build process completed successfully."
exit 0
