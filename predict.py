import argparse
from typing import Optional

from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.settings import settings
import json
from cog import BasePredictor, Input, Path, BaseModel

configure_logging()

class ModelOutput(BaseModel):
    markdown: Path
    metadata: str

class Predictor(BasePredictor):
    def setup(self) -> None:
        self.model_lst = load_all_models()

    def predict(
        self,
        document: Path = Input(
            description="Provide your input file (PDF, EPUB, MOBI, XPS, FB2).",
            default=None,
        ),
        max_pages: int = Input(
            description="Provide the maximum number of pages to parse.",
            default=None
        ),
        parallel_factor: int = Input(
            description="Provide the parallel factor to use for OCR.",
            default=1
        ),
        lang: str = Input(
            description="Provide the language to use for OCR.",
            default="English",
            choices=["English", "Spanish", "Portuguese", "French", "German", "Russian"]
        ),
        dpi: int = Input(
            description="The DPI to use for OCR.",
            default=400
        ),
        enable_editor: bool = Input(
            description="Enable the editor model.",
            default=False
        ),
    ) -> ModelOutput:
        settings.DEFAULT_LANG = lang
        settings.OCR_DPI = dpi
        settings.ENABLE_EDITOR_MODEL = enable_editor
        text, meta = convert_single_pdf(document, self.model_lst, max_pages=max_pages, parallel_factor=parallel_factor)
        out = Path("out.md")
        out.write_text(text, encoding='utf-8')
        return ModelOutput(markdown=out, metadata=json.dumps(meta))

