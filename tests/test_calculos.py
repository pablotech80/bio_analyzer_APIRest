import unittest

from app.body_analysis.calculos import (
    calcular_macronutrientes,
    calcular_porcentaje_grasa,
)
from app.body_analysis.model import ObjetivoNutricional, Sexo


class TestCalculos(unittest.TestCase):

    def test_mantener_peso(self):
        resultado = calcular_macronutrientes(2000, ObjetivoNutricional.MANTENER_PESO)
        esperado = (150.0, 200.0, 66.67)
        self.assertAlmostEqual(resultado[0], esperado[0], places=2)
        self.assertAlmostEqual(resultado[1], esperado[1], places=2)
        self.assertAlmostEqual(resultado[2], esperado[2], places=2)

    def test_perder_grasa(self):
        resultado = calcular_macronutrientes(2000, ObjetivoNutricional.PERDER_GRASA)
        esperado = (200.0, 200.0, 44.44)
        self.assertAlmostEqual(resultado[0], esperado[0], places=2)
        self.assertAlmostEqual(resultado[1], esperado[1], places=2)
        self.assertAlmostEqual(resultado[2], esperado[2], places=2)

    def test_ganar_masa_muscular(self):
        resultado = calcular_macronutrientes(
            2000, ObjetivoNutricional.GANAR_MASA_MUSCULAR
        )
        esperado = (150.0, 250.0, 44.44)
        self.assertAlmostEqual(resultado[0], esperado[0], places=2)
        self.assertAlmostEqual(resultado[1], esperado[1], places=2)
        self.assertAlmostEqual(resultado[2], esperado[2], places=2)

    def test_objetivo_invalido(self):
        with self.assertRaises(ValueError):
            calcular_macronutrientes(2000, "perder peso rapido")

    def test_calcular_porcentaje_grasa_hombre(self):
        altura = 165
        cuello = 41
        cintura = 98
        genero = Sexo.HOMBRE
        resultado = calcular_porcentaje_grasa(cintura, cuello, altura, genero)
        self.assertAlmostEqual(resultado, 25.89, places=2)

    def test_calcular_porcentaje_grasa_mujer(self):
        altura = 170
        cuello = 37
        cintura = 75
        cadera = 100
        genero = Sexo.MUJER
        resultado = calcular_porcentaje_grasa(cintura, cuello, altura, genero, cadera)
        self.assertAlmostEqual(resultado, 26.11, places=2)


if __name__ == "__main__":
    unittest.main()
