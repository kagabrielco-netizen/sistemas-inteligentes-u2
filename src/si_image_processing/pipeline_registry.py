from typing import Dict
from kedro.pipeline import Pipeline
# Aquí importamos el pipeline que creaste en la subcarpeta
from si_image_processing.pipelines.image_processing import pipeline as img_proc

def register_pipelines() -> Dict[str, Pipeline]:
    image_pipeline = img_proc.create_pipeline()
    return {
        # Esto le dice a Kedro que corra este pipeline por defecto
        "__default__": image_pipeline,
        "image_processing": image_pipeline
    }