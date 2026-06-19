package com.nickwe.wordleguessing.android

import android.app.Application
import androidx.compose.ui.test.assertIsEnabled
import androidx.compose.ui.test.assertTextEquals
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextReplacement
import com.nickwe.wordleguessing.android.solver.SolverRepository
import com.nickwe.wordleguessing.android.solver.SolverRepositoryProvider
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain
import org.junit.rules.TestRule
import org.junit.runners.model.Statement

class WordleGuessingHappyPathTest {
    private val fakeRepository = FakeSolverRepository()
    private val repositoryRule = TestRule { base, _ ->
        object : Statement() {
            override fun evaluate() {
                val originalFactory = SolverRepositoryProvider.factory
                SolverRepositoryProvider.factory = { _: Application -> fakeRepository }
                try {
                    base.evaluate()
                } finally {
                    SolverRepositoryProvider.factory = originalFactory
                }
            }
        }
    }
    private val composeRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val ruleChain: RuleChain = RuleChain.outerRule(repositoryRule).around(composeRule)

    @Test
    fun allGreenGuessShowsSingleCandidateAndNewPuzzleClearsResults() {
        "cigar".forEachIndexed { index, char ->
            composeRule.onNodeWithTag("letter_input_$index").performTextReplacement(char.toString())
            repeat(3) {
                composeRule.onNodeWithTag("color_button_$index").performClick()
            }
        }

        composeRule.onNodeWithTag("submit_button").assertIsEnabled().performClick()
        composeRule.waitUntil(timeoutMillis = 10_000) {
            composeRule.onAllNodesWithTag("candidate_item_cigar").fetchSemanticsNodes().isNotEmpty()
        }
        composeRule.onNodeWithTag("result_count").assertTextEquals("1 candidate")
        composeRule.onNodeWithTag("candidate_item_cigar").assertTextEquals("cigar")

        composeRule.onNodeWithTag("new_puzzle_button").performClick()
        composeRule.waitUntil(timeoutMillis = 10_000) {
            composeRule.onAllNodesWithTag("empty_results_text").fetchSemanticsNodes().isNotEmpty()
        }
        composeRule.onNodeWithTag("result_count").assertTextEquals("Results")
        composeRule.onNodeWithTag("empty_results_text").assertTextEquals("Enter a guess to see matching words.")
    }
}

private class FakeSolverRepository : SolverRepository {
    override fun submitGuess(letters: List<String>, colors: List<String>): List<String> {
        return if (letters.joinToString(separator = "").lowercase() == "cigar" && colors.all { it == "green" }) {
            listOf("cigar")
        } else {
            emptyList()
        }
    }

    override fun reset() = Unit
}
