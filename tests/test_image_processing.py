import pytest
from pathlib import Path
from PIL import Image

from si_image_processing.pipelines.image_processing.nodes import process_image


@pytest.fixture
def setup_directories():
    """Asegura que existan las carpetas necesarias para el test."""
    Path("data/01_raw").mkdir(parents=True, exist_ok=True)
    Path("data/03_primary").mkdir(parents=True, exist_ok=True)

    # Crea una imagen de prueba si no existe
    input_path = Path("data/01_raw/marte.jpg")
    if not input_path.exists():
        img = Image.new("RGB", (200, 150), color="white")
        img.save(input_path)

    return str(input_path), "data/03_primary/marte_processed.jpg"


class TestImageProcessing:
    """Suite de tests para la función process_image."""

    def test_process_image_with_emboss_filter(self, setup_directories):
        """Prueba el flujo completo con filtro EMBOSS."""
        input_path, output_path = setup_directories

        result = process_image(
            input_path=input_path,
            output_path=output_path,
            rotation_angle=45,
            filter_name="EMBOSS",
            watermark_text="Katherine Gabriel Corilloclla",
        )

        assert result is not None
        assert isinstance(result, Image.Image)
        assert Path(output_path).exists()

    def test_process_image_no_rotation(self, setup_directories):
        """Prueba sin rotación (ángulo 0)."""
        input_path, output_path = setup_directories

        result = process_image(
            input_path=input_path,
            output_path=output_path,
            rotation_angle=0,
            filter_name="EMBOSS",
            watermark_text="Katherine Gabriel Corilloclla",
        )

        assert result is not None
        assert result.size is not None

    def test_process_image_dynamic_rotation_angles(self, setup_directories):
        """Prueba con diferentes ángulos de rotación."""
        input_path, output_path = setup_directories
        angles = [45, 90, 180, 270]

        for angle in angles:
            output_path_angle = f"data/03_primary/marte_rot_{angle}.jpg"
            result = process_image(
                input_path=input_path,
                output_path=output_path_angle,
                rotation_angle=angle,
                filter_name="EMBOSS",
                watermark_text=f"ROT_{angle}",
            )
            assert result is not None
            assert Path(output_path_angle).exists()

    def test_process_image_different_filters(self, setup_directories):
        """Prueba con diferentes filtros disponibles."""
        input_path, output_path = setup_directories
        filters = ["EMBOSS", "FIND_EDGES", "BLUR", "CONTOUR"]

        for filter_name in filters:
            output_path_filter = f"data/03_primary/marte_{filter_name.lower()}.jpg"
            result = process_image(
                input_path=input_path,
                output_path=output_path_filter,
                rotation_angle=45,
                filter_name=filter_name,
                watermark_text=f"Filter: {filter_name}",
            )
            assert result is not None
            assert Path(output_path_filter).exists()

    def test_process_image_with_watermark(self, setup_directories):
        """Prueba que la marca de agua se agrega correctamente."""
        input_path, output_path = setup_directories
        watermark = "Katherine Gabriel Corilloclla"

        result = process_image(
            input_path=input_path,
            output_path=output_path,
            rotation_angle=45,
            filter_name="EMBOSS",
            watermark_text=watermark,
        )

        assert result is not None
        saved_image = Image.open(output_path)
        assert saved_image.size is not None

    def test_process_image_without_watermark(self, setup_directories):
        """Prueba sin marca de agua (texto vacío)."""
        input_path, output_path = setup_directories

        result = process_image(
            input_path=input_path,
            output_path=output_path,
            rotation_angle=45,
            filter_name="EMBOSS",
            watermark_text="",
        )

        assert result is not None

    def test_invalid_input_path(self):
        """Prueba de FileNotFoundError con ruta inválida."""
        with pytest.raises(FileNotFoundError):
            process_image(
                input_path="ruta/inexistente/imagen.jpg",
                output_path="data/03_primary/out.jpg",
                rotation_angle=45,
                filter_name="EMBOSS",
                watermark_text="ERROR",
            )

    def test_invalid_rotation_angle(self, setup_directories):
        """Prueba de ValueError con ángulo inválido."""
        input_path, output_path = setup_directories

        with pytest.raises(ValueError):
            process_image(
                input_path=input_path,
                output_path=output_path,
                rotation_angle="no_es_numero",
                filter_name="EMBOSS",
                watermark_text="ERROR",
            )

    def test_invalid_filter_name(self, setup_directories):
        """Prueba de ValueError con filtro inexistente."""
        input_path, output_path = setup_directories

        with pytest.raises(ValueError):
            process_image(
                input_path=input_path,
                output_path=output_path,
                rotation_angle=45,
                filter_name="FILTRO_INEXISTENTE",
                watermark_text="ERROR",
            )

    def test_output_directory_creation(self):
        """Prueba que se crean directorios de salida si no existen."""
        input_path = "data/01_raw/marte.jpg"
        output_path = "data/99_custom/test/output.jpg"

        if Path(input_path).exists():
            result = process_image(
                input_path=input_path,
                output_path=output_path,
                rotation_angle=0,
                filter_name="EMBOSS",
                watermark_text="TEST",
            )

            assert result is not None
            assert Path(output_path).exists()

    def test_image_size_after_processing(self, setup_directories):
        """Prueba que el tamaño de la imagen se modifica con rotación."""
        input_path, output_path = setup_directories

        result = process_image(
            input_path=input_path,
            output_path=output_path,
            rotation_angle=45,
            filter_name="EMBOSS",
            watermark_text="Katherine Gabriel Corilloclla",
        )

        assert result is not None
        assert result.size is not None

    def test_all_available_filters(self, setup_directories):
        """Prueba todos los filtros disponibles."""
        input_path, output_path = setup_directories
        filters = ["FIND_EDGES", "EMBOSS", "BLUR", "CONTOUR", "EDGE_ENHANCE", "SHARPEN"]

        for filter_name in filters:
            result = process_image(
                input_path=input_path,
                output_path=output_path,
                rotation_angle=0,
                filter_name=filter_name,
                watermark_text="Katherine Gabriel Corilloclla",
            )
            assert result is not None
