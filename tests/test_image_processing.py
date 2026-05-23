from pathlib import Path
from si_image_processing.pipelines.image_processing.nodes import process_image


def test_process_image():
    # Esto crea la carpeta temporal en GitHub si no existe
    output_dir = Path("data/03_primary")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    result = process_image(
        "data/01_raw/marte.jpg",
        "data/03_primary/test_output.jpg"
    )

    assert result is not None
