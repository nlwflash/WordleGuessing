# Android Release Guide

This project can ship a manually installed Android APK without Play Store distribution.

## Release Files

- `android/version.properties`: committed Android version source of truth
- `android/keystore.properties`: local signing config, never committed
- `android/signing/wordleguessing-release.jks`: local signing key, never committed

## Supported Devices

The current APK targets modern Android phones with `minSdk 24` and includes `arm64-v8a` for
real devices plus `x86_64` for emulator coverage. That comfortably covers devices in the Galaxy
S22 and newer / recent Pixel class.

## Release Checklist

1. Update `android/version.properties` and increment both `VERSION_CODE` and `VERSION_NAME`.
2. From the repo root, make sure the local Python environment is ready:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest -q
   ```

3. From `android/`, run the Android checks:

   ```powershell
   .\gradlew.bat testDebugUnitTest
   .\gradlew.bat connectedAndroidTest
   .\gradlew.bat assembleRelease
   ```

4. Share `android\app\build\outputs\apk\release\app-release.apk`.
5. Generate a checksum alongside the APK before sending it:

   ```powershell
   Get-FileHash .\app\build\outputs\apk\release\app-release.apk -Algorithm SHA256
   ```

## Signing Notes

- Keep the release keystore backed up outside the repo. If it is lost, future updates cannot be
  installed over the old signed builds.
- `android/keystore.properties.example` shows the expected config shape.
- A release APK signed with the release keystore will not install over an existing debug build
  signed by the default Android debug key. Uninstall the debug app first, or intentionally sign
  debug and release with the same long-lived key.

## Backup And APK Packaging

- `android:allowBackup="true"` lets Android back up and restore app data during device transfer
  or cloud restore. This app currently stores little or no sensitive local data, so leaving it on
  is acceptable. If you want every install to start completely fresh with no restored state, set
  it to `false`.
- A universal APK bundles every included native ABI into one file. That makes sharing easier
  because one APK works on both the target phone and the emulator, but it is larger. For this
  project, the current universal APK includes `arm64-v8a` plus `x86_64`.
