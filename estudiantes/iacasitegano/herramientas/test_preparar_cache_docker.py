"""Prueba de regresión de preparar() con el caché horneado y límites de liga.

Requiere Docker y la imagen torneo-bot-base:local. Para una muestra mayor y
con concurrencia, usar verificar_preparar_cache.py.
"""

from pathlib import Path
import tempfile
import unittest

from verificar_preparar_cache import medir


class PrepararCacheDockerTest(unittest.TestCase):
    def test_preparar_deja_margen_mayor_a_diez_segundos(self):
        """Una instancia fría a 0.5 CPU debe terminar import + preparar antes de 10 s."""
        with tempfile.TemporaryDirectory(prefix="iacasitegano-cache-test-") as temporal:
            cache_motor_vacia = Path(temporal) / "cache-motor-vacia"
            cache_motor_vacia.mkdir()
            resultado = medir(0.5, 1, cache_motor_vacia)

        self.assertEqual(resultado["exit"], 0, resultado)
        medicion = resultado["medicion"]
        self.assertTrue(medicion.get("ok"), medicion)
        self.assertLess(medicion["total_s"], 10.0, medicion)


if __name__ == "__main__":
    unittest.main()
