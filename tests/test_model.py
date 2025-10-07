import unittest

from app.body_analysis.model import Sexo, ObjetivoNutricional


class TestEnums(unittest.TestCase):

    def test_sexo_values(self):
        self.assertEqual(Sexo.HOMBRE.value, "h")
        self.assertEqual(Sexo.MUJER.value, "m")

    def test_objetivo_nutricional_values(self):
        self.assertEqual(ObjetivoNutricional.MANTENER_PESO.value, "mantener peso")
        self.assertEqual(ObjetivoNutricional.PERDER_GRASA.value, "perder grasa")
        self.assertEqual(
            ObjetivoNutricional.GANAR_MASA_MUSCULAR.value, "ganar masa muscular"
        )

    def test_invalid_sexo(self):
        with self.assertRaises(ValueError):
            Sexo("x")

    def test_invalid_objetivo_nutricional(self):
        with self.assertRaises(ValueError):
            ObjetivoNutricional("bajar peso")


if __name__ == "__main__":
    unittest.main()
