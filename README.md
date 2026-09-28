# Restaurante App - Evolución Semana 15: Manejo de Eventos y Ventas

**Estudiante:** Gilmar Taylor Urvina Santi  
**Materia:** Programación Orientada a Objetos  

---

## Propósito de la Semana 15
Evolucionar `restaurante_app` incorporando el **manejo de eventos** (`command=` y callbacks) mediante la implementación del módulo de **Registro de Ventas**, relacionando Usuarios y Productos, actualizando inventario y persistiendo en `ventas.json`.

---

## Flujo de Eventos Implementado
```text
[ ACCIÓN USUARIO ] ➔ Click en "Registrar Venta"
       ↓
[ BOTÓN COMMAND ]  ➔ command=self._callback_registrar_venta
       ↓
[ CALLBACK (GUI) ] ➔ Captura selección y delega la operación
       ↓
[ SERVICIO ]       ➔ RestauranteServicio valida stock y calcula total
       ↓
[ PERSISTENCIA ]   ➔ Guarda en ventas.json y actualiza productos.json
       ↓
[ RESPUESTA GUI ]  ➔ Muestra confirmación y refresca las tablas

```
##  Estructura Del Proyecto

restaurante_app/
├── assets/
│   └── logo.png
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md