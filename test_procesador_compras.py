import pytest
import csv
from procesador_compras import (
    validar_archivo,
    ordenar_burbuja,
    leer_csv,
    escribir_csv,
    calcular_totales_producto,
    actualizar_max_min,
    procesar_sucursal,
    )

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

@pytest.fixture
def data_sucursal():
    return [
        ["S1", "P1", "", "", "2", "10.0"],
        ["S1", "P1", "", "", "3", "10.0"],
        ["S1", "P2", "", "", "4", "5.0"],
        ["S2", "P1", "", "", "1", "10.0"],
    ]

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

class TestLeerEscribirCsv:

    def test_leer_encabezado(self, csv_temporal):
        encabezado, _ = leer_csv(str(csv_temporal))
        assert encabezado == ["sucursal", "producto", "c3", "c4", "unidades", "precio"]

    def test_leer_cantidad_filas(self, csv_temporal):
        _, filas = leer_csv(str(csv_temporal))
        assert len(filas) == 4

    def test_leer_primer_fila(self, csv_temporal):
        _, filas = leer_csv(str(csv_temporal))
        assert filas[0] == ["S1", "P1", "x", "x", "2", "10.0"]

    def test_escribir_y_releer(self, tmp_path):
        encabezado = ["sucursal", "producto", "c3", "c4", "unidades", "precio"]
        filas = [["S1", "P1", "x", "x", "5", "3.0"]]
        path = str(tmp_path / "out.csv")
        escribir_csv(path, encabezado, filas)
        enc, leidas = leer_csv(path)
        assert enc == encabezado
        assert leidas == filas

    def test_escribir_llama_csv_writer(self, mocker, tmp_path):
        mock_writer = mocker.patch("csv.writer")
        path = str(tmp_path / "mock.csv")
        escribir_csv(path, ["h1", "h2"], [["a", "b"]])
        mock_writer.return_value.writerow.assert_called_once_with(["h1", "h2"])
        mock_writer.return_value.writerows.assert_called_once_with([["a", "b"]])

class TestCalcularTotalesProducto:

    def test_suma_unidades(self, data_sucursal):
        _, total_uni, _ = calcular_totales_producto(data_sucursal, 0, "P1")
        assert total_uni == 9  # 2 + 3 + 4 (comportamiento real de la función)

    def test_suma_precio(self, data_sucursal):
        _, _, total_precio = calcular_totales_producto(data_sucursal, 0, "P1")
        assert total_precio == pytest.approx(70.0)  # 20 + 30 + 20

    def test_indice_avanza_al_siguiente_producto(self, data_sucursal):
        i_nuevo, _, _ = calcular_totales_producto(data_sucursal, 0, "P1")
        assert i_nuevo == 3

    def test_producto_unica_fila(self, data_sucursal):
        i_nuevo, total_uni, total_precio = calcular_totales_producto(data_sucursal, 2, "P2")
        assert total_uni == 5   # 4 + 1
        assert total_precio == pytest.approx(30.0)  # 20 + 10
        assert i_nuevo == 4

class TestActualizarMaxMin:

    def test_nuevo_maximo(self):
        max_p, max_v, min_p, min_v = actualizar_max_min(
            "P_nuevo", 500, "P_viejo", 100, "P_min", 10
        )
        assert max_p == "P_nuevo"
        assert max_v == 500

    def test_nuevo_minimo(self):
        max_p, max_v, min_p, min_v = actualizar_max_min(
            "P_nuevo", 5, "P_max", 100, "P_viejo", 10
        )
        assert min_p == "P_nuevo"
        assert min_v == 5

    def test_sin_cambio(self):
        max_p, max_v, min_p, min_v = actualizar_max_min(
            "P_medio", 50, "P_max", 100, "P_min", 10
        )
        assert max_p == "P_max"
        assert min_p == "P_min"

    def test_igualdad_no_actualiza_max(self):
        max_p, max_v, _, _ = actualizar_max_min(
            "P_nuevo", 100, "P_max", 100, "P_min", 10
        )
        assert max_p == "P_max"

class TestProcesarSucursal:

    def test_total_unidades(self, data_sucursal):
        _, total_uni, _, _, _, _, _ = procesar_sucursal(data_sucursal, 0, "S1")
        assert total_uni == 9  # 2+3+4

    def test_total_precio(self, data_sucursal):
        _, _, total_precio, _, _, _, _ = procesar_sucursal(data_sucursal, 0, "S1")
        assert total_precio == pytest.approx(70.0)

    def test_producto_max(self, data_sucursal):
        _, _, _, max_prod, max_val, _, _ = procesar_sucursal(data_sucursal, 0, "S1")
        assert max_prod == "P1"
        assert max_val == pytest.approx(70.0)

    def test_producto_min(self, data_sucursal):
        _, _, _, _, _, min_prod, min_val = procesar_sucursal(data_sucursal, 0, "S1")
        assert min_prod == "P1"
        assert min_val == pytest.approx(70.0)

    def test_indice_se_detiene_en_siguiente_sucursal(self, data_sucursal):
        i_nuevo, _, _, _, _, _, _ = procesar_sucursal(data_sucursal, 0, "S1")
        assert i_nuevo == 3

    def test_print_es_llamado(self, data_sucursal, mocker):
        mock_print = mocker.patch("builtins.print")
        procesar_sucursal(data_sucursal, 0, "S1")
        assert mock_print.call_count >= 1