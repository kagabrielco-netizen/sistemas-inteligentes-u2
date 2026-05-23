from kedro.pipeline import Pipeline, node

from .nodes import process_image


def create_pipeline(**kwargs):

    return Pipeline(
        [
            node(
                func=process_image,
                inputs=["params:input_path", "params:output_path"],
                outputs="processed_image",
                name="process_image_node",
            )
        ]
    )
