package com.nickwe.wordleguessing.android.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.nickwe.wordleguessing.android.solver.SolverUiState
import com.nickwe.wordleguessing.android.solver.TileColor
import com.nickwe.wordleguessing.android.solver.TileState

@Composable
fun WordleGuessingScreen(
    uiState: SolverUiState,
    onLetterChange: (Int, String) -> Unit,
    onColorClick: (Int) -> Unit,
    onSubmit: () -> Unit,
    onClearRow: () -> Unit,
    onNewPuzzle: () -> Unit,
) {
    Surface(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = "Wordle Guessing Assistant",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                    )
                    Text(
                        text = "Enter one five-letter guess, tap each tile color, then submit to narrow the remaining candidates offline.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }

            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    uiState.tiles.forEachIndexed { index, tile ->
                        GuessTileEditor(
                            modifier = Modifier.weight(1f),
                            index = index,
                            tile = tile,
                            onLetterChange = onLetterChange,
                            onColorClick = onColorClick,
                        )
                    }
                }
            }

            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Button(
                        modifier = Modifier
                            .weight(1f)
                            .testTag("submit_button"),
                        enabled = uiState.isSubmitEnabled,
                        onClick = onSubmit,
                    ) {
                        Text("Submit Guess")
                    }

                    FilledTonalButton(
                        modifier = Modifier
                            .weight(1f)
                            .testTag("clear_row_button"),
                        onClick = onClearRow,
                    ) {
                        Text("Clear Row")
                    }

                    FilledTonalButton(
                        modifier = Modifier
                            .weight(1f)
                            .testTag("new_puzzle_button"),
                        onClick = onNewPuzzle,
                    ) {
                        Text("New Puzzle")
                    }
                }
            }

            uiState.errorMessage?.let { message ->
                item {
                    Text(
                        text = message,
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodyMedium,
                    )
                }
            }

            item {
                Text(
                    text = uiState.resultSummary,
                    modifier = Modifier.testTag("result_count"),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                )
            }

            if (!uiState.hasSubmittedGuess) {
                item {
                    Text(
                        text = "Enter a guess to see matching words.",
                        modifier = Modifier.testTag("empty_results_text"),
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            } else if (uiState.candidates.isEmpty()) {
                item {
                    Text(
                        text = "No candidate words remain.",
                        modifier = Modifier.testTag("empty_results_text"),
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            } else {
                items(uiState.candidates, key = { it }) { candidate ->
                    Card(
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant,
                        ),
                    ) {
                        Text(
                            text = candidate,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 12.dp)
                                .testTag("candidate_item_$candidate"),
                            style = MaterialTheme.typography.bodyLarge,
                        )
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun GuessTileEditor(
    modifier: Modifier = Modifier,
    index: Int,
    tile: TileState,
    onLetterChange: (Int, String) -> Unit,
    onColorClick: (Int) -> Unit,
) {
    val palette = tilePalette(tile.color)
    Column(
        modifier = modifier.widthIn(min = 56.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        OutlinedTextField(
            value = tile.letter,
            onValueChange = { onLetterChange(index, it) },
            modifier = Modifier
                .fillMaxWidth()
                .testTag("letter_input_$index"),
            singleLine = true,
            textStyle = MaterialTheme.typography.titleLarge.copy(textAlign = TextAlign.Center),
            keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Characters),
            colors = OutlinedTextFieldDefaults.colors(
                focusedTextColor = palette.contentColor,
                unfocusedTextColor = palette.contentColor,
                focusedContainerColor = palette.containerColor,
                unfocusedContainerColor = palette.containerColor,
                focusedBorderColor = palette.borderColor,
                unfocusedBorderColor = palette.borderColor,
            ),
        )

        FilledTonalButton(
            modifier = Modifier
                .fillMaxWidth()
                .testTag("color_button_$index"),
            onClick = { onColorClick(index) },
            colors = ButtonDefaults.filledTonalButtonColors(
                containerColor = palette.containerColor,
                contentColor = palette.contentColor,
            ),
        ) {
            Text(tile.color.label)
        }
    }
}

private fun tilePalette(tileColor: TileColor): TilePalette = when (tileColor) {
    TileColor.UNSET -> TilePalette(
        containerColor = Color(0xFFF8F5EE),
        contentColor = Color(0xFF1F2937),
        borderColor = Color(0xFF9F9687),
    )
    TileColor.GRAY -> TilePalette(
        containerColor = Color(0xFF787C7E),
        contentColor = Color.White,
        borderColor = Color(0xFF5A5D5E),
    )
    TileColor.YELLOW -> TilePalette(
        containerColor = Color(0xFFC9B458),
        contentColor = Color.White,
        borderColor = Color(0xFFA58F39),
    )
    TileColor.GREEN -> TilePalette(
        containerColor = Color(0xFF6AAA64),
        contentColor = Color.White,
        borderColor = Color(0xFF5A8E55),
    )
}

private data class TilePalette(
    val containerColor: Color,
    val contentColor: Color,
    val borderColor: Color,
)
