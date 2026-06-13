package com.nickwe.wordleguessing.android

import androidx.compose.ui.test.assertExists
import androidx.compose.ui.test.assertTextEquals
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextInput
import org.junit.Rule
import org.junit.Test

class WordleGuessingHappyPathTest {
    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun allGreenGuessShowsSingleCandidateAndNewPuzzleClearsResults() {
        "cigar".forEachIndexed { index, char ->
            composeRule.onNodeWithTag("letter_input_$index").performTextInput(char.toString())
            repeat(3) {
                composeRule.onNodeWithTag("color_button_$index").performClick()
            }
        }

        composeRule.onNodeWithTag("submit_button").performClick()
        composeRule.onNodeWithTag("result_count").assertTextEquals("1 candidate")
        composeRule.onNodeWithTag("candidate_item_cigar").assertExists()

        composeRule.onNodeWithTag("new_puzzle_button").performClick()
        composeRule.onNodeWithTag("result_count").assertTextEquals("Results")
        composeRule.onNodeWithTag("empty_results_text").assertExists()
    }
}
