Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)
if (Test-Path "build") {
    Remove-Item -Path "build" -Recurse -Force
}
New-Item -ItemType Directory -Path "build" -Force | Out-Null
cd build
Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.1/python-3.11.1-embed-amd64.zip -OutFile python-3.11.1-embed-amd64.zip
Expand-Archive .\python-3.11.1-embed-amd64.zip
cd .\python-3.11.1-embed-amd64
Add-Content -Path .\python311._pth -Value 'import site'
Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
.\python.exe get-pip.py
Remove-Item -Path .\get-pip.py
Remove-Item -Path "Scripts" -Recurse -Force
Remove-Item -Path ..\python-3.11.1-embed-amd64.zip
.\python.exe -m pip install setuptools
.\python.exe -m pip install --no-deps -r ../../../common/no-deps.txt
.\python.exe -m pip cache purge
cd ..
New-Item -ItemType Directory -Path "scripts" -Force | Out-Null
$lines = Get-Content "../../common/requirements.txt"
$index = 1
$pattern = '^[a-zA-Z0-9_.-]+'

foreach ($line in $lines) {
    if (![string]::IsNullOrWhiteSpace($line)) {
        if ($line -match $pattern) {
            $packageName = $matches[0]
        } else {
            $packageName = $line  # fallback
        }

        $batContent = @"
rem Installing $packageName
setlocal
set "apppath=%~1"
"%apppath%\python.exe" -m pip install "$line"
if %ERRORLEVEL% neq 0 (
    exit /b %ERRORLEVEL%
)
endlocal
exit /b 0
"@
        $batPath = "scripts\install$index.bat"
        Set-Content -Path $batPath -Value $batContent
        $index++
    }
}

$batContent = @"
rem Clean cache
setlocal
set "apppath=%~1"
"%apppath%\python.exe" -m pip cache purge
if %ERRORLEVEL% neq 0 (
    exit /b %ERRORLEVEL%
)
endlocal
exit /b 0
"@
$batPath = "scripts\install$index.bat"
Set-Content -Path $batPath -Value $batContent

$inputFolder = "..\..\common\gpu-requirements"
$outputFolder = "gpu-requirements"

if (-not (Test-Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder | Out-Null
}

Get-ChildItem -Path $inputFolder -Filter "*-requirements.txt" -File | ForEach-Object {
    $filename = $_.BaseName -replace "-requirements$", ""
    $outputFile = Join-Path $outputFolder "$filename.bat"

    # Lire les lignes non vides
    $args = Get-Content $_.FullName | Where-Object { $_.Trim() -ne "" }
    $pipArgs = $args -join " "

    $batContent = @"
rem Installing Pytorch (Heavy, can take a while)
setlocal
set "apppath=%~1"
"%apppath%\python.exe" -m pip install $pipArgs
if %ERRORLEVEL% neq 0 (
    exit /b %ERRORLEVEL%
)
endlocal
exit /b 0
"@

    Set-Content -Path $outputFile -Value $batContent
    Write-Host "Créé: $outputFile"
}

cd ..
$localPrograms = Join-Path $env:LOCALAPPDATA "Programs"
& "$localPrograms\Inno Setup 6\ISCC.exe" setup.iss

if ($LASTEXITCODE -ne 0) {
    Write-Host "Inno Setup compilation failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
} else {
    Write-Host "Inno Setup compilation succeeded."
}
Remove-Item -Path "build" -Recurse -Force
Write-Host "Build directory cleaned up."
Write-Host "Build process completed successfully."
exit 0