import unittest
from src.body_analyzer.analisis_completo import informe_completo


class TestInformeCompleto(unittest.TestCase):
    def test_informe_completo_exitoso_hombre(self):
        data = {
            "peso": 75,
            "altura": 180,
            "edad": 30,
            "genero": "h",
            "cuello": 40,
            "cintura": 90,
        }
        resultado = informe_completo(data)

        self.assertIn("resultados", resultado)
        self.assertIn("interpretaciones", resultado)
        self.assertEqual(len(resultado["resultados"]), 8)
        self.assertEqual(len(resultado["interpretaciones"]), 5)
        self.assertNotIn("error", resultado)

    def test_informe_completo_exitoso_mujer(self):
        data = {
            "peso": 63,
            "altura": 170,
            "edad": 22,
            "genero": "m",
            "cuello": 32,
            "cintura": 76,
            "cadera": 100,
            "objetivo": 'perder grasa'
        }
        resultado = informe_completo(data)

        self.assertIn("resultados", resultado)
        self.assertIn("interpretaciones", resultado)
        self.assertEqual(len(resultado["resultados"]), 8)
        self.assertEqual(len(resultado["interpretaciones"]), 5)
        self.assertNotIn("error", resultado)

    def test_faltan_parametros_obligatorios(self):
        data = {
            "peso": 75,
            "altura": 180,
            "genero": "h",
        }
        resultado = informe_completo(data)

        self.assertIn("error", resultado)
        self.assertEqual(resultado["error"], "Falta el parámetro obligatorio: edad")

    def test_genero_invalido(self):
        data = {
            "peso": 75,
            "altura": 180,
            "edad": 30,
            "genero": "x",
            "cuello": 40,
            "cintura": 90,
        }
        resultado = informe_completo(data)

        self.assertIn("error", resultado)
        self.assertEqual(
            resultado["error"], "Para mujeres, la cadera debe ser especificada."
        )

    def test_peso_invalido(self):
        data = {
            "peso": -75,
            "altura": 180,
            "edad": 30,
            "genero": "h",
            "cuello": 40,
            "cintura": 90,
        }
        resultado = informe_completo(data)

        self.assertIn("error", resultado)
        self.assertEqual(resultado["error"], "'peso' debe ser un int, float positivo.")

    def test_altura_invalida(self):
        data = {
            "peso": 75,
            "altura": -180,
            "edad": 30,
            "genero": "h",
            "cuello": 40,
            "cintura": 90,
        }
        resultado = informe_completo(data)

        self.assertIn("error", resultado)
        self.assertEqual(
            resultado["error"], "'altura' debe ser un int, float positivo."
        )

    def test_edad_invalida(self):
        data = {
            "peso": 75,
            "altura": 180,
            "edad": -30,
            "genero": "h",
            "cuello": 40,
            "cintura": 90,
        }
        resultado = informe_completo(data)

        self.assertIn("error", resultado)
        self.assertEqual(resultado["error"], "'edad' debe ser un int positivo.")

    def test_faltan_parametros_para_mujer(self):
        data = {
            "peso": 65,
            "altura": 165,
            "edad": 28,
            "genero": "m",
            "cuello": 35,
            "cintura": 70,
        }
        resultado = informe_completo(data)

        self.assertIn("error", resultado)
        self.assertEqual(
            resultado["error"],
            "'cadera' debe ser un int, float positivo.",
        )

    def test_parametros_correctos_para_mujer(self):
        data = {
            "peso": 65,
            "altura": 165,
            "edad": 28,
            "genero": "m",
            "cuello": 35,
            "cintura": 70,
            "cadera": 95,
        }
        resultado = informe_completo(data)

        self.assertIn("resultados", resultado)
        self.assertEqual(resultado["resultados"]["rcc"], 0.74)  # Testea el valor RCC
