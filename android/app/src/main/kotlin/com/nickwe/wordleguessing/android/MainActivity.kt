package com.nickwe.wordleguessing.android

import android.app.Application
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nickwe.wordleguessing.android.solver.SolverViewModel
import com.nickwe.wordleguessing.android.ui.WordleGuessingScreen
import com.nickwe.wordleguessing.android.ui.theme.WordleGuessingTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            WordleGuessingTheme {
                val viewModel = viewModel<SolverViewModel>(
                    factory = SolverViewModel.Factory(application as Application),
                )
                val uiState by viewModel.uiState.collectAsState()

                WordleGuessingScreen(
                    uiState = uiState,
                    onLetterChange = viewModel::updateLetter,
                    onColorClick = viewModel::cycleColor,
                    onSubmit = viewModel::submitGuess,
                    onClearRow = viewModel::clearRow,
                    onNewPuzzle = viewModel::newPuzzle,
                )
            }
        }
    }
}
