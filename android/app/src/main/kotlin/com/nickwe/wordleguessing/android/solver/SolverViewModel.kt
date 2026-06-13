package com.nickwe.wordleguessing.android.solver

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class SolverViewModel(
    private val repository: SolverRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(SolverUiState())
    val uiState: StateFlow<SolverUiState> = _uiState.asStateFlow()

    fun updateLetter(index: Int, rawInput: String) {
        mutateTile(index) { tile ->
            tile.copy(letter = rawInput.filter { it.isLetter() }.takeLast(1).uppercase())
        }
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
        }.onFailure {
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
        }.onFailure {
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
        fun blankTiles(): List<TileState> = List(5) { TileState() }
    }
}
