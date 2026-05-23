import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

logger = logging.getLogger(__name__)

# Mapeo de filtros disponibles
AVAILABLE_FILTERS = {
    "FIND_EDGES": ImageFilter.FIND_EDGES,
    "EMBOSS": ImageFilter.EMBOSS,
    "BLUR": ImageFilter.BLUR,
    "CONTOUR": ImageFilter.CONTOUR,
    "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
    "SHARPEN": ImageFilter.SHARPEN,
}


def process_image(
    input_path: str,
    output_path: str,
    rotation_angle: int = 0,
    filter_name: str = "EMBOSS",
    watermark_text: str = "",
) -> Image.Image:
    """Procesa una imagen aplicando rotación dinámica, filtro configurable y marca de agua.

    Args:
        input_path: Ruta del archivo de imagen de entrada.
        output_path: Ruta donde guardar la imagen procesada.
        rotation_angle: Ángulo de rotación en grados (default: 0).
        filter_name: Nombre del filtro a aplicar (default: "EMBOSS").
        watermark_text: Texto de la marca de agua (default: "").

    Returns:
        La imagen procesada como objeto PIL.Image.

    Raises:
        FileNotFoundError: Si el archivo de entrada no existe.
        ValueError: Si el ángulo de rotación o filtro no son válidos.
    """
    # 1. Validar que el archivo de entrada existe
    if not Path(input_path).exists():
        logger.error(f"Archivo de entrada no encontrado: {input_path}")
        raise FileNotFoundError(f"El archivo {input_path} no existe.")

    # 2. Validar que el ángulo es un número
    if not isinstance(rotation_angle, (int, float)):
        logger.error(f"Ángulo inválido: {rotation_angle}")
        raise ValueError("El ángulo de rotación debe ser un número.")

    # 3. Validar que el filtro existe
    if filter_name not in AVAILABLE_FILTERS:
        logger.error(f"Filtro no disponible: {filter_name}")
        available = ", ".join(AVAILABLE_FILTERS.keys())
        raise ValueError(f"Filtro '{filter_name}' no disponible. Opciones: {available}")

    # 4. Crear directorio de salida si no existe
    output_dir = Path(output_path).parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directorio creado: {output_dir}")

    try:
        # 5. Cargar la imagen
        logger.info(f"Cargando imagen desde: {input_path}")
        image = Image.open(input_path)
        logger.info(f"Imagen cargada. Tamaño: {image.size}")

        # 6. Rotación dinámica
        if rotation_angle != 0:
            logger.info(f"Aplicando rotación de {rotation_angle} grados.")
            image = image.rotate(rotation_angle, expand=True)

        # 7. Aplicar filtro seleccionado
        logger.info(f"Aplicando filtro: {filter_name}")
        image = image.filter(AVAILABLE_FILTERS[filter_name])

        # 8. Agregar marca de agua personalizada
        if watermark_text:
            logger.info(f"Agregando marca de agua: {watermark_text}")
            draw = ImageDraw.Draw(image)
            width, height = image.size
            # Posición dinámica en centro inferior para mejor visibilidad
            position = (max(10, width // 2 - 150), max(10, height - 30))
            draw.text(position, watermark_text, fill="white")

        # 9. Guardar la imagen procesada
        logger.info(f"Guardando imagen procesada en: {output_path}")
        image.save(output_path)
        logger.info("Imagen guardada exitosamente.")

        return image

    except Exception as e:
        logger.error(f"Error al procesar la imagen: {str(e)}")
        raise
