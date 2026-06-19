import java.util.Locale

plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.kotlinAndroid)
    alias(libs.plugins.chaquopy)
}

val repoVenvPython = if (System.getProperty("os.name").lowercase(Locale.ROOT).contains("windows")) {
    "../../.venv/Scripts/python.exe"
} else {
    "../../.venv/bin/python"
}

android {
    namespace = "com.nickwe.wordleguessing.android"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.nickwe.wordleguessing.android"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = libs.versions.composeCompiler.get()
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

chaquopy {
    defaultConfig {
        version = "3.12"

        // Reuse the repo-local virtualenv whenever it exists so Android builds do not
        // depend on a globally configured Python interpreter.
        if (file(repoVenvPython).exists()) {
            buildPython(repoVenvPython)
        }
    }

    sourceSets {
        getByName("main") {
            // Point at the repo root so Android can import the shared `source_code` package.
            srcDir("../..")
            exclude(".git/**")
            exclude(".mypy_cache/**")
            exclude(".ruff_cache/**")
            exclude(".venv/**")
            exclude("WordleGuessing.egg-info/**")
            exclude("android/**")
            exclude("docs/**")
            exclude("packaging/**")
            exclude("release/**")
            exclude("scripts/**")
            exclude("test/**")
            exclude("source_code/app.py")
            exclude("source_code/__main__.py")
            exclude("source_code/application/**")
            exclude("source_code/presentation/**")
        }
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
    implementation(libs.google.material)

    testImplementation(libs.junit4)

    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)

    debugImplementation(libs.androidx.compose.ui.tooling)
    debugImplementation(libs.androidx.compose.ui.test.manifest)
}
