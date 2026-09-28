import os
import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio

class MainView(tk.Frame):
    def __init__(self, master, servicio: RestauranteServicio, al_cerrar_sesion):
        super().__init__(master)
        self.servicio = servicio
        self.al_cerrar_sesion = al_cerrar_sesion
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Barra superior con Assets / Logo
        top_bar = tk.Frame(self, bg="#2C3E50", padx=10, pady=10)
        top_bar.pack(fill=tk.X)

        # Cargar logo de assets de forma segura
        ruta_assets = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        ruta_logo = os.path.join(ruta_assets, "logo.png")
        if os.path.exists(ruta_logo):
            try:
                self.img_logo = tk.PhotoImage(file=ruta_logo)
                lbl_logo = tk.Label(top_bar, image=self.img_logo, bg="#2C3E50")
                lbl_logo.pack(side=tk.LEFT, padx=(0, 10))
            except Exception:
                pass

        self.lbl_bienvenida = tk.Label(top_bar, text="Bienvenido a Restaurante App", fg="white", bg="#2C3E50", font=("Helvetica", 12, "bold"))
        self.lbl_bienvenida.pack(side=tk.LEFT)

        btn_logout = tk.Button(top_bar, text="Cerrar Sesión", bg="#E74C3C", fg="white", font=("Helvetica", 9, "bold"),
                               command=self._cerrar_sesion, cursor="hand2")
        btn_logout.pack(side=tk.RIGHT)

        # Contenedor de Pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab Ventas (Semana 15)
        tab_ventas = tk.Frame(notebook)
        notebook.add(tab_ventas, text="🛒 Registro de Ventas")
        self._crear_seccion_ventas(tab_ventas)

        # Tab Productos
        tab_prod = tk.Frame(notebook)
        notebook.add(tab_prod, text="📦 Gestión de Productos")
        self._crear_seccion_productos(tab_prod)

        # Tab Usuarios
        tab_usr = tk.Frame(notebook)
        notebook.add(tab_usr, text="👥 Usuarios Registrados")
        self._crear_tabla_usuarios(tab_usr)

    def _crear_seccion_ventas(self, parent):
        # Formulario de Registro de Venta
        frame_form = tk.LabelFrame(parent, text=" Nueva Operación de Venta ", padx=10, pady=10)
        frame_form.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(frame_form, text="Usuario Cliente:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.cbo_usuarios = ttk.Combobox(frame_form, state="readonly", width=30)
        self.cbo_usuarios.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame_form, text="Producto:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.cbo_productos = ttk.Combobox(frame_form, state="readonly", width=30)
        self.cbo_productos.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        tk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.ent_cantidad_venta = tk.Entry(frame_form, width=15)
        self.ent_cantidad_venta.insert(0, "1")
        self.ent_cantidad_venta.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Evento command= hacia el Callback de Venta
        btn_registrar_venta = tk.Button(frame_form, text="Registrar Venta", bg="#27AE60", fg="white", 
                                        font=("Helvetica", 10, "bold"), command=self._callback_registrar_venta, cursor="hand2")
        btn_registrar_venta.grid(row=1, column=3, sticky="e", padx=5, pady=5)

        # Tabla de Historial de Ventas
        frame_tabla = tk.LabelFrame(parent, text=" Historial de Ventas Registradas ", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("id", "fecha", "usuario", "producto", "cantidad", "total")
        self.tabla_ventas = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        self.tabla_ventas.heading("id", text="ID Venta")
        self.tabla_ventas.heading("fecha", text="Fecha y Hora")
        self.tabla_ventas.heading("usuario", text="ID Usuario")
        self.tabla_ventas.heading("producto", text="Cód. Producto")
        self.tabla_ventas.heading("cantidad", text="Cant.")
        self.tabla_ventas.heading("total", text="Total ($)")

        self.tabla_ventas.pack(fill=tk.BOTH, expand=True)

    def _callback_registrar_venta(self):
        usr_sel = self.cbo_usuarios.get().strip()
        prod_sel = self.cbo_productos.get().strip()
        cant_str = self.ent_cantidad_venta.get().strip()

        if not usr_sel or not prod_sel:
            messagebox.showwarning("Atención", "Debe seleccionar un usuario y un producto.")
            return

        try:
            cant = int(cant_str)
            if cant <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un entero positivo.")
            return

        usr_id = usr_sel.split(" - ")[0]
        prod_cod = prod_sel.split(" - ")[0]

        exito, msj = self.servicio.registrar_venta(usr_id, prod_cod, cant)
        if exito:
            messagebox.showinfo("Venta Registrada", msj)
            self._cargar_tabla_ventas()
            self._cargar_tabla_productos()
            self._actualizar_combos()
        else:
            messagebox.showerror("Error en Venta", msj)

    def _crear_seccion_productos(self, parent):
        frame_form = tk.LabelFrame(parent, text=" Formulario de Producto ", padx=10, pady=10)
        frame_form.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(frame_form, text="Código:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ent_codigo = tk.Entry(frame_form, width=15)
        self.ent_codigo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.ent_nombre = tk.Entry(frame_form, width=25)
        self.ent_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        tk.Label(frame_form, text="Precio ($):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.ent_precio = tk.Entry(frame_form, width=15)
        self.ent_precio.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame_form, text="Stock:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.ent_stock = tk.Entry(frame_form, width=15)
        self.ent_stock.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        frame_acciones = tk.Frame(frame_form)
        frame_acciones.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(frame_acciones, text="Registrar", bg="#4CAF50", fg="white", command=self._registrar_producto, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_acciones, text="Consultar/Cargar", bg="#2196F3", fg="white", command=self._consultar_producto, width=14).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_acciones, text="Actualizar", bg="#FF9800", fg="white", command=self._actualizar_producto, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_acciones, text="Eliminar", bg="#F44336", fg="white", command=self._eliminar_producto, width=12).pack(side=tk.LEFT, padx=5)

        frame_tabla = tk.LabelFrame(parent, text=" Listado de Productos ", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("codigo", "nombre", "precio", "stock")
        self.tabla_productos = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Nombre del Producto")
        self.tabla_productos.heading("precio", text="Precio ($)")
        self.tabla_productos.heading("stock", text="Stock Disponible")
        self.tabla_productos.pack(fill=tk.BOTH, expand=True)

    def _crear_tabla_usuarios(self, parent):
        frame_tabla = tk.LabelFrame(parent, text=" Usuarios del Sistema ", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("identificacion", "nombre")
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        self.tabla_usuarios.heading("identificacion", text="Identificación / Usuario")
        self.tabla_usuarios.heading("nombre", text="Nombre Completo")
        self.tabla_usuarios.pack(fill=tk.BOTH, expand=True)

    def _actualizar_combos(self):
        usrs = [f"{u.identificacion} - {u.nombre}" for u in self.servicio.listar_usuarios()]
        self.cbo_usuarios["values"] = usrs
        if usrs:
            self.cbo_usuarios.current(0)

        prods = [f"{p.codigo} - {p.nombre} (${p.precio:.2f})" for p in self.servicio.listar_productos()]
        self.cbo_productos["values"] = prods
        if prods:
            self.cbo_productos.current(0)

    def _cargar_tabla_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)
        for v in self.servicio.listar_ventas():
            self.tabla_ventas.insert("", tk.END, values=(v.id_venta, v.fecha, v.usuario_id, v.producto_codigo, v.cantidad, f"${v.total:.2f}"))

    def _cargar_tabla_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        for p in self.servicio.listar_productos():
            self.tabla_productos.insert("", tk.END, values=(p.codigo, p.nombre, f"${p.precio:.2f}", p.stock))

    def _cargar_tabla_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        for u in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert("", tk.END, values=(u.identificacion, u.nombre))

    def _registrar_producto(self):
        c, n, p_str, s_str = self.ent_codigo.get().strip(), self.ent_nombre.get().strip(), self.ent_precio.get().strip(), self.ent_stock.get().strip()
        if not c or not n or not p_str or not s_str:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return
        try:
            p, s = float(p_str), int(s_str)
        except ValueError:
            messagebox.showerror("Error", "Precio y stock deben ser numéricos.")
            return

        if self.servicio.agregar_producto(c, n, p, s):
            messagebox.showinfo("Éxito", f"Producto '{n}' registrado.")
            self._cargar_tabla_productos()
            self._actualizar_combos()
        else:
            messagebox.showerror("Error", f"El código '{c}' ya existe.")

    def _consultar_producto(self):
        c = self.ent_codigo.get().strip()
        p = self.servicio.buscar_producto_por_codigo(c)
        if p:
            self.ent_nombre.delete(0, tk.END); self.ent_nombre.insert(0, p.nombre)
            self.ent_precio.delete(0, tk.END); self.ent_precio.insert(0, str(p.precio))
            self.ent_stock.delete(0, tk.END); self.ent_stock.insert(0, str(p.stock))
        else:
            messagebox.showerror("No encontrado", f"No existe producto '{c}'.")

    def _actualizar_producto(self):
        c, n, p_str, s_str = self.ent_codigo.get().strip(), self.ent_nombre.get().strip(), self.ent_precio.get().strip(), self.ent_stock.get().strip()
        if self.servicio.actualizar_producto(c, n, float(p_str), int(s_str)):
            messagebox.showinfo("Éxito", "Producto actualizado.")
            self._cargar_tabla_productos()
            self._actualizar_combos()

    def _eliminar_producto(self):
        c = self.ent_codigo.get().strip()
        if self.servicio.eliminar_producto(c):
            messagebox.showinfo("Éxito", "Producto eliminado.")
            self._cargar_tabla_productos()
            self._actualizar_combos()

    def actualizar_datos(self):
        usr = self.servicio.obtener_usuario_actual()
        if usr:
            self.lbl_bienvenida.config(text=f"Bienvenido, {usr.nombre}")
        self._cargar_tabla_productos()
        self._cargar_tabla_usuarios()
        self._cargar_tabla_ventas()
        self._actualizar_combos()

    def _cerrar_sesion(self):
        self.servicio.cerrar_sesion()
        self.al_cerrar_sesion()