package com.nickwe.wordleguessing.android.solver

interface SolverRepository {
    fun submitGuess(letters: List<String>, colors: List<String>): List<String>

    fun reset()
}
