; Ahim PDF Reader Installer Script
!define APP_NAME "Ahim PDF Reader"
!define COMP_NAME "Ahim Studio"
!define VERSION "1.0.0"
!define EXE_NAME "AhimPDFReader.exe"
!define ICON_PATH "assets\icon.ico"

Name "${APP_NAME}"
OutFile "dist\AhimPDFReader_Installer_v${VERSION}.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
Icon "${ICON_PATH}"

Page directory
Page instfiles

Section "Install"
    SetOutPath "$INSTDIR"
    File "dist\${EXE_NAME}"
    File "assets\icon.ico"
    File "assets\icon.png"

    ; Create Shortcuts
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}" "" "$INSTDIR\icon.ico"
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}" "" "$INSTDIR\icon.ico"
    
    ; Registry for uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\${EXE_NAME}"
    Delete "$INSTDIR\icon.ico"
    Delete "$INSTDIR\icon.png"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
    
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
SectionEnd
