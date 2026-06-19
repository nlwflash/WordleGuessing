package com.nickwe.wordleguessing.android.solver

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class SolverViewModelTest {
    @Test
    fun submitEnabledOnlyWhenAllTilesHaveLettersAndColors() {
        val viewModel = SolverViewModel(FakeSolverRepository())

        repeat(5) { index ->
            viewModel.updateLetter(index, "a")
        }
        assertFalse(viewModel.uiState.value.isSubmitEnabled)

        repeat(5) { index ->
            viewModel.cycleColor(index)
        }
        assertTrue(viewModel.uiState.value.isSubmitEnabled)
    }

    @Test
    fun updateLetterDistributesPastedGuessAcrossEmptyTiles() {
        val viewModel = SolverViewModel(FakeSolverRepository())

        viewModel.updateLetter(0, "cigar")

        assertEquals(listOf("C", "I", "G", "A", "R"), viewModel.uiState.value.tiles.map { it.letter })
    }

    @Test
    fun deletingFilledTileClearsItAndMovesFocusBackward() {
        val viewModel = SolverViewModel(FakeSolverRepository())

        viewModel.updateLetter(0, "c")
        viewModel.updateLetter(1, "i")
        val focusTarget = viewModel.updateLetter(1, "")

        assertEquals(0, focusTarget)
        assertEquals(listOf("C", "", "", "", ""), viewModel.uiState.value.tiles.map { it.letter })
    }

    @Test
    fun backspaceFromEmptyTileClearsNearestPreviousLetter() {
        val viewModel = SolverViewModel(FakeSolverRepository())

        viewModel.updateLetter(0, "c")
        viewModel.updateLetter(1, "i")
        val focusTarget = viewModel.handleBackspace(2)

        assertEquals(1, focusTarget)
        assertEquals(listOf("C", "", "", "", ""), viewModel.uiState.value.tiles.map { it.letter })
    }

    @Test
    fun submitGuessUpdatesCandidatesAndClearsTheRow() {
        val repository = FakeSolverRepository(candidates = listOf("cigar"))
        val viewModel = SolverViewModel(repository)

        seedCompleteRow(viewModel, "cigar")
        viewModel.submitGuess()

        assertEquals(listOf("cigar"), viewModel.uiState.value.candidates)
        assertTrue(viewModel.uiState.value.hasSubmittedGuess)
        assertEquals(SolverViewModel.blankTiles(), viewModel.uiState.value.tiles)
        assertNull(viewModel.uiState.value.errorMessage)
        assertEquals(listOf("C", "I", "G", "A", "R"), repository.lastLetters)
        assertEquals(listOf("green", "green", "green", "green", "green"), repository.lastColors)
    }

    @Test
    fun newPuzzleResetsRepositoryAndClearsResults() {
        val repository = FakeSolverRepository(candidates = listOf("cigar"))
        val viewModel = SolverViewModel(repository)

        seedCompleteRow(viewModel, "cigar")
        viewModel.submitGuess()
        viewModel.newPuzzle()

        assertEquals(1, repository.resetCalls)
        assertFalse(viewModel.uiState.value.hasSubmittedGuess)
        assertTrue(viewModel.uiState.value.candidates.isEmpty())
        assertEquals(SolverViewModel.blankTiles(), viewModel.uiState.value.tiles)
    }

    @Test
    fun submitGuessSurfacesRepositoryFailure() {
        val viewModel = SolverViewModel(FakeSolverRepository(throwOnSubmit = true))

        seedCompleteRow(viewModel, "cigar")
        viewModel.submitGuess()

        assertEquals("Unable to process guess right now.", viewModel.uiState.value.errorMessage)
        assertTrue(viewModel.uiState.value.candidates.isEmpty())
    }

    private fun seedCompleteRow(viewModel: SolverViewModel, word: String) {
        word.forEachIndexed { index, char ->
            viewModel.updateLetter(index, char.toString())
            repeat(3) {
                viewModel.cycleColor(index)
            }
        }
    }

    private class FakeSolverRepository(
        private val candidates: List<String> = emptyList(),
        private val throwOnSubmit: Boolean = false,
    ) : SolverRepository {
        var lastLetters: List<String> = emptyList()
        var lastColors: List<String> = emptyList()
        var resetCalls: Int = 0

        override fun submitGuess(letters: List<String>, colors: List<String>): List<String> {
            if (throwOnSubmit) {
                throw IllegalStateException("boom")
            }

            lastLetters = letters
            lastColors = colors
            return candidates
        }

        override fun reset() {
            resetCalls += 1
        }
    }
}
