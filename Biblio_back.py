import json
from datetime import datetime, timedelta
import os

class BibliotecaBackend:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Archivos JSON 
        self.archivos = {
            'usuarios': os.path.join(self.data_dir, 'usuarios.json'),
            'bibliotecarios': os.path.join(self.data_dir, 'bibliotecarios.json'),
            'materiales': os.path.join(self.data_dir, 'materiales.json'),
            'prestamos': os.path.join(self.data_dir, 'prestamos.json'),
            'sucursales': os.path.join(self.data_dir, 'sucursales.json'),
            'penalizaciones': os.path.join(self.data_dir, 'penalizaciones.json')
        }
        
        self.datos = {}
        self.cargar_datos()
    
    def cargar_datos(self):
        for key, archivo in self.archivos.items():
            try:
                with open(archivo, 'r') as f:
                    self.datos[key] = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                if key == 'penalizaciones':
                    self.datos[key] = {}  
                else:
                    self.datos[key] = []  
                self.guardar_datos(key)
    
    def guardar_datos(self, clave=None):
        if clave:
            with open(self.archivos[clave], 'w') as f:
                json.dump(self.datos[clave], f, indent=4)
        else:
            for key in self.archivos:
                with open(self.archivos[key], 'w') as f:
                    json.dump(self.datos[key], f, indent=4)
    
    # Métodos para Usuarios
    def registrar_usuario(self, nombre, contacto, es_bibliotecario=False):
        tipo = 'bibliotecarios' if es_bibliotecario else 'usuarios'
        nuevo = {
            'id': str(len(self.datos[tipo]) + 1),
            'nombre': nombre,
            'contacto': contacto,
            'fecha_registro': datetime.now().strftime("%Y-%m-%d")
        }
        
        if not es_bibliotecario:
            nuevo['penalizaciones'] = 0
            nuevo['materiales_prestados'] = []
        
        self.datos[tipo].append(nuevo)
        self.guardar_datos(tipo)
        return nuevo
    
    def agregar_material(self, tipo, sucursal_id=None, **kwargs):
        material = {
            'id': str(len(self.datos['materiales']) + 1),
            'tipo': tipo,
            'estado': 'disponible',
            'fecha_ingreso': datetime.now().strftime("%Y-%m-%d"),
            **kwargs
        }
        if sucursal_id:
            material['sucursal_id'] = sucursal_id
        self.datos['materiales'].append(material)
        self.guardar_datos('materiales')
        return material
    
    def buscar_materiales(self, filtro=None, valor=None):
        if not filtro:
            return self.datos['materiales']
        return [m for m in self.datos['materiales'] 
                if str(valor).lower() in str(m.get(filtro, '')).lower()]
    
    # Métodos para Préstamos
    def realizar_prestamo(self, usuario_id, material_id):
        usuario = next((u for u in self.datos['usuarios'] if u['id'] == usuario_id), None)
        material = next((m for m in self.datos['materiales'] if m['id'] == material_id), None)
        
        if not usuario or not material:
            return False, "Usuario o material no encontrado"
        
        if material['estado'] != 'disponible':
            return False, "Material no disponible"
        
        if usuario['penalizaciones'] > 0:
            return False, "Usuario con penalizaciones pendientes"
        
        prestamo = {
            'id': str(len(self.datos['prestamos']) + 1),
            'usuario_id': usuario_id,
            'material_id': material_id,
            'fecha_prestamo': datetime.now().strftime("%Y-%m-%d"),
            'fecha_devolucion': (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            'devuelto': False
        }
        
        # Actualizar estados
        material['estado'] = 'prestado'
        usuario['materiales_prestados'].append(material_id)
        
        self.datos['prestamos'].append(prestamo)
        self.guardar_datos('prestamos')
        self.guardar_datos('materiales')
        self.guardar_datos('usuarios')
        
        return True, prestamo
    
    def registrar_devolucion(self, prestamo_id):
        prestamo = next((p for p in self.datos['prestamos'] if p['id'] == prestamo_id), None)
        if not prestamo:
            return False, "Préstamo no encontrado"
        
        if prestamo['devuelto']:
            return False, "Este préstamo ya fue devuelto"
        
        # Actualizar material
        material = next((m for m in self.datos['materiales'] if m['id'] == prestamo['material_id']), None)
        if material:
            material['estado'] = 'disponible'
        
        # Actualizar usuario
        usuario = next((u for u in self.datos['usuarios'] if u['id'] == prestamo['usuario_id']), None)
        if usuario:
            usuario['materiales_prestados'].remove(prestamo['material_id'])
            
            # Calcular penalización p/retraso
            fecha_devolucion = datetime.strptime(prestamo['fecha_devolucion'], "%Y-%m-%d")
            if datetime.now() > fecha_devolucion:
                dias_retraso = (datetime.now() - fecha_devolucion).days
                multa = dias_retraso * 5  # $5 por día de retraso
                usuario['penalizaciones'] += multa
                
                # Registrar penalización
                if prestamo['usuario_id'] not in self.datos['penalizaciones']:
                    self.datos['penalizaciones'][prestamo['usuario_id']] = []
                
                self.datos['penalizaciones'][prestamo['usuario_id']].append({
                    'fecha': datetime.now().strftime("%Y-%m-%d"),
                    'monto': multa,
                    'prestamo_id': prestamo_id,
                    'dias_retraso': dias_retraso
                })
        
        prestamo['devuelto'] = True
        prestamo['fecha_devolucion_real'] = datetime.now().strftime("%Y-%m-%d")
        
        self.guardar_datos('prestamos')
        self.guardar_datos('materiales')
        self.guardar_datos('usuarios')
        self.guardar_datos('penalizaciones')
        
        return True, prestamo