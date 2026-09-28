import json
import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.path.join(BASE_DIR, "datos")

class ArchivoServicio:
    @staticmethod
    def cargar_productos() -> list[Producto]:
        ruta = os.path.join(DATOS_DIR, "productos.json")
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [Producto.desde_diccionario(p) for p in datos]

    @staticmethod
    def guardar_productos(productos: list[Producto]) -> None:
        ruta = os.path.join(DATOS_DIR, "productos.json")
        os.makedirs(DATOS_DIR, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([p.a_diccionario() for p in productos], f, indent=2, ensure_ascii=False)

    @staticmethod
    def cargar_usuarios() -> list[Usuario]:
        ruta = os.path.join(DATOS_DIR, "usuarios.json")
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [Usuario.desde_diccionario(u) for u in datos]

    @staticmethod
    def cargar_ventas() -> list[Venta]:
        ruta = os.path.join(DATOS_DIR, "ventas.json")
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [Venta.desde_diccionario(v) for v in datos]

    @staticmethod
    def guardar_ventas(ventas: list[Venta]) -> None:
        ruta = os.path.join(DATOS_DIR, "ventas.json")
        os.makedirs(DATOS_DIR, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([v.a_diccionario() for v in ventas], f, indent=2, ensure_ascii=False)