package com.nickwe.wordleguessing.android.solver

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import java.util.logging.Level
import java.util.logging.Logger
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class SolverViewModel(
    private val repository: SolverRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(SolverUiState())
    val uiState: StateFlow<SolverUiState> = _uiState.asStateFlow()

    fun updateLetter(index: Int, rawInput: String): Int? {
        val current = _uiState.value
        if (index !in current.tiles.indices) {
            return null
        }

        val normalizedInput = rawInput.filter { it.isLetter() }.uppercase()
        val updatedTiles = current.tiles.toMutableList()
        val nextFocusIndex = if (normalizedInput.length > 1 && current.tiles[index].letter.isEmpty()) {
            val insertedLetters = normalizedInput.take(updatedTiles.size - index)
            insertedLetters.forEachIndexed { offset, char ->
                updatedTiles[index + offset] = updatedTiles[index + offset].copy(letter = char.toString())
            }
            (index + insertedLetters.length).takeIf { it in updatedTiles.indices }
        } else {
            val normalizedLetter = normalizedInput.takeLast(1)
            val isDeletingFilledTile = normalizedLetter.isEmpty() && current.tiles[index].letter.isNotEmpty()
            updatedTiles[index] = updatedTiles[index].copy(letter = normalizedLetter)
            when {
                isDeletingFilledTile -> (index - 1).takeIf { it >= 0 }
                normalizedLetter.isNotEmpty() && index < updatedTiles.lastIndex -> index + 1
                else -> null
            }
        }

        _uiState.value = current.copy(
            tiles = updatedTiles,
            errorMessage = null,
        )
        return nextFocusIndex
    }

    fun handleBackspace(index: Int): Int? {
        val current = _uiState.value
        if (index !in current.tiles.indices) {
            return null
        }

        val updatedTiles = current.tiles.toMutableList()
        val focusTarget = if (current.tiles[index].letter.isNotEmpty()) {
            updatedTiles[index] = updatedTiles[index].copy(letter = "")
            (index - 1).takeIf { it >= 0 }
        } else {
            val previousFilledIndex = (index - 1 downTo 0)
                .firstOrNull { current.tiles[it].letter.isNotEmpty() }
                ?: return null
            updatedTiles[previousFilledIndex] = updatedTiles[previousFilledIndex].copy(letter = "")
            previousFilledIndex
        }

        _uiState.value = current.copy(
            tiles = updatedTiles,
            errorMessage = null,
        )
        return focusTarget
    }

    fun cycleColor(index: Int) {
        mutateTile(index) { tile -> tile.copy(color = tile.color.next()) }
    }

    fun clearRow() {
        _uiState.value = _uiState.value.copy(
            tiles = blankTiles(),
            errorMessage = null,
        )
    }

    fun submitGuess() {
        val current = _uiState.value
        if (!current.isSubmitEnabled) {
            _uiState.value = current.copy(
                errorMessage = "Enter one letter and one color in all five tiles.",
            )
            return
        }

        val letters = current.tiles.map { it.letter }
        val colors = current.tiles.map { it.color.pythonValue }
        runCatching {
            repository.submitGuess(letters, colors)
        }.onSuccess { candidates ->
            _uiState.value = current.copy(
                tiles = blankTiles(),
                candidates = candidates,
                hasSubmittedGuess = true,
                errorMessage = null,
            )
        }.onFailure { error ->
            LOGGER.log(Level.SEVERE, "submitGuess failed", error)
            _uiState.value = current.copy(
                errorMessage = "Unable to process guess right now.",
            )
        }
    }

    fun newPuzzle() {
        val current = _uiState.value
        runCatching {
            repository.reset()
        }.onSuccess {
            _uiState.value = SolverUiState()
        }.onFailure { error ->
            LOGGER.log(Level.SEVERE, "newPuzzle failed", error)
            _uiState.value = current.copy(
                errorMessage = "Unable to start a new puzzle right now.",
            )
        }
    }

    private fun mutateTile(index: Int, update: (TileState) -> TileState) {
        val current = _uiState.value
        if (index !in current.tiles.indices) {
            return
        }

        val updatedTiles = current.tiles.toMutableList()
        updatedTiles[index] = update(updatedTiles[index])
        _uiState.value = current.copy(
            tiles = updatedTiles,
            errorMessage = null,
        )
    }

    class Factory(
        private val application: Application,
    ) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            require(modelClass.isAssignableFrom(SolverViewModel::class.java)) {
                "Unsupported ViewModel class: ${modelClass.name}"
            }

            return SolverViewModel(SolverRepositoryProvider.factory(application)) as T
        }
    }

    companion object {
        private val LOGGER: Logger = Logger.getLogger(SolverViewModel::class.java.name)

        fun blankTiles(): List<TileState> = List(5) { TileState() }
    }
}
