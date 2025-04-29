from dataclasses import dataclass, field
from typing import Optional, List, Literal, Dict, Any, TypeAlias, ByteString

from pygments.formatters import HtmlFormatter

MediaType = Literal["screen", "print"]


@dataclass
class MarkdownOptions:
    """
    Configuration options for the python-markdown library.
    """
    # A list of extensions
    extensions: List[Any] = field(default_factory=list)
    # A dictionary of configuration settings for extensions
    extension_configs: Dict[str, Any] = field(default_factory=dict)
    # Format of output. Default: "html"
    output_format: Literal["html", "xhtml"] = field(default="xhtml")
    # Length of tabs in the source. Default: 4
    tab_length: int = field(default=4)


@dataclass
class BaseConfig:
    # Base directory to be saved by the file server.
    base_dir: str = field(default_factory=str)
    # Encoding of the markdown file, default is "utf-8".
    md_file_encoding: str = field(default="utf-8")
    # Encoding of the stylesheet, default is "utf-8".
    stylesheet_file_encoding: str = field(default="utf-8")
    # List of css files to use for styling.
    stylesheets: List[str] = field(default_factory=list)
    # Custom css styles.
    css: str = field(default_factory=str)
    # List of scripts to load into the page.
    scripts: List[str] = field(default_factory=list)
    # Name of the HTML Document
    document_title: str = field(default_factory=str)
    # List of class for the body tag
    body_class: List[str] = field(default_factory=list)
    # Media type to emulate the page with.
    page_media_type: MediaType = field(default="screen")
    # Highlight.js stylesheet to use (without the .css extension).
    # @see https://github.com/isagalaev/highlight.js/tree/master/src/styles
    highlight_style: str = field(default_factory=str)
    # Options for the python-markdown library.
    markdown_options: MarkdownOptions = field(default_factory=MarkdownOptions)
    # PDF options for Puppeteer.
    # @see https://pptr.dev/api/puppeteer.pdfoptions
    pdf_options: Dict[str, Any] = field(default_factory=dict)
    # Launch options for Puppeteer.
    # @see https://pptr.dev/browsers-api/browsers.launchoptions/
    launch_options: Dict[str, Any] = field(default_factory=dict)
    # If True, open chromium with devtools instead of saving the pdf.
    # This is meant for development only, to inspect the rendered HTML.
    devtools: bool = field(default=False)
    # Port to run the local server on.
    port: Optional[int] = field(default_factory=int)
    # Description path for the output file(include the extension).
    dest: Optional[str] = field(default_factory=str)


class PdfConfig(BaseConfig):
    # If True, save the html file instead of the pdf output, default is False.
    as_html: Optional[bool] = False


class HtmlConfig(BaseConfig):
    # If True, save the html file instead of the pdf output, default is True.
    as_html: bool = True


@dataclass
class BaseOutput:
    file_name: str = field(default_factory=str)


class PdfOutput(BaseOutput):
    content: ByteString = field(default_factory=ByteString)


class HtmlOutput(BaseOutput):
    content: str = field(default_factory=str)


Config: TypeAlias = PdfConfig | HtmlConfig
Output: TypeAlias = PdfOutput | HtmlOutput


def get_default_pdf_config():
    pygments_style = "friendly"
    pygments_css = HtmlFormatter(style=pygments_style).get_style_defs(".highlight")
    default_css = """
           body { font-family: Arial, sans-serif; margin: 10mm; }
           h1, h2, h3 { color: #333; }
           h1 { font-size: 24px; }
           h2 { font-size: 18px; }
           h3 { font-size: 16px; }
           body { font-size: 13px; }
           pre { padding: 10px; border-radius: 5px; }
           pre { padding: 10px; border-radius: 5px; }
           table { border-collapse: collapse; width: 100%; margin: 1em 0; border: 1px solid #dfdfdf; }
           th, td { border: 1px solid #dfdfdf; padding: 4px; text-align: left; font-size: 13px; }
           th { background-color: #ffffff; color: #333; font-weight: bold; text-align: center; }
           tr:nth-child(odd) { background-color: #f5f5f5; }
           tr:nth-child(even) { background-color: #ffffff; }
       """
    css_content = f"{pygments_css}\n{default_css}"
    return PdfConfig(
        css=css_content,
        pdf_options={
            "format": "A4",
            "printBackground": True,
        },
        markdown_options=MarkdownOptions(
            extensions=["tables", "fenced_code", "codehilite"],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "guess_lang": False,
                    "use_pygments": True,
                    "pygments_style": pygments_style,
                }
            },
            output_format="html",
            tab_length=4
        )
    )
