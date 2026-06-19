package com.nickwe.wordleguessing.android.solver

data class SolverUiState(
    val tiles: List<TileState> = List(5) { TileState() },
    val candidates: List<String> = emptyList(),
    val hasSubmittedGuess: Boolean = false,
    val errorMessage: String? = null,
) {
    val isSubmitEnabled: Boolean
        get() = tiles.all { tile ->
            tile.letter.length == 1 && tile.letter[0].isLetter() && tile.color != TileColor.UNSET
        }

    val resultSummary: String
        get() = when {
            !hasSubmittedGuess -> "Results"
            candidates.size == 1 -> "1 candidate"
            else -> "${candidates.size} candidates"
        }
}
