# reometroGUI
Este es un proyecto de interfaz gráfica de usuario (GUI) desarrollado en **Python** utilizando la librería **Tkinter** y **Matplotlib** para el control y visualización de datos de un **Reómetro Eritrocitário**. El software simula la comunicación con un controlador y procesa datos de ensayo de forma local.

-----

### 🌟 Características Principales

  * **Interfaz Gráfica Intuitiva:** Desarrollada con Tkinter para facilitar la operación del reómetro.
  * **Modos de Ensayo:** Soporte para ensayos de **Carga**, **Descarga**, **Dinámico** y **Homogeneización**.
  * **Configuración de Parámetros:** Selección de **Revoluciones por Minuto (RPM)** (17, 35, 70) y **Frecuencia Dinámica (Fr)** (0.5 Hz, 1.0 Hz, 1.5 Hz).
  * **Visualización de Datos:** Graficación en tiempo real (simulada) de los ejes **R** y **T** mediante Matplotlib, guardando la imagen como `input.png`.
  * **Simulación de Conexión:** Manejo del estado de conexión/desconexión con el controlador.
  * **Exportación de Datos:** Funcionalidad para guardar los datos de los ensayos en formato CSV.

-----

### 💻 Requisitos

Para ejecutar esta aplicación, necesitarás tener instalado Python junto con las siguientes librerías:

  * **Tkinter** (Generalmente incluida en la instalación estándar de Python).
  * **Pillow (PIL)**: Para el manejo de imágenes en la GUI.
  * **Matplotlib**: Para la generación de gráficos.

#### Instalación de Dependencias

```bash
pip install Pillow matplotlib
```

-----

### 🚀 Uso

#### 1\. Estructura de Archivos

Asegúrate de tener los siguientes archivos en el mismo directorio que `GUI_v_0.50.py`:

| Archivo | Descripción |
| :--- | :--- |
| `GUI_v_0.50.py` | El script principal de la aplicación. |
| `carga.csv` | Datos simulados para el ensayo de Carga. |
| `descarga.csv` | Datos simulados para el ensayo de Descarga. |
| `05.csv`, `10.csv`, `15.csv` | Datos simulados para ensayos Dinámicos (0.5, 1.0, 1.5 Hz). |
| `rojo.png`, `rojo_inicio.png` | Archivos de imagen para el ícono y la pantalla inicial. |

> **Nota:** El archivo `input.csv` se genera automáticamente como una copia temporal de los archivos de ensayo.

#### 2\. Ejecución

Ejecuta el script de Python desde tu terminal:

```bash
python GUI_v_0.50.py
```

#### 3\. Flujo Operacional

1.  **Conectar:** Selecciona el radio button **"conectar"** para simular la conexión con el controlador. La mayoría de los botones de ensayo requieren esta conexión.
2.  **Configurar:** Utiliza los radio buttons para seleccionar las **Revoluciones del motor** (RPM) y la **Frecuencia de ensayo dinámico** (Fr) deseadas.
3.  **Iniciar Ensayo:** Haz clic en los botones **Carga**, **Descarga**, **Dinámico** o **Homogeneizar**.
      * Los ensayos de Carga, Descarga y Dinámico cargarán los datos del CSV correspondiente, los procesarán (`Tomar_datos`), generarán un gráfico (`Dibujar`) y lo mostrarán en la GUI.
4.  **Parar:** Usa el botón **"Parar Motor"** (rojo) para detener la simulación del ensayo.
5.  **Exportar:** El botón **"Exportar"** permite guardar los datos del último ensayo graficado.

-----

### ⚙️ Notas de Desarrollo

  * La comunicación real por puerto serie (tokens como `EC7000`, `EO7005`) está simulada. Para una implementación física, los métodos `carga`, `descarga`, etc., deberían incluir la lógica de envío de estos *tokens* al controlador.
  * El manejo de errores en la lectura de CSV está implementado para la conversión de formatos numéricos (reemplazando `,` por `.`).
  * Los datos de los ejes **X** y **Y** se almacenan en las listas globales `X`, `Y` y `T` (tiempo).

-----

### 🤝 Contribuciones

Si deseas contribuir, puedes:

  * Implementar la **comunicación real** por puerto serie (por ejemplo, con la librería `pyserial`).
  * Mejorar el manejo de errores y la validación de archivos CSV.
  * Refinar la interfaz gráfica y la interactividad de los gráficos.
