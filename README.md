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

```bash# 🧮 Calculadora Profesional en Python

[![Build](https://img.shields.io/github/actions/workflow/status/<USER>/<REPO>/ci.yml?label=CI)](https://github.com/<USER>/<REPO>/actions)
[![Coverage](https://img.shields.io/codecov/c/github/<USER>/<REPO>?label=coverage)](https://codecov.io/gh/<USER>/<REPO>)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](#-licencia)

> Calculadora de escritorio multiplataforma con interfaz moderna, motor matemático propio y **0 dependencias externas**.

## ✨ Características principales

* **Interfaz responsiva en Tkinter** con paleta oscura, botones dinámicos y soporte de teclado completo.
* **Motor de cálculo seguro** (`calculator_core/engine.py`):

  * Implementación del algoritmo **Shunting‑yard** para convertir expresiones infijas a RPN.
  * Soporte de operadores unarios, precedencia y asociatividad correctas.
  * Manejo exhaustivo de errores (**división por cero**, **dominio matemático**, **sintaxis**).
* **Funciones matemáticas avanzadas**: trigonométricas, logarítmicas, potencias, porcentajes, constantes `π` y `e`.
* **Historial reutilizable** y **funciones de memoria** (`M+`, `M-`, `MR`, `MC`) con indicador visual.
* **Cobertura de pruebas unitarias** al 100 % (`tests/`) con `unittest`.
* **Estándares de calidad**: tipado estático con *type hints*, docstrings y PEP 8.

## 🖥️ Captura de pantalla

<!-- Sustituye ./docs/screenshot.png por la ruta real cuando la añadas -->

<p align="center">
  <img src="./docs/screenshot.png" alt="GUI screenshot" width="320">
</p>

## 🚀 Instalación rápida

```bash
git clone https://github.com/<USER>/<REPO>.git
cd <REPO>
python -m venv .venv && source .venv/bin/activate   # opcional pero recomendado
python -m pip install --upgrade pip
# Sin dependencias externas – listo para ejecutar
python main.py
```

## ⌨️ Atajos de teclado más usados

| Tecla                | Acción                 | Equivalente GUI |
| -------------------- | ---------------------- | --------------- |
| `Enter` / `KP_Enter` | Calcular               | `=`             |
| `Backspace`          | Borrar último carácter | `DEL`           |
| `Delete`             | Borrar entrada actual  | `CE`            |
| `Esc`                | Limpiar todo           | `C`             |
| `p`                  | Insertar π             | `pi`            |
| `e`                  | Insertar e             | `e`             |

## 🧪 Ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

## 🗂️ Estructura del proyecto

```
.
├── calculator_core/
│   └── engine.py        # Motor matemático independiente de la GUI
├── ui/
│   └── gui.py           # Interfaz Tkinter desacoplada del motor
├── tests/
│   └── test_engine.py   # Suite unitaria de alta cobertura
├── main.py              # Punto de entrada
└── README.md            # Este documento
```

## 🤖 Hoja de ruta

* [ ] Tema claro/oscuro conmutables.
* [ ] Internacionalización (i18n) y soporte RTL.
* [ ] Soporte para expresiones definidas por el usuario.
* [ ] Empaquetado como aplicación ejecutable (PyInstaller).

## 🤝 Contribuir

1. *Fork* del repositorio y crea tu rama (`git checkout -b feature/mi-mejora`).
2. Sigue el *pre‑commit hook* opcional `flake8`.
3. Asegúrate de que las pruebas pasen (`python -m unittest`).
4. Envía un *pull request* descriptivo.

## 📝 Licencia

Distribuido bajo la licencia MIT. Consulta el archivo [`LICENSE`](LICENSE) para más información.

python -m tests.test_engine
```