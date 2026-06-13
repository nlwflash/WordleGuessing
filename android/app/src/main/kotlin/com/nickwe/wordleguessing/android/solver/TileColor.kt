package com.nickwe.wordleguessing.android.solver

enum class TileColor(
    val pythonValue: String,
    val label: String,
) {
    UNSET("", "Unset"),
    GRAY("gray", "Gray"),
    YELLOW("yellow", "Yellow"),
    GREEN("green", "Green"),
    ;

    fun next(): TileColor = entries[(ordinal + 1) % entries.size]
}
