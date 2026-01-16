# Lector-DJ: Automatización de Clasificación de Documentos

Este proyecto utiliza Inteligencia Artificial (Gemini 1.5 Flash) para automatizar el reconocimiento y clasificación de diversos tipos de documentos legales y financieros.

## Características

- **Reconocimiento Multimodal**: Identifica IDs, facturas, recibos de impuestos y registros de propiedad directamente desde imágenes y PDFs.
- **Procesamiento Seguro**: Sistema de extracción de ZIPs con protección contra vulnerabilidades de "Directory Traversal".
- **Procesamiento por Lotes**: Escanea carpetas locales o archivos ZIP para procesar múltiples documentos a la vez.
- **Aprendizaje por Ejemplos (Few-shot)**: Utiliza documentos de referencia para mejorar la precisión en formatos específicos de un país.
- **Salida Estructurada**: Genera resultados en formato JSON para facilitar la integración con otros sistemas.
- **Basado en Calidad**: Incluye una suite de pruebas unitarias para garantizar la robustez del manejo de archivos.

## Requisitos Previos

- Python 3.10+
- Una API Key de Google Gemini.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <repo-url>
   cd lector-dj
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Coloca algunos ejemplos de documentos en la carpeta `examples/` para guiar al modelo.
2. Coloca los documentos a procesar en la carpeta `input/` o proporciona un archivo `.zip`.
3. Ejecuta el script principal:
   ```bash
   python main.py --input ./input
   ```

## Plan de Implementación

El detalle del plan de desarrollo se encuentra en [implementation_plan.md](./implementation_plan.md).
