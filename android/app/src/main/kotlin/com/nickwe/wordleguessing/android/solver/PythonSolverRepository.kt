package com.nickwe.wordleguessing.android.solver

import android.app.Application
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class PythonSolverRepository private constructor(
    private val session: PyObject,
) : SolverRepository {
    override fun submitGuess(letters: List<String>, colors: List<String>): List<String> {
        return session.callAttr("submit_guess", letters, colors)
            .asList()
            .map { it.toString() }
    }

    override fun reset() {
        session.callAttr("reset")
    }

    companion object {
        fun create(application: Application): PythonSolverRepository {
            if (!Python.isStarted()) {
                Python.start(AndroidPlatform(application))
            }

            val bridge = Python.getInstance().getModule("source_code.solver_core.android_bridge")
            val session = bridge.callAttr("create_session")
            return PythonSolverRepository(session)
        }
    }
}
