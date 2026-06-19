# AGENTS.md

## Repository Guidance

- Read `docs/android-release.md` before making Android release or APK distribution changes.
- Treat `android/version.properties` as the source of truth for Android `VERSION_CODE` and `VERSION_NAME`.
- Bump both Android version values for every new shared release build.
- Never commit `android/keystore.properties` or private key material under `android/signing/`.
- Before wrapping up Android release work, run from `android/`: `.\gradlew.bat testDebugUnitTest connectedAndroidTest assembleRelease`.
- Keep desktop packaging unchanged during Android-only work unless the user explicitly asks for cross-platform release changes.
