from kedro.pipeline import Pipeline, node, pipeline

from .nodes import process_image


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=process_image,
                inputs=[
                    "params:input_path",
                    "params:output_path",
                    "params:rotation_angle",
                    "params:filter_name",
                    "params:watermark_text",
                ],
                outputs="processed_image",
                name="process_image_node",
            ),
        ]
    )
