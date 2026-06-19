package com.nickwe.wordleguessing.android.solver

import android.app.Application

object SolverRepositoryProvider {
    var factory: (Application) -> SolverRepository = { application ->
        PythonSolverRepository.create(application)
    }
}
