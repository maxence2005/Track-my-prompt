[Setup]
AppName=TrackMyPrompt
AppVersion=1.0
DefaultDirName={autopf}\TrackMyPrompt
DefaultGroupName=TrackMyPrompt
OutputDir=.
OutputBaseFilename=TrackMyPromptInstaller
Compression=lzma
SolidCompression=yes
LicenseFile=../../LICENSE

[Files]
Source: "../../track_my_prompt\*"; DestDir: "{app}\track_my_prompt"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "build/python-3.11.1-embed-amd64\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "build/scripts\install*.bat"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "launch.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Icons]
Name: "{group}\TrackMyPrompt"; Filename: "{app}\launch.bat"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\TrackMyPrompt"; Filename: "{app}\launch.bat"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{group}\Uninstall TrackMyPrompt"; Filename: "{uninstallexe}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\Lib"
Type: filesandordirs; Name: "{app}\Scripts"
Type: filesandordirs; Name: "{app}\share"

Type: dirifempty; Name: "{app}"

[Code]
var
  MyComboBox: TNewComboBox;
  ResultCode: Integer;
  ScriptCount: Integer;
  ScriptFiles: TStringList;

procedure CreateDropdown;
begin
  MyComboBox := TNewComboBox.Create(WizardForm);
  MyComboBox.Parent := WizardForm.SelectDirPage;
  MyComboBox.Top := WizardForm.DirEdit.Top + WizardForm.DirEdit.Height + 16;
  MyComboBox.Left := WizardForm.DirEdit.Left;
  MyComboBox.Width := WizardForm.DirEdit.Width;
  MyComboBox.Items.Add('Option A');
  MyComboBox.Items.Add('Option B');
  MyComboBox.Items.Add('Option C');
  MyComboBox.ItemIndex := 0;
end;

function FindInstallScripts(): Integer;
var
  I: Integer;
  ScriptPath: string;
begin
  Result := 0;
  ScriptFiles := TStringList.Create;
  
  // Search for install1.bat, install2.bat, etc.
  I := 1;
  while True do
  begin
    ScriptPath := ExpandConstant('{tmp}\install' + IntToStr(I) + '.bat');
    if FileExists(ScriptPath) then
    begin
      ScriptFiles.Add(ScriptPath);
      Inc(Result);
      Inc(I);
    end
    else
      Break;
  end;
  
  Log('Number of scripts found: ' + IntToStr(Result));
end;

procedure ExecuteScripts();
var
  I: Integer;
  CurrentProgress: Integer;
  ProgressMax: Integer;
  ScriptFile: string;
  ScriptMessage: string;
  FileLines: TStringList;
begin
  if ScriptCount = 0 then
    Exit;
    
  ProgressMax := WizardForm.ProgressGauge.Max;

  for I := 0 to ScriptFiles.Count - 1 do
  begin
    CurrentProgress := (I * ProgressMax) div ScriptCount;
    ScriptFile := ScriptFiles[I];

    // Read rem in the first line of the script for a message
    ScriptMessage := '';
    FileLines := TStringList.Create;
    try
      FileLines.LoadFromFile(ScriptFile);
      if (FileLines.Count > 0) and (Pos('rem', LowerCase(Trim(FileLines[0]))) = 1) then
        ScriptMessage := Trim(Copy(FileLines[0], 4, MaxInt)); // Enlève le "rem "
    except
      ScriptMessage := '';
    end;
    FileLines.Free;

    if ScriptMessage = '' then
      ScriptMessage := 'Running ' + ExtractFileName(ScriptFile) + '...';

    // UI updates
    WizardForm.StatusLabel.Caption := 'Step ' + IntToStr(I + 1) + '/' + IntToStr(ScriptCount) + ' : ' + ScriptMessage;
    WizardForm.ProgressGauge.Position := CurrentProgress;
    WizardForm.Repaint;

    Log('Running script: ' + ScriptFile);

    if not Exec(ScriptFile, ExpandConstant('"{app}"'), '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      MsgBox('Error while running script ' + ExtractFileName(ScriptFile) + #13#10'Error code: ' + IntToStr(ResultCode), mbError, MB_OK);
      Exit;
    end;

    if ResultCode <> 0 then
    begin
      if MsgBox('Script ' + ExtractFileName(ScriptFile) + ' failed (code: ' + IntToStr(ResultCode) + ')' + #13#10'Do you want to continue the installation?', mbConfirmation, MB_YESNO) = IDNO then
        Exit;
    end;
  end;

  WizardForm.StatusLabel.Caption := 'Installation completed successfully!';
  WizardForm.ProgressGauge.Position := ProgressMax;
  WizardForm.Repaint;
end;

procedure InitializeWizard;
begin
  CreateDropdown;
  ScriptFiles := TStringList.Create;
  WizardForm.DiskSpaceLabel.Caption := 'Approximately 3 GB of disk space will be used.';
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Find all install scripts
    ScriptCount := FindInstallScripts();
    
    if ScriptCount > 0 then
    begin
      Log('Starting post-install scripts execution');
      ExecuteScripts();
    end
    else
    begin
      Log('No install scripts found');
      WizardForm.StatusLabel.Caption := 'No configuration script found.';
    end;
  end;
end;

procedure DeinitializeSetup();
begin
  if Assigned(ScriptFiles) then
    ScriptFiles.Free;
end;