package com.nickwe.wordleguessing.android.solver

data class TileState(
    val letter: String = "",
    val color: TileColor = TileColor.UNSET,
)
