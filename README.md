# Subir proyecto de Semáforos a la rama `Universidad` en GitHub

A continuación se presentan los pasos completos para organizar tu proyecto en una carpeta local y subirlo a tu repositorio en la rama **Universidad**.
Integrantes
## - Julian Rincon 
## - Paula Caballero 
---

Este proyecto modela el comportamiento emergente de sistemas de tráfico urbano, donde los semáforos se autoorganizan basándose en reglas locales sin control centralizado. El sistema incorpora elementos caóticos para estudiar cómo pequeñas perturbaciones pueden generar comportamientos complejos e impredecibles.

## 1. Clonar el repositorio en tu computador
Abre **Git Bash** o la terminal de tu preferencia y clona tu repositorio (cambia la URL por la tuya):

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

Esto creará una carpeta con el nombre de tu repositorio.

---

## 2. Entrar en el repositorio y crear la carpeta del proyecto
```bash
cd TU_REPOSITORIO
mkdir Semaforos_Parcial
```

---

## 3. Mover los archivos del proyecto a la nueva carpeta
Si tus archivos están en `Descargas/Semaforos Int`, ejecuta (en Git Bash):

```bash
mv ~/Downloads/"Semaforos Int"/* Semaforos_Parcial/
```

>  Nota: en Windows, si usas **PowerShell**, el comando es:
```powershell
Move-Item "$env:USERPROFILE\Downloads\Semaforos Int\*" .\Semaforos_Parcial```

---

## 4. Cambiar a la rama `Universidad`
```bash
git checkout Universidad
```

Si la rama no existe localmente, primero ejecútalo así:
```bash
git fetch origin
git checkout -b Universidad origin/Universidad
```

---

## 5. Agregar y confirmar los cambios
```bash
git add Semaforos_Parcial
git commit -m "Agregando proyecto de semáforos en carpeta Semaforos_Parcial"
```

---
---

## 6. Estrucutura del proyecto
```bash
📁 Proyecto/
├── 📄 main.py                    # Aplicación principal con interfaz gráfica
├── 📄 grid_saso.py              # Visualización del grid de tráfico
├── 📄 smoke_test.py             # Pruebas básicas del sistema
├── 📄 README.md                 # Este archivo
└── 📁 Back/                     # Módulo principal del sistema
    ├── 📄 __init__.py           # Inicializador del paquete
    ├── 📄 config.py             # Configuración del sistema
    ├── 📄 controller.py         # Controlador principal con reglas
    ├── 📄 queues.py             # Manejo de vehículos y colas
    ├── 📄 chaos.py              # Motor de caos (Ecuaciones de Lorenz)
    ├── 📄 metrics.py            # Recopilación de métricas
    └── 📄 run_loop.py           # Loop de simulación 
```

---
## 7. Subir los cambios al repositorio remoto
```bash
git push origin Universidad
```

---

 Con esto tu proyecto de semáforos quedará guardado en la carpeta **Semaforos_Parcial** dentro de la rama **Universidad**.

 IMPORTANTE - Importaciones y Ubicación de Archivos

# ADVERTENCIA CRÍTICA:
 La estructura de directorios y las importaciones son EXTREMADAMENTE SENSIBLES. Cualquier cambio en la ubicación de los archivos o en las rutas de importación puede causar fallos en la ejecución.

 # Requisitos de ubicación
  - Mantén la estructura exacta como se muestra arriba
  - NO muevas archivos entre directorios
  - El archivo Back/__init__.py debe existir (puede estar vacío)
  - Ejecuta SIEMPRE desde el directorio raíz del proyecto
  - Python debe reconocer Back/ como un paquete
# Parametros

d (Distancia lejana): Rango de detección de vehículos acercándose
n (Umbral rojo): Número mínimo de vehículos para cambiar semáforo
u (Tiempo mínimo): Tiempo mínimo que debe estar en verde

# Pestañas de Información

Estadísticas: Métricas en tiempo real del sistema
Reglas: Contadores y estado de aplicación de las 6 reglas
Análisis Caos: Entropía, variabilidad y complejidad del sistema

# Regla 1: Contador de Vehículos en Rojo
Si hay ≥ n vehículos esperando en rojo Y 
el otro semáforo lleva ≥ u tiempo en verde
→ CAMBIAR el semáforo
# Regla 2: Tiempo Mínimo en Verde
Un semáforo debe permanecer verde al menos u unidades de tiempo
antes de poder cambiar
# Regla 3: Evitar Cambios Innecesarios
Si hay ≤ m vehículos cerca (distancia r) de un semáforo verde
→ NO CAMBIAR (dejar que pasen)
# Regla 4: Dar Paso a Vehículos en Rojo
Si no hay vehículos acercándose a la luz verde (distancia d) Y
hay vehículos esperando en rojo
→ CAMBIAR para dar paso
# Regla 5: Evitar Bloqueos
Si hay vehículos detenidos más allá de la intersección (distancia e)
→ CAMBIAR para evitar congestión
