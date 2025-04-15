import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from Biblio_back import BibliotecaBackend
from datetime import datetime
from PIL import Image, ImageTk

class BibliotecaFrontend:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca Digital")
        self.root.geometry("1200x650+0+0")
        
        self.colores = {
            "fondo": "#d2b48c",
            "primario": "#5d2417",
            "secundario": "#8d4925",
            "resaltado": "#c57d56",
            "detalle": "#320000",
            "verde": "#567d46",
            "blanco": "#ffffff"
        }
        
        self.fondo_tk = None
        self.cargar_fondo()
        
        self.biblioteca = BibliotecaBackend()
        
        self.estilo = ttk.Style()
        self.estilo.theme_use('default')
        
        fuente = ('Athene Voyage', 12)
        self.estilo.configure('TButton', font=fuente, padding=10, background=self.colores["primario"], foreground=self.colores["blanco"])
        self.estilo.map('TButton', background=[('active', self.colores["secundario"])])
        self.estilo.configure('TLabel', font=fuente, background=self.colores["fondo"], foreground=self.colores["detalle"])
        self.estilo.configure('Treeview', font=('Arial', 11), background=self.colores["blanco"], fieldbackground=self.colores["blanco"], foreground=self.colores["detalle"])
        self.estilo.configure('Treeview.Heading', font=('Arial', 12, 'bold'), background=self.colores["resaltado"], foreground=self.colores["detalle"])
        
        self.pantalla_actual = None
        self.mostrar_pantalla_inicio()
        try:
            root.iconbitmap("C://Users//Gabriela//Documents//SEGUNDO SEMESTRE CDD//PROGRAMACIÓN AVANZADA//Unidad_2//fondo.ico")
        except:
            pass
        
    def cargar_fondo(self):
        try:
            imagen_fondo = Image.open("C://Users//Gabriela//Documents//SEGUNDO SEMESTRE CDD//PROGRAMACIÓN AVANZADA//Unidad_2//fots.jpg")
            imagen_fondo = imagen_fondo.resize((1200, 650))
            self.fondo_tk = ImageTk.PhotoImage(imagen_fondo)
            self.label_fondo = tk.Label(self.root, image=self.fondo_tk)
            self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error al cargar imagen de fondo: {e}")
            
    def limpiar_pantalla(self):
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
        self.pantalla_actual = None
        
    def crear_frame(self):
        frame = tk.Frame(self.root, bg=self.colores["fondo"])
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        self.pantalla_actual = frame
        return frame
    
    def crear_label(self, parent, texto, tam=18, negrita=False):
        font = ('Athene Voyage', tam, 'bold' if negrita else 'normal')
        return tk.Label(parent, text=texto, font=font, fg=self.colores["detalle"], bg=self.colores["fondo"])
    
    def crear_entry(self, parent, variable):
        entry = ttk.Entry(parent, textvariable=variable)
        entry.pack(side='left', expand=True, fill='x', padx=5)
        return entry
    
    def crear_boton(self, parent, texto, comando):
        boton = ttk.Button(parent, text=texto, command=comando)
        boton.pack(pady=6, ipadx=10, ipady=6)
        return boton
    
    def boton_volver(self, frame, comando=None):
        if comando is None:
            comando = self.mostrar_pantalla_inicio
        ttk.Button(frame, text="Volver al Menú Principal", command=comando).pack(pady=10)
        
    def mostrar_pantalla_inicio(self):
        self.limpiar_pantalla()
        self.pantalla_actual = tk.Canvas(self.root, width=1200, height=650)
        self.pantalla_actual.pack(fill='both', expand=True)
        self.pantalla_actual.create_image(0, 0, image=self.fondo_tk, anchor='nw')
        contenedor = tk.Frame(self.pantalla_actual, bg=self.colores["fondo"])
        self.pantalla_actual.create_window(600, 325, window=contenedor) 
        label_titulo = tk.Label(
            contenedor,
            text="Biblioteca Digital",
            font=('Athene Voyage', 28, 'bold'),
            fg=self.colores["detalle"],
            bg=self.colores["fondo"]
        )
        label_titulo.pack(pady=20)
        botones_frame = tk.Frame(contenedor, bg=self.colores["fondo"])
        botones_frame.pack()
        opciones = [
            ("Buscar Materiales", self.mostrar_buscar_materiales),
            ("Realizar Préstamo", self.mostrar_realizar_prestamo),
            ("Registrar Devolución", self.mostrar_registrar_devolucion),
            ("Administrar Catálogo", self.mostrar_admin_catalogo),
            ("Registrar Usuario", self.mostrar_registrar_usuario),
            ("Ver Reportes", self.mostrar_reportes),
            ("Salir", self.root.quit)
        ]
        for texto, comando in opciones:
            ttk.Button(botones_frame, text=texto, command=comando).pack(fill='x', pady=6, ipadx=10, ipady=6)
            
    def mostrar_buscar_materiales(self):
        self.limpiar_pantalla()
        self.pantalla_actual = tk.Frame(self.root)
        self.pantalla_actual.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(self.pantalla_actual, text="Buscar Materiales", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Controles bus
        search_frame = tk.Frame(self.pantalla_actual)
        search_frame.pack(fill='x', pady=10)
        tk.Label(search_frame, text="Filtrar por:").pack(side='left', padx=5)
        
        self.filtro_var = tk.StringVar()
        filtros = ttk.Combobox(search_frame, textvariable=self.filtro_var, values=["Todos", "Título", "Autor", "Género", "Tipo", "Estado"])
        filtros.current(0)
        filtros.pack(side='left', padx=5)
        
        self.busqueda_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.busqueda_var).pack(side='left', expand=True, fill='x', padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.buscar_materiales).pack(side='left', padx=5)
        resultados_container = tk.Frame(self.pantalla_actual)
        resultados_container.pack(expand=True, fill='both', pady=10)
        self.resultados_frame = ttk.Treeview(resultados_container)
        self.resultados_frame.pack(side='left', expand=True, fill='both')
        scrollbar = ttk.Scrollbar(resultados_container, orient="vertical", command=self.resultados_frame.yview)
        scrollbar.pack(side='right', fill='y')
        self.resultados_frame.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar all_mat_in
        self.buscar_materiales()
        self.boton_volver(self.pantalla_actual)
        
    def buscar_materiales(self):
        # Limpiar resultados
        for item in self.resultados_frame.get_children():
            self.resultados_frame.delete(item)
        
        # Config_colum
        self.resultados_frame['columns'] = ("ID", "Tipo", "Título", "Autor", "Género", "Estado", "Fecha Ingreso")
        self.resultados_frame.column("#0", width=0, stretch=tk.NO)
        
        for col in self.resultados_frame['columns']:
            self.resultados_frame.column(col, anchor='w', width=120)
            self.resultados_frame.heading(col, text=col, anchor='w')
        
        self.resultados_frame.column("Título", width=200)
        self.resultados_frame.column("Autor", width=150)
        
        filtro = self.filtro_var.get()
        busqueda = self.busqueda_var.get()
        
        if filtro == "Todos":
            materiales = self.biblioteca.buscar_materiales()
        else:
            mapeo_filtros = {
                "Título": "titulo",
                "Autor": "autor",
                "Género": "genero",
                "Tipo": "tipo",
                "Estado": "estado"
            }
            materiales = self.biblioteca.buscar_materiales(mapeo_filtros[filtro], busqueda)
        if not materiales:
            messagebox.showinfo("Información", "No se encontraron materiales con esos criterios.")
            return
        for mat in materiales:
            self.resultados_frame.insert('', 'end', values=(
                mat['id'],
                mat.get('tipo', 'N/A'),
                mat.get('titulo', 'N/A'),
                mat.get('autor', 'N/A'),
                mat.get('genero', 'N/A'),
                mat.get('estado', 'N/A'),
                mat.get('fecha_ingreso', 'N/A')
            ))
            
    def mostrar_realizar_prestamo(self):
        self.limpiar_pantalla()
        
        self.pantalla_actual = tk.Frame(self.root)
        self.pantalla_actual.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(self.pantalla_actual, text="Realizar Préstamo", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Frame pf
        form_frame = tk.Frame(self.pantalla_actual)
        form_frame.pack(fill='x', pady=10)
        
        # Usuario ID
        tk.Label(form_frame, text="ID Usuario:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.usuario_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.usuario_id_var).grid(row=0, column=1, sticky='we', padx=5, pady=5)
        
        # Botón pb us
        ttk.Button(form_frame, text="Buscar Usuario", command=lambda: self.buscar_usuario(self.usuario_id_var.get())).grid(row=0, column=2, padx=5)
        
        # Material ID
        tk.Label(form_frame, text="ID Material:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.material_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.material_id_var).grid(row=1, column=1, sticky='we', padx=5, pady=5)
        
        # Botón pb mat
        ttk.Button(form_frame, text="Buscar Material", command=lambda: self.buscar_material(self.material_id_var.get())).grid(row=1, column=2, padx=5)
        
        # Botón realizar préstamo
        ttk.Button(form_frame, text="Realizar Préstamo", command=self.realizar_prestamo).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Información del usuario y material
        self.info_usuario = tk.Label(self.pantalla_actual, text="", font=('Arial', 10))
        self.info_usuario.pack(pady=5)
        
        self.info_material = tk.Label(self.pantalla_actual, text="", font=('Arial', 10))
        self.info_material.pack(pady=5)
        
        # Botón de descarga matdig
        self.boton_descarga = ttk.Button(self.pantalla_actual, text="Descargar", command=self.descargar_material_digital)
        self.boton_descarga.pack(pady=5)
        self.boton_descarga.pack_forget()  # Ocultar inicialmente
        
        # Info del préstamo
        self.info_prestamo = tk.Label(self.pantalla_actual, text="", font=('Arial', 12))
        self.info_prestamo.pack(pady=10)
        
        self.boton_volver(self.pantalla_actual)
        
    def buscar_material(self, material_id):
        material = next((m for m in self.biblioteca.datos['materiales'] if m['id'] == material_id), None)
        
        if material:
            info = f"Material: {material.get('titulo', 'N/A')} | Tipo: {material.get('tipo', 'N/A')}"
            info += f" | Estado: {material.get('estado', 'N/A')}"
            self.info_material.config(text=info)
            
            if material.get('tipo') == 'MaterialDigital' and 'enlace_descarga' in material:
                self.material_actual = material  # Guardar referencia al material actual
                self.boton_descarga.pack(pady=5)
            else:
                self.boton_descarga.pack_forget()
        else:
            messagebox.showerror("Error", "Material no encontrado")
            self.info_material.config(text="")
            self.boton_descarga.pack_forget()
            
    def descargar_material_digital(self):
        if hasattr(self, 'material_actual'):
            material = self.material_actual
            mensaje = f"Material descargado:\n\n"
            mensaje += f"Título: {material.get('titulo', 'N/A')}\n"
            mensaje += f"Tipo: {material.get('tipo', 'N/A')}\n"
            mensaje += f"Formato: {material.get('tipo_archivo', 'N/A')}\n"
            mensaje += f"Enlace: {material.get('enlace_descarga', 'N/A')}\n\n"
            mensaje += "¡Descarga completada!"
            
            messagebox.showinfo("Descarga Exitosa", mensaje)
        else:
            messagebox.showerror("Error", "No hay material digital seleccionado")
            
    def buscar_usuario(self, usuario_id):
        usuario = next((u for u in self.biblioteca.datos['usuarios'] if u['id'] == usuario_id), None)
        if usuario:
            info = f"Usuario: {usuario['nombre']} | Contacto: {usuario['contacto']}"
            info += f" | Penalizaciones: ${usuario['penalizaciones']}"
            self.info_usuario.config(text=info)
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
            
    def realizar_prestamo(self):
        usuario_id = self.usuario_id_var.get()
        material_id = self.material_id_var.get()
        
        if not usuario_id or not material_id:
            messagebox.showerror("Error", "Debe ingresar ambos IDs")
            return
        
        resultado, mensaje = self.biblioteca.realizar_prestamo(usuario_id, material_id)
        
        if resultado:
            info = f"Préstamo realizado con éxito:\n"
            info += f"ID Préstamo: {mensaje['id']}\n"
            info += f"Fecha Préstamo: {mensaje['fecha_prestamo']}\n"
            info += f"Fecha Devolución: {mensaje['fecha_devolucion']}"
        
            self.info_prestamo.config(text=info)
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente")
        
            # Actualizar información mostrada
            self.buscar_usuario(usuario_id)
            self.buscar_material(material_id)
        else:
            messagebox.showerror("Error", mensaje)
    
    def mostrar_registrar_devolucion(self):
        self.limpiar_pantalla()
        
        self.pantalla_actual = tk.Frame(self.root)
        self.pantalla_actual.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(self.pantalla_actual, text="Registrar Devolución", 
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Frame para lista de préstamos
        prestamos_container = tk.Frame(self.pantalla_actual)
        prestamos_container.pack(expand=True, fill='both', pady=10)
        
        # Lista de préstamos activos con scrollbar
        self.prestamos_tree = ttk.Treeview(prestamos_container)
        self.prestamos_tree.pack(side='left', expand=True, fill='both')
        
        scrollbar = ttk.Scrollbar(prestamos_container, orient="vertical", command=self.prestamos_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.prestamos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurar columnas
        self.prestamos_tree['columns'] = ("ID", "Usuario", "Material", "Fecha Préstamo", "Fecha Devolución")
        self.prestamos_tree.column("#0", width=0, stretch=tk.NO)
        
        for col in self.prestamos_tree['columns']:
            self.prestamos_tree.column(col, anchor='w', width=120)
            self.prestamos_tree.heading(col, text=col, anchor='w')
        
        self.prestamos_tree.column("Usuario", width=150)
        self.prestamos_tree.column("Material", width=200)
        
        # Llenar con préstamos activos
        for p in self.biblioteca.datos['prestamos']:
            if not p['devuelto']:
                usuario = next((u for u in self.biblioteca.datos['usuarios'] if u['id'] == p['usuario_id']), {})
                material = next((m for m in self.biblioteca.datos['materiales'] if m['id'] == p['material_id']), {})
                
                self.prestamos_tree.insert('', 'end', values=(
                    p['id'],
                    usuario.get('nombre', 'N/A'),
                    material.get('titulo', 'N/A'),
                    p['fecha_prestamo'],
                    p['fecha_devolucion']
                ))
        
        # Controles de_dev
        control_frame = tk.Frame(self.pantalla_actual)
        control_frame.pack(fill='x', pady=10)
        
        tk.Label(control_frame, text="ID Préstamo:").pack(side='left', padx=5)
        
        self.prestamo_id_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.prestamo_id_var, width=15).pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="Registrar Devolución", command=self.registrar_devolucion).pack(side='left', padx=5)
        
        # Información de penalización
        self.info_penalizacion = tk.Label(self.pantalla_actual, text="", font=('Arial', 12))
        self.info_penalizacion.pack(pady=10)
        
        self.boton_volver(self.pantalla_actual)
        
    def registrar_devolucion(self):
        prestamo_id = self.prestamo_id_var.get()
        
        if not prestamo_id:
            messagebox.showerror("Error", "Ingrese el ID del préstamo")
            return
        
        resultado, mensaje = self.biblioteca.registrar_devolucion(prestamo_id)
        
        if resultado:
            # Verificar si hubo penalización
            prestamo = next((p for p in self.biblioteca.datos['prestamos'] if p['id'] == prestamo_id), {})
            usuario = next((u for u in self.biblioteca.datos['usuarios'] if u['id'] == prestamo.get('usuario_id', '')), {})
            
            if usuario.get('penalizaciones', 0) > 0:
                self.info_penalizacion.config(
                    text=f"Penalización aplicada: ${usuario['penalizaciones']}"
                )
            
            messagebox.showinfo("Éxito", "Devolución registrada correctamente")
            self.mostrar_registrar_devolucion()  # Actualizar lista
        else:
            messagebox.showerror("Error", mensaje)
    
    def mostrar_admin_catalogo(self):
        self.limpiar_pantalla()
        self.pantalla_actual = tk.Frame(self.root)
        self.pantalla_actual.pack(expand=True, fill='both', padx=20, pady=20)
        tk.Label(self.pantalla_actual, text="Administrar Catálogo", font=('Arial', 18, 'bold')).pack(pady=10)

        # Pestañas
        notebook = ttk.Notebook(self.pantalla_actual)
        notebook.pack(expand=True, fill='both')

        # Pestaña agre_mat
        add_frame = tk.Frame(notebook)
        notebook.add(add_frame, text="Agregar Material")

        # Contenedor principal para el formulario
        form_container = tk.Frame(add_frame)
        form_container.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(form_container, text="Agregar Nuevo Material", font=('Arial', 14)).pack(pady=10)

        # Frame para contr_bas
        basic_frame = tk.Frame(form_container)
        basic_frame.pack(fill='x', pady=10)

        # Tipo de material
        tk.Label(basic_frame, text="Tipo:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.tipo_var = tk.StringVar()
        tipos = ttk.Combobox(basic_frame, textvariable=self.tipo_var, values=["Libro", "Revista", "MaterialDigital"])
        tipos.current(0)
        tipos.grid(row=0, column=1, sticky='we', padx=5, pady=5)
        tipos.bind("<<ComboboxSelected>>", self.actualizar_formulario_material)

        # Título 
        tk.Label(basic_frame, text="Título:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.titulo_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.titulo_var).grid(row=1, column=1, sticky='we', padx=5, pady=5)
        
        # Frame para campos dinámicos
        self.campos_dinamicos = tk.Frame(form_container)
        self.campos_dinamicos.pack(fill='x', pady=10)
        ttk.Button(form_container, text="Agregar", command=self.agregar_material).pack(pady=10)
        # Inicializar campos dinámicos
        self.actualizar_formulario_material()
        
        # Pestaña Lista de Materiales
        list_frame = tk.Frame(notebook)
        notebook.add(list_frame, text="Lista de Materiales")
        
        # Contenedor para la lista_mat
        list_container = tk.Frame(list_frame)
        list_container.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Treeview para materiales con scrollbar
        self.materiales_tree = ttk.Treeview(list_container)
        self.materiales_tree.pack(side='left', expand=True, fill='both')
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.materiales_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.materiales_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurar columnas
        self.materiales_tree['columns'] = ("ID", "Tipo", "Título", "Autor", "Género", "Estado")
        self.materiales_tree.column("#0", width=0, stretch=tk.NO)
        
        for col in self.materiales_tree['columns']:
            self.materiales_tree.column(col, anchor='w', width=120)
            self.materiales_tree.heading(col, text=col, anchor='w')
            
        self.materiales_tree.column("Título", width=200)
        self.materiales_tree.column("Autor", width=150)
        
        # Llenar con materiales
        for material in self.biblioteca.datos['materiales']:
            self.materiales_tree.insert('', 'end', values=(
                material['id'],
                material.get('tipo', 'N/A'),
                material.get('titulo', 'N/A'),
                material.get('autor', 'N/A'),
                material.get('genero', 'N/A'),
                material.get('estado', 'N/A')
            ))
            
        # Botón para eliminar material
        ttk.Button(list_frame, text="Eliminar Material Seleccionado", command=self.eliminar_material).pack(pady=10)
        self.boton_volver(self.pantalla_actual)
        
    def actualizar_formulario_material(self, event=None):
        # Limpiar frame de campos dinámicos
        for widget in self.campos_dinamicos.winfo_children():
            widget.destroy()
        tipo = self.tipo_var.get()
        row = 0
        if tipo == "Libro":
            tk.Label(self.campos_dinamicos, text="Autor:").grid(row=row, column=0, sticky='e', padx=5, pady=5)
            self.autor_var = tk.StringVar()
            ttk.Entry(self.campos_dinamicos, textvariable=self.autor_var).grid(row=row, column=1, sticky='we', padx=5, pady=5)
            row += 1
            tk.Label(self.campos_dinamicos, text="Género:").grid(row=row, column=0, sticky='e', padx=5, pady=5)
            self.genero_var = tk.StringVar()
            ttk.Entry(self.campos_dinamicos, textvariable=self.genero_var).grid(row=row, column=1, sticky='we', padx=5, pady=5)
        elif tipo == "Revista":
            # No mostramos campos aquí, se pedirán con diálogos
            pass
        elif tipo == "MaterialDigital":
            # No mostramos campos aquí, solo el enlace se pedirá con diálogo
            pass
        
    def agregar_material(self):
        tipo = self.tipo_var.get()
        titulo = self.titulo_var.get()
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio")
            return
        datos = {'titulo': titulo}
        if tipo == "Libro":
            datos['autor'] = self.autor_var.get()
            datos['genero'] = self.genero_var.get()
        elif tipo == "Revista":
            datos['edicion'] = simpledialog.askstring("Edición", "Ingrese el número de edición:")
            datos['periodicidad'] = simpledialog.askstring("Periodicidad", "Ingrese la periodicidad (mensual, trimestral, etc.):")
        elif tipo == "MaterialDigital":
            datos['tipo_archivo'] = "PDF"  
            datos['enlace_descarga'] = simpledialog.askstring("Enlace", "Ingrese el enlace de descarga simulado:")
        if tipo != "MaterialDigital":
            sucursales = [s['nombre'] for s in self.biblioteca.datos['sucursales']]
            if sucursales:
                seleccion = simpledialog.askstring("Sucursal", "Seleccione sucursal:\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(sucursales)))
                if seleccion and seleccion.isdigit() and 0 < int(seleccion) <= len(sucursales):
                    datos['sucursal_id'] = self.biblioteca.datos['sucursales'][int(seleccion)-1]['id']
        self.biblioteca.agregar_material(tipo, **datos)
        messagebox.showinfo("Éxito", "Material agregado correctamente")
        self.mostrar_admin_catalogo()
        
    def eliminar_material(self):
        seleccion = self.materiales_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un material")
            return
        material_id = self.materiales_tree.item(seleccion[0])['values'][0]
        material = next((m for m in self.biblioteca.datos['materiales'] if m['id'] == material_id), None)
        if material and material['estado'] == 'prestado':
            messagebox.showerror("Error", "No se puede eliminar un material prestado")
            return
        self.biblioteca.datos['materiales'] = [m for m in self.biblioteca.datos['materiales'] if m['id'] != material_id]
        self.biblioteca.guardar_datos('materiales')
        messagebox.showinfo("Éxito", "Material eliminado")
        self.mostrar_admin_catalogo()  
    
    def mostrar_registrar_usuario(self):
        self.limpiar_pantalla()
        self.pantalla_actual = tk.Frame(self.root)
        self.pantalla_actual.pack(expand=True, fill='both', padx=20, pady=20)
        tk.Label(self.pantalla_actual, text="Registrar Usuario", font=('Arial', 18, 'bold')).pack(pady=10)
        form_frame = tk.Frame(self.pantalla_actual)
        form_frame.pack(fill='x', pady=10)
        tk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.usuario_nombre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.usuario_nombre_var).grid(row=0, column=1, sticky='we', padx=5, pady=5)
        tk.Label(form_frame, text="Contacto:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.usuario_contacto_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.usuario_contacto_var).grid(row=1, column=1, sticky='we', padx=5, pady=5)
        ttk.Button(form_frame, text="Registrar", command=self.registrar_usuario).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame para lista_us
        usuarios_container = tk.Frame(self.pantalla_actual)
        usuarios_container.pack(expand=True, fill='both', pady=10)
        
        # Treeview con scrollbar
        self.usuarios_tree = ttk.Treeview(usuarios_container)
        self.usuarios_tree.pack(side='left', expand=True, fill='both')
        scrollbar = ttk.Scrollbar(usuarios_container, orient="vertical", command=self.usuarios_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.usuarios_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurar columnas
        self.usuarios_tree['columns'] = ("ID", "Nombre", "Contacto", "Fecha Registro", "Penalizaciones", "Materiales Prestados")
        self.usuarios_tree.column("#0", width=0, stretch=tk.NO)
        for col in self.usuarios_tree['columns']:
            self.usuarios_tree.column(col, anchor='w', width=120)
            self.usuarios_tree.heading(col, text=col, anchor='w')
        self.usuarios_tree.column("Nombre", width=150)
        self.usuarios_tree.column("Contacto", width=150)
        
        # Llenar con usuarios
        for usuario in self.biblioteca.datos['usuarios']:
            self.usuarios_tree.insert('', 'end', values=(
                usuario['id'],
                usuario['nombre'],
                usuario['contacto'],
                usuario.get('fecha_registro', 'N/A'),
                f"${usuario['penalizaciones']}",
                len(usuario['materiales_prestados'])
            ))
        self.boton_volver(self.pantalla_actual)
    
    def registrar_usuario(self):
        nombre = self.usuario_nombre_var.get()
        contacto = self.usuario_contacto_var.get()
        if not nombre or not contacto:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        self.biblioteca.registrar_usuario(nombre, contacto)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        self.mostrar_registrar_usuario()  
    
    def mostrar_reportes(self):
        self.limpiar_pantalla()
        self.pantalla_actual = tk.Frame(self.root)
        self.pantalla_actual.pack(expand=True, fill='both', padx=20, pady=20)
        tk.Label(self.pantalla_actual, text="Reportes", font=('Arial', 18, 'bold')).pack(pady=10)
        # Frame para estadísticas
        stats_frame = tk.Frame(self.pantalla_actual)
        stats_frame.pack(fill='x', pady=10)
        # Total materiales
        total_materiales = len(self.biblioteca.datos['materiales'])
        tk.Label(stats_frame, text=f"Total Materiales: {total_materiales}", font=('Arial', 12)).pack(anchor='w', pady=5)
        
        # Materiales por tipo
        tipos = {}
        for mat in self.biblioteca.datos['materiales']:
            tipo = mat['tipo']
            tipos[tipo] = tipos.get(tipo, 0) + 1
        for tipo, cantidad in tipos.items():
            tk.Label(stats_frame, text=f"{tipo}: {cantidad}", font=('Arial', 11)).pack(anchor='w', padx=20)
        # Materiales prestados
        materiales_prestados = len([m for m in self.biblioteca.datos['materiales'] if m['estado'] == 'prestado'])
        tk.Label(stats_frame, text=f"Materiales Prestados: {materiales_prestados}", font=('Arial', 12)).pack(anchor='w', pady=5)
        # Usuarios registrados
        total_usuarios = len(self.biblioteca.datos['usuarios'])
        tk.Label(stats_frame, text=f"Usuarios Registrados: {total_usuarios}", font=('Arial', 12)).pack(anchor='w', pady=5)
        # Usuarios con penalizaciones
        usuarios_penalizados = len([u for u in self.biblioteca.datos['usuarios'] if u['penalizaciones'] > 0])
        tk.Label(stats_frame, text=f"Usuarios Penalizados: {usuarios_penalizados}", font=('Arial', 12)).pack(anchor='w', pady=5)
        # Préstamos vencidos
        hoy = datetime.now().strftime("%Y-%m-%d")
        prestamos_vencidos = len([p for p in self.biblioteca.datos['prestamos'] if not p['devuelto'] and p['fecha_devolucion'] < hoy])
        tk.Label(stats_frame, text=f"Préstamos Vencidos: {prestamos_vencidos}", font=('Arial', 12)).pack(anchor='w', pady=5)
        self.boton_volver(self.pantalla_actual)
        
    # Iniciar/finalizar programa
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaFrontend(root)
    root.mainloop()