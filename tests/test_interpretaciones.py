import unittest

from src.body_analyzer.interpretaciones import *


class TestFuncionesSalud(unittest.TestCase):

    def test_interpretar_imc_hombre_alto_musculo(self):
        resultado = interpretar_imc(26.0, 20.0, Sexo.HOMBRE)
        self.assertEqual(resultado, "El IMC es alto, pero puede estar influenciado por una alta masa muscular.")

    def test_interpretar_imc_mujer_alto_musculo(self):
        resultado = interpretar_imc(26.0, 17.0, Sexo.MUJER)
        self.assertEqual(resultado, "El IMC es alto, pero puede estar influenciado por una alta masa muscular.")

    def test_interpretar_imc_bajo(self):
        resultado = interpretar_imc(17.0, 15.0, Sexo.HOMBRE)
        self.assertEqual(resultado, "El IMC es bajo, se recomienda consultar con un profesional de salud.")

    def test_interpretar_imc_normal(self):
        resultado = interpretar_imc(22.0, 15.0, Sexo.HOMBRE)
        self.assertEqual(resultado, "El IMC está dentro del rango normal.")

    def test_interpretar_porcentaje_grasa_hombre_alto(self):
        resultado = interpretar_porcentaje_grasa(GRASA_ALTA_HOMBRES + 1, Sexo.HOMBRE)
        self.assertEqual(resultado, "Alto")

    def test_interpretar_porcentaje_grasa_mujer_bajo(self):
        resultado = interpretar_porcentaje_grasa(GRASA_BAJA_MUJERES - 1, Sexo.MUJER)
        self.assertEqual(resultado, "Bajo")

    def test_interpretar_porcentaje_grasa_normal(self):
        resultado = interpretar_porcentaje_grasa(GRASA_ALTA_HOMBRES - 1, Sexo.HOMBRE)
        self.assertEqual(resultado, "Normal")

    def test_interpretar_ffmi_hombre_fuerte(self):
        resultado = interpretar_ffmi(FFMI_UMBRAL_HOMBRES[4], Sexo.HOMBRE)
        self.assertEqual(resultado, "Muy fuerte (Excelente forma física). Cerca del máximo potencial.")

    def test_interpretar_ffmi_mujer_cercano_normal(self):
        resultado = interpretar_ffmi(FFMI_UMBRAL_MUJERES[0] + 1, Sexo.MUJER)
        self.assertEqual(resultado, "Normal")

    def test_interpretar_rcc_alto_riesgo_hombre(self):
        resultado = interpretar_rcc(RCC_ALTO_HOMBRES + 0.1, Sexo.HOMBRE)
        self.assertEqual(resultado, "Alto riesgo")

    def test_interpretar_rcc_moderado_riesgo_mujer(self):
        resultado = interpretar_rcc(RCC_MODERADO_MUJERES + 0.01, Sexo.MUJER)
        self.assertEqual(resultado, "Moderado riesgo")

    def test_interpretar_ratio_cintura_altura_alto_riesgo(self):
        resultado = interpretar_ratio_cintura_altura(RATIO_ALTO_RIESGO + 0.01)
        self.assertEqual(resultado, "Alto riesgo")

    def test_interpretar_ratio_cintura_altura_bajo_riesgo(self):
        resultado = interpretar_ratio_cintura_altura(RATIO_MODERADO_RIESGO - 0.01)
        self.assertEqual(resultado, "Bajo riesgo")

    def test_interpretar_ratio_cintura_altura_invalid(self):
        with self.assertRaises(ValueError):
            interpretar_ratio_cintura_altura(0)


if __name__ == '__main__':
    unittest.main()
