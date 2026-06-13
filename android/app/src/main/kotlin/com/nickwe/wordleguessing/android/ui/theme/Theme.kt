package com.nickwe.wordleguessing.android.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.ui.graphics.Color

private val LightColors = lightColorScheme(
    primary = Walnut,
    onPrimary = Sand,
    secondary = Clay,
    tertiary = Olive,
    background = Sand,
    onBackground = Walnut,
    surface = Color(0xFFFCFAF4),
    onSurface = Walnut,
    surfaceVariant = Wheat,
    onSurfaceVariant = Color(0xFF544C40),
    error = Brick,
)

private val DarkColors = darkColorScheme(
    primary = Sand,
    onPrimary = Walnut,
    secondary = Clay,
    tertiary = Olive,
    background = Color(0xFF1C1A17),
    onBackground = Sand,
    surface = Color(0xFF26231E),
    onSurface = Sand,
    surfaceVariant = Color(0xFF3A352C),
    onSurfaceVariant = Color(0xFFE1D7C3),
    error = Color(0xFFFFB4AB),
)

@Composable
fun WordleGuessingTheme(
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = if (isSystemInDarkTheme()) DarkColors else LightColors,
        typography = Typography(),
        content = content,
    )
}
