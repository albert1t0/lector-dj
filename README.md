# Lector-DJ: Automatización de Clasificación de Documentos

Este proyecto utiliza Inteligencia Artificial (Gemini 1.5 Flash) para automatizar el reconocimiento y clasificación de diversos tipos de documentos legales y financieros.

## Características

- **Reconocimiento Multimodal**: Utiliza **Gemini 1.5 Flash** para identificar IDs, facturas, recibos de impuestos y registros de propiedad directamente desde imágenes y PDFs.
- **Aprendizaje por Ejemplos (Few-shot)**: El sistema aprende de los documentos que coloques en la carpeta `examples/`.
- **Soporte PDF**: Conversión automática de páginas de PDF a imágenes para análisis visual.
- **Procesamiento Seguro**: Sistema de extracción de ZIPs con protección contra vulnerabilidades de "Directory Traversal".
- **Salida Estructurada**: Genera un archivo `results.json` con la categoría, confianza y razonamiento de la IA para cada documento.

## Requisitos Previos

- Python 3.10+
- Una API Key de Google Gemini.
- **Tesseract OCR** (opcional, para soporte extendido) y **poppler-utils** (necesario para la conversión de PDFs).

### Configuración de API

1. Crea un archivo `.env` basado en el `.env.example`.
2. Agrega tu `GOOGLE_API_KEY`.

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

1. **Entrenamiento (Few-shot)**: Crea subcarpetas en `examples/` con el nombre de la categoría y coloca ejemplos reales:
   - `examples/IDENTITY_DOCUMENT/cedula_ejemplo.jpg`
   - `examples/INVOICE/factura_ejemplo.png`
2. **Procesamiento**: Coloca los documentos a procesar en la carpeta `input/` o proporciona un archivo `.zip`.
3. **Ejecución**:
   ```bash
   python main.py --input ./input
   ```

Los resultados se guardarán en `output/results.json`.

## Plan de Implementación

El detalle del plan de desarrollo se encuentra en [implementation_plan.md](./implementation_plan.md).
