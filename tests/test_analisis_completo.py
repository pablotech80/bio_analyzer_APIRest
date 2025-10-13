import unittest

from werkzeug.datastructures import MultiDict

from app.blueprints.bioanalyze.services import (AnalysisValidationError,
                                                run_biometric_analysis)


class TestRunBiometricAnalysis(unittest.TestCase):

    def test_run_biometric_analysis_success(self):
        form = MultiDict(
            {
                "peso": "80",
                "altura": "180",
                "edad": "32",
                "genero": "h",
                "cuello": "40",
                "cintura": "90",
                "factor_actividad": "1.55",
                "objetivo": "mantener peso",
                "nivel": "saludable",
            }
        )

        payload = run_biometric_analysis(form)

        self.assertIn("tmb", payload.results)
        self.assertIn("imc", payload.results)
        self.assertEqual(payload.inputs["genero"], "h")
        self.assertAlmostEqual(payload.results["imc"], 24.69, places=2)

    def test_run_biometric_analysis_missing_field(self):
        form = MultiDict({"peso": "80"})
        with self.assertRaises(AnalysisValidationError):
            run_biometric_analysis(form)


if __name__ == "__main__":
    unittest.main()
