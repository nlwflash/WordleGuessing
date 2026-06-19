package com.nickwe.wordleguessing.android.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.text.KeyboardActions
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
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.nickwe.wordleguessing.android.solver.SolverUiState
import com.nickwe.wordleguessing.android.solver.TileColor
import com.nickwe.wordleguessing.android.solver.TileState

@Composable
fun WordleGuessingScreen(
    uiState: SolverUiState,
    onLetterChange: (Int, String) -> Int?,
    onColorClick: (Int) -> Unit,
    onSubmit: () -> Unit,
    onClearRow: () -> Unit,
    onNewPuzzle: () -> Unit,
) {
    val focusManager = LocalFocusManager.current
    val focusRequesters = remember { List(5) { FocusRequester() } }

    Surface(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .safeDrawingPadding()
                .imePadding()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(
                    text = "Wordle Guessing Assistant",
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    text = "Type one guess, tap each color until it matches the clue, and keep narrowing the list offline.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            Card {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp),
                ) {
                    Text(
                        text = "Current Guess",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        text = "Letter focus advances automatically. You can also paste into an empty tile to fill the row.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        uiState.tiles.forEachIndexed { index, tile ->
                            GuessTileEditor(
                                modifier = Modifier.weight(1f),
                                index = index,
                                tile = tile,
                                focusRequester = focusRequesters[index],
                                isLastTile = index == uiState.tiles.lastIndex,
                                onLetterChange = { rawInput ->
                                    val hasLetterInput = rawInput.any { it.isLetter() }
                                    val nextFocusIndex = onLetterChange(index, rawInput)
                                    when {
                                        nextFocusIndex != null -> focusRequesters[nextFocusIndex].requestFocus()
                                        hasLetterInput -> focusManager.clearFocus()
                                    }
                                },
                                onColorClick = {
                                    focusManager.clearFocus()
                                    onColorClick(index)
                                },
                                onMoveNext = {
                                    if (index < focusRequesters.lastIndex) {
                                        focusRequesters[index + 1].requestFocus()
                                    } else {
                                        focusManager.clearFocus()
                                    }
                                },
                                onDone = { focusManager.clearFocus() },
                            )
                        }
                    }

                    Button(
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 52.dp)
                            .testTag("submit_button"),
                        enabled = uiState.isSubmitEnabled,
                        onClick = {
                            focusManager.clearFocus()
                            onSubmit()
                        },
                    ) {
                        Text("Submit Guess")
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        FilledTonalButton(
                            modifier = Modifier
                                .weight(1f)
                                .heightIn(min = 48.dp)
                                .testTag("clear_row_button"),
                            onClick = {
                                focusManager.clearFocus()
                                onClearRow()
                            },
                        ) {
                            Text("Clear Row")
                        }

                        FilledTonalButton(
                            modifier = Modifier
                                .weight(1f)
                                .heightIn(min = 48.dp)
                                .testTag("new_puzzle_button"),
                            onClick = {
                                focusManager.clearFocus()
                                onNewPuzzle()
                            },
                        ) {
                            Text("New Puzzle")
                        }
                    }
                }
            }

            uiState.errorMessage?.let { message ->
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer,
                    ),
                ) {
                    Text(
                        text = message,
                        modifier = Modifier.fillMaxWidth().padding(12.dp),
                        color = MaterialTheme.colorScheme.onErrorContainer,
                        style = MaterialTheme.typography.bodyMedium,
                    )
                }
            }

            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    Text(
                        text = uiState.resultSummary,
                        modifier = Modifier.testTag("result_count"),
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                    )

                    when {
                        !uiState.hasSubmittedGuess -> {
                            EmptyResultsState(
                                text = "Enter a guess to see matching words.",
                            )
                        }

                        uiState.candidates.isEmpty() -> {
                            EmptyResultsState(
                                text = "No candidate words remain.",
                            )
                        }

                        else -> {
                            LazyVerticalGrid(
                                modifier = Modifier.fillMaxSize(),
                                columns = GridCells.Adaptive(minSize = 88.dp),
                                horizontalArrangement = Arrangement.spacedBy(10.dp),
                                verticalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                items(uiState.candidates, key = { it }) { candidate ->
                                    Card(
                                        modifier = Modifier.fillMaxWidth(),
                                        colors = CardDefaults.cardColors(
                                            containerColor = MaterialTheme.colorScheme.surfaceVariant,
                                        ),
                                    ) {
                                        Text(
                                            text = candidate,
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .padding(horizontal = 10.dp, vertical = 12.dp)
                                                .testTag("candidate_item_$candidate"),
                                            textAlign = TextAlign.Center,
                                            style = MaterialTheme.typography.bodyLarge,
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun EmptyResultsState(text: String) {
    Box(
        modifier = Modifier
            .fillMaxSize(),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = text,
            modifier = Modifier.testTag("empty_results_text"),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
            style = MaterialTheme.typography.bodyMedium,
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun GuessTileEditor(
    modifier: Modifier = Modifier,
    index: Int,
    tile: TileState,
    focusRequester: FocusRequester,
    isLastTile: Boolean,
    onLetterChange: (String) -> Unit,
    onColorClick: () -> Unit,
    onMoveNext: () -> Unit,
    onDone: () -> Unit,
) {
    val palette = tilePalette(tile.color)
    Column(
        modifier = modifier.widthIn(min = 56.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        OutlinedTextField(
            value = tile.letter,
            onValueChange = onLetterChange,
            modifier = Modifier
                .fillMaxWidth()
                .height(80.dp)
                .focusRequester(focusRequester)
                .testTag("letter_input_$index"),
            singleLine = true,
            textStyle = MaterialTheme.typography.headlineSmall.copy(
                textAlign = TextAlign.Center,
                fontWeight = FontWeight.Bold,
            ),
            keyboardOptions = KeyboardOptions(
                capitalization = KeyboardCapitalization.Characters,
                keyboardType = KeyboardType.Text,
                imeAction = if (isLastTile) ImeAction.Done else ImeAction.Next,
            ),
            keyboardActions = KeyboardActions(
                onNext = { onMoveNext() },
                onDone = { onDone() },
            ),
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
                .heightIn(min = 48.dp)
                .testTag("color_button_$index"),
            onClick = onColorClick,
            colors = ButtonDefaults.filledTonalButtonColors(
                containerColor = palette.containerColor,
                contentColor = palette.contentColor,
            ),
        ) {
            Text(
                text = tile.color.label,
                maxLines = 1,
                style = MaterialTheme.typography.labelLarge,
            )
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
