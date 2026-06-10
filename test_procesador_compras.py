import pytest
import csv
from procesador_compras import validar_archivo, ordenar_burbuja

@pytest.fixture
def csv_temporal(tmp_path):
    encabezado = ["sucursal", "producto", "c3", "c4", "unidades", "precio"]
    filas = [
        ["S1", "P1", "x", "x", "2", "10.0"],
        ["S1", "P1", "x", "x", "3", "10.0"],
        ["S1", "P2", "x", "x", "4", "5.0"],
        ["S2", "P1", "x", "x", "1", "10.0"],
    ]
    path = tmp_path / "test.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        writer.writerows(filas)
    return path

class TestValidarArchivo:

    def test_archivo_existente(self, csv_temporal):
        assert validar_archivo(str(csv_temporal)) is True

    def test_archivo_inexistente(self):
        assert validar_archivo("/tmp/no_existe_12345.csv") is False

    def test_usa_os_path_exists(self, mocker):
        mock_exists = mocker.patch("os.path.exists", return_value=True)
        validar_archivo("cualquier_path.csv")
        mock_exists.assert_called_once_with("cualquier_path.csv")

class TestOrdenarBurbuja:

    def test_lista_ya_ordenada(self):
        filas = [["A", "P1"], ["A", "P2"], ["B", "P1"]]
        assert ordenar_burbuja(filas[:]) == [["A", "P1"], ["A", "P2"], ["B", "P1"]]

    def test_lista_desordenada(self):
        filas = [["B", "P1"], ["A", "P2"], ["A", "P1"]]
        assert ordenar_burbuja(filas[:]) == [["A", "P1"], ["A", "P2"], ["B", "P1"]]

    def test_lista_un_elemento(self):
        assert ordenar_burbuja([["A", "P1"]]) == [["A", "P1"]]

    def test_lista_vacia(self):
        assert ordenar_burbuja([]) == []

    def test_ordena_por_sucursal_luego_producto(self):
        filas = [["Z", "A"], ["A", "Z"], ["A", "A"]]
        assert ordenar_burbuja(filas[:]) == [["A", "A"], ["A", "Z"], ["Z", "A"]]
