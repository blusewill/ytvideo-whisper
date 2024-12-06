# Download Github Repo
# From : https://gist.github.com/Tsugami/2de3d13bfd9f9ffd6ea5eb26efad41cd

function Download-File {
  param (
    [string]$Url,
    [string]$File
  )
  Write-Host "Downloading $Url to $File"
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  Invoke-WebRequest -Uri $url -OutFile $File
}

function Remove-Directory {
  param (
    [string]$Path
  )
  if ([System.IO.Directory]::Exists($Path)) {
    Write-Host "Deleting $Path"
    [System.IO.Directory]::Delete($Path, $true)
  }
}

function Unzip-File {
  param(
    [string]$File,
    [string]$Destination = (Get-Location).Path
  )

  $FilePath = Resolve-Path $File
  $DestinationPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination)

  If ($PSVersionTable.PSVersion.Major -ge 3) {
    [System.IO.Compression.ZipFile]::ExtractToDirectory("$FilePath", "$DestinationPath")
  }
  else {
    throw "Unzip-File is not supported on PowerShell versions less than 3.0"
  }
}

function Move-DirectoryContent {
  param (
    [string]$Source,
    [string]$Destination
  )

  $SourcePath = Resolve-Path $Source
  $DestinationPath = Resolve-Path $Destination

  Write-Output "Moving content of $SourcePath to $DestinationPath"
  Get-ChildItem -Path $SourcePath -Recurse | Move-Item -Destination $DestinationPath
}

$ProgressPreference = 'SilentlyContinue'
$CUR_DIR = Get-Location
if ([System.IO.File]::Exists("$CUR_DIR\ytvideo_whisper.ipynb")) {
   Write-Host "You're Currently Running off the Git Repo" 
}
elseif (Test-Path "$env:USERPROFILE\ytvideo-whisper-master") {
    Write-Host "Previous Installation Detected."
    Write-Host "Starting..."
    $CUR_DIR = "$env:USERPROFILE\ytvideo-whisper-master"
}
else {
    Write-Host "You're Not Running off Git Repo."
    Write-Host "Downloading ytvideo-whisper"
    $username = "blusewill"
    $reponame = "ytvideo-whisper"
    $branch = "master"
    $Temp_DIR = $env:TEMP
    $SourceFile = Join-Path $Temp_DIR "ytvideo-whisper.zip"
    $DestPath = Join-Path $env:userprofile "ytvideo-whisper-master" 

    Download-File "https://github.com/$UserName/$RepoName/archive/$Branch.zip" $SourceFile
    Remove-Directory $DestPath
    Unzip-File $SourceFile $DestPath

    $ZipOutputDir = Join-Path $DestPath "$RepoName-$Branch"

    Move-DirectoryContent $ZipOutputDir $DestPath
    Remove-Directory $ZipOutputDir
    $CUR_DIR = "$env:USERPROFILE\ytvideo-whisper-master"
}


# Function Install Winget / Check Winget
# From : https://github.com/christitustech/winutil

function Test-WinUtilPackageManager {
    <#

    .SYNOPSIS
        Checks if Winget and/or Choco are installed

    .PARAMETER winget
        Check if Winget is installed

    .PARAMETER choco
        Check if Chocolatey is installed

    #>

    Param(
        [System.Management.Automation.SwitchParameter]$winget,
        [System.Management.Automation.SwitchParameter]$choco
    )

    $status = "not-installed"

    if ($winget) {
        # Check if Winget is available while getting it's Version if it's available
        $wingetExists = $true
        try {
            $wingetVersionFull = winget --version
        } catch [System.Management.Automation.CommandNotFoundException], [System.Management.Automation.ApplicationFailedException] {
            Write-Warning "Winget was not found due to un-availablity reasons"
            $wingetExists = $false
        } catch {
            Write-Warning "Winget was not found due to un-known reasons, The Stack Trace is:`n$($psitem.Exception.StackTrace)"
            $wingetExists = $false
    }

        # If Winget is available, Parse it's Version and give proper information to Terminal Output.
    # If it isn't available, the return of this funtion will be "not-installed", indicating that
        # Winget isn't installed/available on The System.
    if ($wingetExists) {
            # Check if Preview Version
            if ($wingetVersionFull.Contains("-preview")) {
                $wingetVersion = $wingetVersionFull.Trim("-preview")
                $wingetPreview = $true
            } else {
                $wingetVersion = $wingetVersionFull
                $wingetPreview = $false
            }

            # Check if Winget's Version is too old.
            $wingetCurrentVersion = [System.Version]::Parse($wingetVersion.Trim('v'))
            # Grabs the latest release of Winget from the Github API for version check process.
            $response = Invoke-RestMethod -Uri "https://api.github.com/repos/microsoft/Winget-cli/releases/latest" -Method Get -ErrorAction Stop
            $wingetLatestVersion = [System.Version]::Parse(($response.tag_name).Trim('v')) #Stores version number of latest release.
            $wingetOutdated = $wingetCurrentVersion -lt $wingetLatestVersion
            Write-Host "===========================================" -ForegroundColor Green
            Write-Host "---        Winget is installed          ---" -ForegroundColor Green
            Write-Host "===========================================" -ForegroundColor Green
            Write-Host "Version: $wingetVersionFull" -ForegroundColor White

            if (!$wingetPreview) {
                Write-Host "    - Winget is a release version." -ForegroundColor Green
            } else {
                Write-Host "    - Winget is a preview version. Unexpected problems may occur." -ForegroundColor Yellow
            }

            if (!$wingetOutdated) {
                Write-Host "    - Winget is Up to Date" -ForegroundColor Green
                $status = "installed"
            } else {
                Write-Host "    - Winget is Out of Date" -ForegroundColor Red
                $status = "outdated"
            }
        } else {
            Write-Host "===========================================" -ForegroundColor Red
            Write-Host "---      Winget is not installed        ---" -ForegroundColor Red
            Write-Host "===========================================" -ForegroundColor Red
            $status = "not-installed"
        }
    }

    if ($choco) {
        if ((Get-Command -Name choco -ErrorAction Ignore) -and ($chocoVersion = (Get-Item "$env:ChocolateyInstall\choco.exe" -ErrorAction Ignore).VersionInfo.ProductVersion)) {
            Write-Host "===========================================" -ForegroundColor Green
            Write-Host "---      Chocolatey is installed        ---" -ForegroundColor Green
            Write-Host "===========================================" -ForegroundColor Green
            Write-Host "Version: v$chocoVersion" -ForegroundColor White
            $status = "installed"
        } else {
            Write-Host "===========================================" -ForegroundColor Red
            Write-Host "---    Chocolatey is not installed      ---" -ForegroundColor Red
            Write-Host "===========================================" -ForegroundColor Red
            $status = "not-installed"
        }
    }

    return $status
}

function Install-WinUtilWinget {
    <#

    .SYNOPSIS
        Installs Winget if it is not already installed.

    .DESCRIPTION
        This function will download the latest version of Winget and install it. If Winget is already installed, it will do nothing.
    #>
    $isWingetInstalled = Test-WinUtilPackageManager -winget

    try {
        if ($isWingetInstalled -eq "installed") {
            Write-Host "`nWinget is already installed.`r" -ForegroundColor Green
            return
        } elseif ($isWingetInstalled -eq "outdated") {
            Write-Host "`nWinget is Outdated. Continuing with install.`r" -ForegroundColor Yellow
        } else {
            Write-Host "`nWinget is not Installed. Continuing with install.`r" -ForegroundColor Red
        }


        # Gets the computer's information
        if ($null -eq $sync.ComputerInfo) {
            $ComputerInfo = Get-ComputerInfo -ErrorAction Stop
        } else {
            $ComputerInfo = $sync.ComputerInfo
        }

        if (($ComputerInfo.WindowsVersion) -lt "1809") {
            # Checks if Windows Version is too old for Winget
            Write-Host "Winget is not supported on this version of Windows (Pre-1809)" -ForegroundColor Red
            return
        }

        # Install Winget via GitHub method.
        # Used part of my own script with some modification: ruxunderscore/windows-initialization
        Write-Host "Downloading Winget Prerequsites`n"
        Get-WinUtilWingetPrerequisites
        Write-Host "Downloading Winget and License File`r"
        Get-WinUtilWingetLatest
        Write-Host "Installing Winget w/ Prerequsites`r"
        Add-AppxProvisionedPackage -Online -PackagePath $ENV:TEMP\Microsoft.DesktopAppInstaller.msixbundle -DependencyPackagePath $ENV:TEMP\Microsoft.VCLibs.x64.Desktop.appx, $ENV:TEMP\Microsoft.UI.Xaml.x64.appx -LicensePath $ENV:TEMP\License1.xml
        Write-Host "Manually adding Winget Sources, from Winget CDN."
        Add-AppxPackage -Path https://cdn.winget.microsoft.com/cache/source.msix #Seems some installs of Winget don't add the repo source, this should makes sure that it's installed every time.
        Write-Host "Winget Installed" -ForegroundColor Green
        Write-Host "Enabling NuGet and Module..."
        Install-PackageProvider -Name NuGet -Force
        Install-Module -Name Microsoft.WinGet.Client -Force
        # Winget only needs a refresh of the environment variables to be used.
        Write-Output "Refreshing Environment Variables...`n"
        $ENV:PATH = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    } catch {
        Write-Host "Failure detected while installing via GitHub method. Continuing with Chocolatey method as fallback." -ForegroundColor Red
        # In case install fails via GitHub method.
        try {
        # Install Choco if not already present
        Install-WinUtilChoco
        Start-Process -Verb runas -FilePath powershell.exe -ArgumentList "choco install winget-cli"
        Write-Host "Winget Installed" -ForegroundColor Green
        Write-Output "Refreshing Environment Variables...`n"
        $ENV:PATH = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        } catch {
            throw [WingetFailedInstall]::new('Failed to install!')
        }
    }

}

function Test-PythonInstalled {
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Microsoft") {
            return $false
        } else {
            return $true
        }
    } catch {
        return $false
    }
}

if (Test-PythonInstalled = $true) {
        Write-Host "Python is already installed"
} else {
    Write-Host "Python is not installed Installing Python..."
    Install-WinUtilWinget
    Start-Process -FilePath "winget" -ArgumentList "install Python.Python.3.12" -NoNewWindow -Wait
    Write-Host "Python is installed on this machine"
    $ENV:PATH = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}



if (Test-Path "$CUR_DIR\.virtualenv ") {
    Write-Host "Virtual Environment is Ready!"
}
else {
    Start-Process -FilePath "python" -ArgumentList "-m venv .virtualenv" -WorkingDirectory $CUR_DIR -NoNewWindow -Wait
    Get-Item .virtualenv -Force | Foreach-Object { $_.Attributes = $_. Attributes -bor "Hidden" }
}

$ENV_Python = "$CUR_DIR\.virtualenv\Scripts"
$CTRANSLATE_PATH = "$CUR_DIR\.virtualenv\Lib\site-packages\ctranslate2"

if ([System.IO.File]::Exists("$CUR_DIR\.virtualenv\done")) {
    Write-Host "Virtual Environment is already up."
    Write-Host "Running Scripts"
    Start-Process -FilePath "$ENV_Python\python.exe" -ArgumentList "$CUR_DIR\start.py" -WorkingDirectory $CUR_DIR -NoNewWindow -Wait
}

else {
    Write-Host "Installing Requirements"
    
    Start-Process -FilePath "$ENV_Python\python.exe" -ArgumentList "-m pip install --upgrade pip" -WorkingDirectory $CUR_DIR -NoNewWindow -Wait

    Start-Process -FilePath "$ENV_Python\python.exe" -ArgumentList "-m pip install -r $CUR_DIR\requirements.txt" -WorkingDirectory $CUR_DIR -NoNewWindow -Wait
    
    Clear-Host
   
    Write-Host "Setting Up CUDA."
    Write-Host "This might take a while."

    Invoke-WebRequest "https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_CUDA12_win_v1.7z" -OutFile "$CUR_DIR\cuBLAS.and.cuDNN_CUDA12_win_v1.7z"

    Invoke-WebRequest "https://www.7-zip.org/a/7zr.exe" -OutFile "$CUR_DIR\7zr.exe"

    Start-Process -FilePath "$CUR_DIR\7zr.exe" -ArgumentList "e $CUR_DIR\cuBLAS.and.cuDNN_CUDA12_win_v1.7z -o$CTRANSLATE_PATH" -WorkingDirectory $CUR_DIR -NoNewWindow -Wait

    Remove-Item "$CUR_DIR\cuBLAS.and.cuDNN_CUDA12_win_v1.7z"
    Remove-Item "$CUR_DIR\7zr.exe"

    Out-File "$CUR_DIR\.virtualenv\done"

    Start-Process -FilePath "$ENV_Python\python.exe" -ArgumentList "$CUR_DIR\start.py" -WorkingDirectory $CUR_DIR -NoNewWindow -Wait
}
