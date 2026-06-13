# Android Prototype

This repo now contains an Android client scaffold in `android/` which keeps the existing desktop
Tkinter app intact and reuses the shared Python solver through Chaquopy.

## What It Includes

- A native Jetpack Compose single-screen solver UI
- A Kotlin `ViewModel` and repository layer for Android state management
- A Chaquopy-backed bridge into `source_code.solver_core.android_bridge`
- Android unit coverage for the `ViewModel`
- An instrumentation happy-path test for the Compose UI

## Local Prerequisites

Install these locally before building the Android app:

1. JDK 17
2. Android Studio or the Android SDK command-line tooling
3. A repo-local Python 3.12 virtual environment at `.venv`

The Android Gradle module is configured to use `.venv\Scripts\python.exe` on Windows and
`.venv/bin/python` on non-Windows platforms when those paths exist.

## Python Environment

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

The shared solver tests can still be run from the repo root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m mypy
```

## Android Build Notes

If `android/` does not already contain a Gradle wrapper on your machine, generate it after
installing Gradle or by opening the project in Android Studio:

```powershell
cd .\android
gradle wrapper
```

Then build or test from `android/`:

```powershell
.\gradlew.bat assembleDebug
.\gradlew.bat test
.\gradlew.bat connectedAndroidTest
```

## Implementation Notes

- The Android app starts Python in `WordleGuessingApplication`.
- The Android repository calls `create_session()` from the Python bridge and then invokes
  `submit_guess` and `reset` on the returned session object.
- The Chaquopy source set points at the repo root so the Android app can import the shared
  `source_code` package, while excluding the desktop-only Tkinter UI and repo-local tooling
  directories.
