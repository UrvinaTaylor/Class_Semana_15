from datetime import datetime

class Venta:
    def __init__(self, id_venta: str, usuario_id: str, producto_codigo: str, cantidad: int, total: float, fecha: str = None):
        self.id_venta = id_venta
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def a_diccionario(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "total": self.total,
            "fecha": self.fecha
        }

    @staticmethod
    def desde_diccionario(datos: dict) -> 'Venta':
        return Venta(
            id_venta=datos.get("id_venta", ""),
            usuario_id=datos.get("usuario_id", ""),
            producto_codigo=datos.get("producto_codigo", ""),
            cantidad=datos.get("cantidad", 1),
            total=float(datos.get("total", 0.0)),
            fecha=datos.get("fecha", "")
        )