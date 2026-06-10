import pytest
from procesador_compras import validar_archivo

class TestValidarArchivo:

    def test_archivo_existente(self, csv_temporal):
        assert validar_archivo(str(csv_temporal)) is True

    def test_archivo_inexistente(self):
        assert validar_archivo("/tmp/no_existe_12345.csv") is False

    def test_usa_os_path_exists(self, mocker):
        mock_exists = mocker.patch("os.path.exists", return_value=True)
        validar_archivo("cualquier_path.csv")
        mock_exists.assert_called_once_with("cualquier_path.csv")
