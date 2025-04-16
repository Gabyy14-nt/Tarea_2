## Tarea_2
Sistema de Biblioteca Digital
## Descripción
Sistema de gestión de biblioteca digital con funcionalidades para préstamos, devoluciones, catálogo y usuarios.
 
## Autoejecutables 
El archivo BibliotecaDigital_Instalador.exe es el WinRAR autocomprimido. 

## Instalación para los archivos .py
1. Clonar el repositorio o descargar los archivos:
2. Instalar las dependencias:
3. Asegurarse de tener los siguientes archivos en el mismo directorio:
- Biblio_front.py
- Biblio_back.py
- imagen_fondo.png 
- fondo.ico
## Configuración
- Modificar las rutas de imágenes en el código si es necesario
- El sistema creará automáticamente los archivos JSON para almacenar datos

## *Explicación Técnica del Sistema de Biblioteca Digital*
## Arquitectura
El sistema sigue un patrón MVC (Modelo-Vista-Controlador) con:
- **Frontend**: Biblio_front.py (Interfaz gráfica)
- **Backend**: Biblio_back.py (Lógica de negocio)
- **Modelo**: Datos almacenados en archivos JSON

### Módulo de Materiales
- Gestión de libros, revistas y materiales digitales
- Búsqueda por múltiples criterios
- Estados: Disponible/Prestado

### Módulo de Usuarios
- Registro de usuarios
- Historial de préstamos
- Sistema de penalizaciones

### Módulo de Préstamos
- Registro de préstamos y devoluciones
- Cálculo automático de fechas de devolución
- Control de materiales prestados

### Módulo de Reportes
- Estadísticas de uso
- Materiales más prestados
- Usuarios con más actividad

## Flujo de Datos
1. La interfaz captura las acciones del usuario
2. El controlador procesa las solicitudes
3. El backend manipula los datos
4. Los cambios se persisten en archivos JSON
5. La interfaz muestra los resultados actualizados

## Persistencia
Los datos se guardan en archivos JSON:
- materiales.json
- usuarios.json
- prestamos.json
