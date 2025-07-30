# Calculadora Profesional en Python

## 📜 Descripción

Este proyecto es una aplicación de calculadora de escritorio funcional, robusta y profesional, desarrollada **únicamente con la librería estándar de Python**. La interfaz gráfica está construida con `tkinter` y la lógica de cálculo se gestiona mediante un motor de parsing propio para evitar el uso de la función `eval()`, que es insegura.

## ✨ Funcionalidades

### Operaciones Soportadas
- **Básicas**: Suma (`+`), Resta (`-`), Multiplicación (`*`), División (`/`).
- **Avanzadas**: Potencia (`^`), Raíz Cuadrada (`sqrt()`), Porcentaje (`%`).
- **Trigonométricas**: `sin()`, `cos()`, `tan()`.
- **Logarítmicas**: Logaritmo natural (`ln()`), Logaritmo base 10 (`log()`).
- **Constantes**: Pi (`pi`), Euler (`e`).
- **Control**: Paréntesis `()`, borrado (`C`, `CE`, `DEL`) y cambio de signo (`+/-`).

### Funcionalidades Adicionales
- **Historial de Operaciones**: Una ventana muestra los últimos cálculos. Haz clic en una entrada para reutilizar la expresión.
- **Funciones de Memoria**: `M+`, `M-`, `MR`, `MC` para almacenar, recuperar y limpiar un valor en memoria. Un indicador `M` aparece en pantalla cuando la memoria está en uso.

## 🛠️ Requisitos Técnicos

- **Lenguaje**: Python 3.x
- **Dependencias**: Ninguna. Solo la librería estándar de Python.
- **Interfaz Gráfica**: `tkinter`.
- **Seguridad**: Se ha implementado un parser basado en el **algoritmo Shunting-yard** para procesar las expresiones matemáticas de forma segura.

## 🚀 Cómo Ejecutar la Aplicación

1.  Asegúrate de tener Python 3 instalado.
2.  Clona o descarga este repositorio.
3.  Navega hasta el directorio raíz del proyecto (`calculadora_project/`).
4.  Ejecuta el siguiente comando en tu terminal:

    ```bash
    python main.py
    ```

## 🧪 Cómo Ejecutar las Pruebas

Las pruebas unitarias para el motor de cálculo (`engine.py`) se encuentran en el directorio `tests/`. Para ejecutarlas, usa el siguiente comando desde el directorio raíz:

```bash
python -m tests.test_engine
```