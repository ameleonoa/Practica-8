import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# DATOS
COLOR_FONDO = "#DCEBFA"
COLOR_BOTON = "#A9CBEE"
COLOR_BOTON_HOVER = "#8DB9E6"
COLOR_ENCABEZADO = "#B8D4F0"


def aplicar_estilo(ventana):
    ventana.configure(bg=COLOR_FONDO)
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure(".", background=COLOR_FONDO, foreground="#1F2D3D")
    estilo.configure("TFrame", background=COLOR_FONDO)
    estilo.configure("TLabel", background=COLOR_FONDO, foreground="#1F2D3D")
    estilo.configure("TButton", background=COLOR_BOTON, foreground="#1F2D3D",
                     padding=5, borderwidth=1)
    estilo.map("TButton", background=[("active", COLOR_BOTON_HOVER)])
    estilo.configure("TNotebook", background=COLOR_FONDO)
    estilo.configure("TNotebook.Tab", background=COLOR_ENCABEZADO, padding=(12, 4))
    estilo.map("TNotebook.Tab", background=[("selected", "#FFFFFF")])
    estilo.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF")
    estilo.configure("Treeview.Heading", background=COLOR_ENCABEZADO,
                     foreground="#1F2D3D", font=("Arial", 9, "bold"))

USUARIOS = {
    "admin": ("admin123", "Administrador"),
    "vendedor": ("ventas123", "Vendedor"),
}

clientes = []
productos = []
ventas = []



# INICIO DE SESIÓN

def login():
    resultado = {"usuario": None, "rol": None}

    ventana = tk.Tk()
    aplicar_estilo(ventana)
    ventana.title("Iniciar sesión - Tienda")
    ventana.geometry("320x230")
    ventana.resizable(False, False)

    ttk.Label(ventana, text="Iniciar sesión", font=("Arial", 16, "bold")).pack(pady=12)

    usuario = tk.StringVar()
    clave = tk.StringVar()

    ttk.Label(ventana, text="Usuario:").pack()
    ttk.Entry(ventana, textvariable=usuario, width=25).pack(pady=3)
    ttk.Label(ventana, text="Contraseña:").pack()
    ttk.Entry(ventana, textvariable=clave, show="*", width=25).pack(pady=3)

    def entrar():
        u = usuario.get().strip()
        if u in USUARIOS and USUARIOS[u][0] == clave.get():
            resultado["usuario"] = u
            resultado["rol"] = USUARIOS[u][1]
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ttk.Button(ventana, text="Entrar", command=entrar).pack(pady=15)
    ventana.bind("<Return>", lambda e: entrar())
    ventana.mainloop()
    return resultado


# PESTAÑA CLIENTES
def pestana_clientes(nb):
    marco = ttk.Frame(nb, padding=10)
    nombre = tk.StringVar()
    telefono = tk.StringVar()
    correo = tk.StringVar()

    ttk.Label(marco, text="Nombre:").grid(row=0, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=nombre, width=30).grid(row=0, column=1, pady=3)
    ttk.Label(marco, text="Teléfono:").grid(row=1, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=telefono, width=30).grid(row=1, column=1, pady=3)
    ttk.Label(marco, text="Correo:").grid(row=2, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=correo, width=30).grid(row=2, column=1, pady=3)

    tabla = ttk.Treeview(marco, columns=("id", "nombre", "telefono", "correo"),
                         show="headings", height=10)
    for col, texto, ancho in (("id", "ID", 40), ("nombre", "Nombre", 180),
                              ("telefono", "Teléfono", 110), ("correo", "Correo", 200)):
        tabla.heading(col, text=texto)
        tabla.column(col, width=ancho)
    tabla.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")

    def refrescar():
        tabla.delete(*tabla.get_children())
        for c in clientes:
            tabla.insert("", "end", values=(c["id"], c["nombre"], c["telefono"], c["correo"]))

    def agregar():
        if not nombre.get().strip():
            messagebox.showwarning("Aviso", "El nombre es obligatorio")
            return
        nuevo_id = max([c["id"] for c in clientes], default=0) + 1
        clientes.append({"id": nuevo_id, "nombre": nombre.get().strip(),
                         "telefono": telefono.get().strip(), "correo": correo.get().strip()})
        nombre.set("")
        telefono.set("")
        correo.set("")
        refrescar()

    def eliminar():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un cliente de la tabla")
            return
        id_cliente = int(tabla.item(sel[0])["values"][0])
        clientes[:] = [c for c in clientes if c["id"] != id_cliente]
        refrescar()

    ttk.Button(marco, text="Agregar cliente", command=agregar).grid(row=3, column=0, pady=8)
    ttk.Button(marco, text="Eliminar seleccionado", command=eliminar).grid(row=3, column=1, pady=8)

    return marco, refrescar


# PESTAÑA PRODUCTOS
def pestana_productos(nb):
    marco = ttk.Frame(nb, padding=10)
    codigo = tk.StringVar()
    nombre = tk.StringVar()
    precio = tk.StringVar()
    stock = tk.StringVar()

    ttk.Label(marco, text="Código:").grid(row=0, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=codigo, width=30).grid(row=0, column=1, pady=3)
    ttk.Label(marco, text="Nombre:").grid(row=1, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=nombre, width=30).grid(row=1, column=1, pady=3)
    ttk.Label(marco, text="Precio:").grid(row=2, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=precio, width=30).grid(row=2, column=1, pady=3)
    ttk.Label(marco, text="Cantidad en inventario:").grid(row=3, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=stock, width=30).grid(row=3, column=1, pady=3)

    tabla = ttk.Treeview(marco, columns=("codigo", "nombre", "precio", "stock"),
                         show="headings", height=9)
    for col, texto, ancho in (("codigo", "Código", 80), ("nombre", "Nombre", 220),
                              ("precio", "Precio", 90), ("stock", "Cantidad", 90)):
        tabla.heading(col, text=texto)
        tabla.column(col, width=ancho)
    tabla.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

    def refrescar():
        tabla.delete(*tabla.get_children())
        for p in productos:
            tabla.insert("", "end", values=(p["codigo"], p["nombre"],
                                            f"{p['precio']:.2f}", p["stock"]))

    def agregar():
        cod = codigo.get().strip()
        if not cod or not nombre.get().strip():
            messagebox.showwarning("Aviso", "Código y nombre son obligatorios")
            return
        if any(p["codigo"] == cod for p in productos):
            messagebox.showerror("Error", "Ya existe un producto con ese código")
            return
        try:
            pr = float(precio.get())
            st = int(stock.get())
            if pr < 0 or st < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser números válidos")
            return
        productos.append({"codigo": cod, "nombre": nombre.get().strip(),
                          "precio": pr, "stock": st})
        for v in (codigo, nombre, precio, stock):
            v.set("")
        refrescar()

    def eliminar():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla")
            return
        cod = str(tabla.item(sel[0])["values"][0])
        productos[:] = [p for p in productos if p["codigo"] != cod]
        refrescar()

    ttk.Button(marco, text="Agregar producto", command=agregar).grid(row=4, column=0, pady=8)
    ttk.Button(marco, text="Eliminar seleccionado", command=eliminar).grid(row=4, column=1, pady=8)

    return marco, refrescar



# TICKET

def armar_ticket(folio, fecha, cliente, vendedor, carrito, subtotal, total):
    ancho = 44
    lineas = [
        "=" * ancho,
        "TIENDA".center(ancho),
        "NOTA DE VENTA".center(ancho),
        "=" * ancho,
        f"Folio: {folio}",
        f"Fecha: {fecha}",
        f"Cliente: {cliente}",
        f"Atendió: {vendedor}",
        "-" * ancho,
        f"{'Producto':<18}{'Cant':>5}{'P.Unit':>9}{'Importe':>10}",
        "-" * ancho,
    ]
    for item in carrito:
        importe = item["cantidad"] * item["precio"]
        lineas.append(f"{item['nombre'][:17]:<18}{item['cantidad']:>5}"
                      f"{item['precio']:>9.2f}{importe:>10.2f}")
    lineas += [
        "-" * ancho,
        f"{'Subtotal:':>34}{subtotal:>10.2f}",
        f"{'TOTAL:':>34}{total:>10.2f}",
        "=" * ancho,
        "Gracias por su compra".center(ancho),
    ]
    return "\n".join(lineas)


def mostrar_ticket(texto):
    ventana = tk.Toplevel()
    ventana.configure(bg=COLOR_FONDO)
    ventana.title("Ticket de venta")
    caja = tk.Text(ventana, width=46, height=24, font=("Courier", 10))
    caja.insert("1.0", texto)
    caja.config(state="disabled")
    caja.pack(padx=10, pady=10)
    ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=5)



# PESTAÑA VENTAS
def pestana_ventas(nb, usuario):
    marco = ttk.Frame(nb, padding=10)
    carrito = []

    cliente_sel = tk.StringVar()
    producto_sel = tk.StringVar()
    cantidad = tk.StringVar(value="1")
    var_subtotal = tk.StringVar(value="Subtotal: $0.00")
    var_total = tk.StringVar(value="Total: $0.00")

    ttk.Label(marco, text="Cliente:").grid(row=0, column=0, sticky="e", pady=3)
    combo_cliente = ttk.Combobox(marco, textvariable=cliente_sel, state="readonly", width=35)
    combo_cliente.grid(row=0, column=1, columnspan=2, sticky="w", pady=3)

    ttk.Label(marco, text="Producto:").grid(row=1, column=0, sticky="e", pady=3)
    combo_producto = ttk.Combobox(marco, textvariable=producto_sel, state="readonly", width=35)
    combo_producto.grid(row=1, column=1, columnspan=2, sticky="w", pady=3)

    ttk.Label(marco, text="Cantidad:").grid(row=2, column=0, sticky="e", pady=3)
    ttk.Entry(marco, textvariable=cantidad, width=8).grid(row=2, column=1, sticky="w", pady=3)

    tabla = ttk.Treeview(marco, columns=("producto", "cantidad", "precio", "importe"),
                         show="headings", height=8)
    for col, texto, ancho in (("producto", "Producto", 220), ("cantidad", "Cantidad", 80),
                              ("precio", "Precio unitario", 110), ("importe", "Importe", 100)):
        tabla.heading(col, text=texto)
        tabla.column(col, width=ancho)
    tabla.grid(row=4, column=0, columnspan=4, pady=10, sticky="nsew")

    ttk.Label(marco, textvariable=var_subtotal, font=("Arial", 11)).grid(row=5, column=2, columnspan=2, sticky="e")
    ttk.Label(marco, textvariable=var_total, font=("Arial", 12, "bold")).grid(row=6, column=2, columnspan=2, sticky="e")

    def calcular():
        subtotal = sum(i["cantidad"] * i["precio"] for i in carrito)
        total = subtotal
        var_subtotal.set(f"Subtotal: ${subtotal:.2f}")
        var_total.set(f"Total: ${total:.2f}")
        return subtotal, total

    def refrescar_tabla():
        tabla.delete(*tabla.get_children())
        for i in carrito:
            tabla.insert("", "end", values=(i["nombre"], i["cantidad"],
                                            f"{i['precio']:.2f}",
                                            f"{i['cantidad'] * i['precio']:.2f}"))
        calcular()

    def refrescar():

        combo_cliente["values"] = [f"{c['id']} - {c['nombre']}" for c in clientes]
        combo_producto["values"] = [f"{p['codigo']} - {p['nombre']}" for p in productos]

    def agregar_al_ticket():
        if not producto_sel.get():
            messagebox.showwarning("Aviso", "Elige un producto")
            return
        try:
            cant = int(cantidad.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un entero mayor a 0")
            return
        codigo = producto_sel.get().split(" - ")[0]
        prod = next(p for p in productos if p["codigo"] == codigo)
        ya_en_ticket = sum(i["cantidad"] for i in carrito if i["codigo"] == codigo)
        if ya_en_ticket + cant > prod["stock"]:
            messagebox.showerror("Error", f"Inventario insuficiente (disponible: {prod['stock']})")
            return
        for i in carrito:
            if i["codigo"] == codigo:
                i["cantidad"] += cant
                break
        else:
            carrito.append({"codigo": codigo, "nombre": prod["nombre"],
                            "cantidad": cant, "precio": prod["precio"]})
        refrescar_tabla()

    def quitar():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un renglón del ticket")
            return
        carrito.pop(tabla.index(sel[0]))
        refrescar_tabla()

    def finalizar():
        if not cliente_sel.get():
            messagebox.showwarning("Aviso", "Elige un cliente")
            return
        if not carrito:
            messagebox.showwarning("Aviso", "El ticket está vacío")
            return
        subtotal, total = calcular()
        folio = len(ventas) + 1
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        nombre_cliente = cliente_sel.get().split(" - ", 1)[1]
        texto = armar_ticket(folio, fecha, nombre_cliente, usuario, carrito, subtotal, total)
        # descontar inventario
        for item in carrito:
            for p in productos:
                if p["codigo"] == item["codigo"]:
                    p["stock"] -= item["cantidad"]
        ventas.append({"folio": folio, "fecha": fecha, "cliente": nombre_cliente,
                       "vendedor": usuario, "total": total, "ticket": texto})
        mostrar_ticket(texto)
        carrito.clear()
        cliente_sel.set("")
        producto_sel.set("")
        cantidad.set("1")
        refrescar_tabla()

    def cancelar():
        carrito.clear()
        refrescar_tabla()

    ttk.Button(marco, text="Agregar al ticket", command=agregar_al_ticket).grid(row=3, column=0, columnspan=2, pady=5)
    ttk.Button(marco, text="Quitar seleccionado", command=quitar).grid(row=3, column=2, pady=5)
    ttk.Button(marco, text="Finalizar venta", command=finalizar).grid(row=8, column=2, pady=10)
    ttk.Button(marco, text="Cancelar venta", command=cancelar).grid(row=8, column=3, pady=10)

    return marco, refrescar



# PESTAÑA HISTORIAL

def pestana_historial(nb):
    marco = ttk.Frame(nb, padding=10)

    tabla = ttk.Treeview(marco, columns=("folio", "fecha", "cliente", "vendedor", "total"),
                         show="headings", height=14)
    for col, texto, ancho in (("folio", "Folio", 50), ("fecha", "Fecha", 130),
                              ("cliente", "Cliente", 150), ("vendedor", "Vendedor", 100),
                              ("total", "Total", 90)):
        tabla.heading(col, text=texto)
        tabla.column(col, width=ancho)
    tabla.pack(pady=10, fill="both", expand=True)

    def refrescar():
        tabla.delete(*tabla.get_children())
        for v in ventas:
            tabla.insert("", "end", values=(v["folio"], v["fecha"], v["cliente"],
                                            v["vendedor"], f"{v['total']:.2f}"))

    def ver_ticket():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una venta")
            return
        folio = int(tabla.item(sel[0])["values"][0])
        venta = next(v for v in ventas if v["folio"] == folio)
        mostrar_ticket(venta["ticket"])

    ttk.Button(marco, text="Ver ticket", command=ver_ticket).pack()

    return marco, refrescar


# VENTANA PRINCIPAL

def ventana_principal(usuario, rol):
    ventana = tk.Tk()
    aplicar_estilo(ventana)
    ventana.title(f"Tienda - {usuario} ({rol})")
    ventana.geometry("640x560")

    ttk.Label(ventana, text=f"Bienvenido, {usuario}  |  Rol: {rol}",
              font=("Arial", 11, "bold")).pack(pady=6)

    estado = {"cerrar_sesion": False}

    def cerrar_sesion():
        estado["cerrar_sesion"] = True
        ventana.destroy()

    ttk.Button(ventana, text="Cerrar sesión", command=cerrar_sesion).pack()

    nb = ttk.Notebook(ventana)
    nb.pack(fill="both", expand=True, padx=8, pady=8)

    refrescadores = []

    marco, ref = pestana_clientes(nb)
    nb.add(marco, text="Clientes")
    refrescadores.append(ref)


    if rol == "Administrador":
        marco, ref = pestana_productos(nb)
        nb.add(marco, text="Productos")
        refrescadores.append(ref)

    marco, ref = pestana_ventas(nb, usuario)
    nb.add(marco, text="Ventas")
    refrescadores.append(ref)

    if rol == "Administrador":
        marco, ref = pestana_historial(nb)
        nb.add(marco, text="Historial")
        refrescadores.append(ref)


    nb.bind("<<NotebookTabChanged>>", lambda e: [r() for r in refrescadores])

    ventana.mainloop()
    return estado["cerrar_sesion"]



# PROGRAMA PRINCIPAL

if __name__ == "__main__":
    while True:
        datos = login()
        if not datos["rol"]:
            break
        volver_al_login = ventana_principal(datos["usuario"], datos["rol"])
        if not volver_al_login:
            break
