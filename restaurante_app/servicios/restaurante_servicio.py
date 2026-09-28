import uuid
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        self._productos: list[Producto] = ArchivoServicio.cargar_productos()
        self._usuarios: list[Usuario] = ArchivoServicio.cargar_usuarios()
        self._ventas: list[Venta] = ArchivoServicio.cargar_ventas()
        self._usuario_autenticado: Usuario | None = None

    def validar_acceso(self, identificacion: str, clave: str) -> bool:
        for u in self._usuarios:
            if u.identificacion == identificacion and u.clave == clave:
                self._usuario_autenticado = u
                return True
        return False

    def obtener_usuario_actual(self) -> Usuario | None:
        return self._usuario_autenticado

    def cerrar_sesion(self) -> None:
        self._usuario_autenticado = None

    def listar_productos(self) -> list[Producto]:
        return self._productos

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios

    def listar_ventas(self) -> list[Venta]:
        return self._ventas

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        for p in self._productos:
            if p.codigo.lower() == codigo.lower():
                return p
        return None

    def agregar_producto(self, codigo: str, nombre: str, precio: float, stock: int) -> bool:
        if self.buscar_producto_por_codigo(codigo) is not None:
            return False
        nuevo = Producto(codigo, nombre, precio, stock)
        self._productos.append(nuevo)
        ArchivoServicio.guardar_productos(self._productos)
        return True

    def actualizar_producto(self, codigo: str, nombre: str, precio: float, stock: int) -> bool:
        prod = self.buscar_producto_por_codigo(codigo)
        if prod is None:
            return False
        prod.nombre = nombre
        prod.precio = precio
        prod.stock = stock
        ArchivoServicio.guardar_productos(self._productos)
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        prod = self.buscar_producto_por_codigo(codigo)
        if prod is None:
            return False
        self._productos.remove(prod)
        ArchivoServicio.guardar_productos(self._productos)
        return True

    def registrar_venta(self, usuario_id: str, producto_codigo: str, cantidad: int) -> tuple[bool, str]:
        prod = self.buscar_producto_por_codigo(producto_codigo)
        if not prod:
            return False, "El producto seleccionado no existe."

        if prod.stock < cantidad:
            return False, f"Stock insuficiente. Disponible: {prod.stock}"

        prod.stock -= cantidad
        ArchivoServicio.guardar_productos(self._productos)

        total = prod.precio * cantidad
        id_v = f"V-{len(self._ventas) + 1:03d}"
        nueva_venta = Venta(id_v, usuario_id, producto_codigo, cantidad, total)
        self._ventas.append(nueva_venta)
        ArchivoServicio.guardar_ventas(self._ventas)

        return True, f"Venta registrada con éxito. Total: ${total:.2f}"