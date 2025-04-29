from typing import ByteString

import markdown
from commons_lang import object_utils
from pyppeteer.browser import Browser

from md_to_pdf.types import Config


def get_html(md_content: str, config: Config, ) -> str:
    md = markdown.markdown(
        md_content,
        extensions=config.markdown_options.extensions,
        extension_configs=config.markdown_options.extension_configs,
        output_format=config.markdown_options.output_format,
        tab_length=config.markdown_options.tab_length
    )
    return \
        f"""<!DOCTYPE html>
<html>
    <head>
        <title>{config.document_title}</title>
        <meta charset="utf-8">
        <style>{config.css}</style>
    </head>
    <body class={' '.join(config.body_class)}>
        {md}
    </body>
</html>"""


async def generate_output(html_content: str, config: Config, browser: Browser) -> ByteString:
    page = await browser.newPage()
    await page.setContent(html_content)
    pdf_bytes: ByteString = await page.pdf(**config.pdf_options)
    await page.close()
    return pdf_bytes


async def md_to_pdf(md_content: str, config: Config, browser: Browser) -> ByteString:
    pdf_configs = config.pdf_options
    header_template = object_utils.get(pdf_configs, "headerTemplate")
    footer_template = object_utils.get(pdf_configs, "footerTemplate")
    display_header_footer = object_utils.get(pdf_configs, "displayHeaderFooter")

    if (header_template or footer_template) and not display_header_footer:
        pdf_configs["displayHeaderFooter"] = True

    html_content: str = get_html(md_content, config)
    pdf_bytes: ByteString = await generate_output(html_content, config, browser)
    return pdf_bytes
