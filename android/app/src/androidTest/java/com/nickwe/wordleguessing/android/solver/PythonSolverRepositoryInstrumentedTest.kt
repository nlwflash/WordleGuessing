package com.nickwe.wordleguessing.android.solver

import android.app.Application
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class PythonSolverRepositoryInstrumentedTest {
    @Test
    fun submitGuess_allGreenCigar_returnsSingleCandidate() {
        val application = ApplicationProvider.getApplicationContext<Application>()
        val repository = PythonSolverRepository.create(application)

        val candidates = repository.submitGuess(
            letters = listOf("C", "I", "G", "A", "R"),
            colors = listOf("green", "green", "green", "green", "green"),
        )

        assertTrue("Expected at least one candidate", candidates.isNotEmpty())
        assertEquals(listOf("cigar"), candidates)
    }
}
