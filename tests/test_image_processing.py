from si_image_processing.pipelines.image_processing.nodes import process_image


def test_process_image():

    result = process_image(
        "data/01_raw/marte.jpg",
        "data/03_primary/test_output.jpg"
    )

    assert result is not None
    