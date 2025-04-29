import os
import uuid
from pathlib import Path
from typing import Optional, Literal, ByteString

os.environ["PYPPETEER_CHROMIUM_REVISION"] = "1265049"

from pyppeteer.browser import Browser

from md_to_pdf import types as cfg
from md_to_pdf.core import md_to_pdf as convert_md_to_pdf
from md_to_pdf.utils import system_utils

import pyppeteer


def default():
    pass


async def md_to_pdf(
        md_content: Optional[str] = None,
        md_file_path: Optional[Path | str] = None,
        output_type: Literal["file", "content"] = "file",
        config: Optional[cfg.Config] = cfg.get_default_pdf_config()
) -> Path | ByteString:
    if not md_content and not md_file_path:
        raise ValueError("MarkdownContent and MarkdownFilePath cannot both be None")

    if not config.base_dir:
        config.base_dir = str(md_file_path.parent if md_file_path else Path.cwd())
    if not config.port:
        config.port = system_utils.get_free_port()

    browser: Browser = await pyppeteer.launch(
        {
            "devtools": config.devtools,
            **config.launch_options
        }
    )
    if md_content is None and md_file_path is not None:
        md_content = md_file_path.read_text(encoding=config.md_file_encoding)
    pdf = await convert_md_to_pdf(md_content, config, browser)
    await browser.close()

    md_file_name = md_file_path.name if md_file_path is not None else str(uuid.uuid4()) + ".md"
    if output_type == "file":
        pdf_file_name = md_file_name.replace(".md", ".pdf")
        pdf_file_path = Path(config.base_dir) / pdf_file_name
        pdf_file_path.write_bytes(pdf)
        return pdf_file_path
    return pdf
