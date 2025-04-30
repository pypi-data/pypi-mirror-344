from anyvec.processing.document import (
    extract_text_plain,
    extract_text_pdf,
    extract_text_docx_like,
    extract_text_ps,
    extract_text_epub,
    extract_text_xlsx,
    extract_text_xls,
    extract_text_ods,
    extract_text_odt,
    extract_text_odp,
    extract_text_pptx_like,
    extract_text_mammoth,
    extract_images_pdf,
    extract_images_docx,
    extract_images_pptx_like,
    extract_images_odt,
    extract_images_odp,
    extract_images_ods,
    extract_images_epub,
    extract_images_xlsx,
)

# Mapping: mime type -> (text extractor, image extractor)
mime_handlers = {
    # Word processing
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": (
        extract_text_docx_like,
        extract_images_docx,
    ),  # .docx
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template": (
        extract_text_mammoth,
        lambda _: [],
    ),  # .dotx
    "application/vnd.ms-word.template.macroenabled.12": (
        extract_text_mammoth,
        lambda _: [],
    ),  # .dotm
    "application/vnd.ms-word.document.macroenabled.12": (
        extract_text_mammoth,
        lambda _: [],
    ),  # .docm
    # Plain text and similar
    "text/plain": (extract_text_plain, lambda _: []),
    "application/rtf": (extract_text_plain, lambda _: []),
    "text/html": (extract_text_plain, lambda _: []),
    "text/markdown": (extract_text_plain, lambda _: []),
    # PDF
    "application/pdf": (extract_text_pdf, extract_images_pdf),
    # Spreadsheets
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": (
        extract_text_xlsx,
        extract_images_xlsx,
    ),  # .xlsx
    "application/vnd.ms-excel": (extract_text_xls, lambda _: []),  # .xls
    "application/vnd.oasis.opendocument.spreadsheet": (
        extract_text_ods,
        extract_images_ods,
    ),
    # Word processing
    "application/vnd.oasis.opendocument.text": (
        extract_text_odt,
        extract_images_odt,
    ),
    # Presentations
    "application/vnd.oasis.opendocument.presentation": (
        extract_text_odp,
        extract_images_odp,
    ),
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": (
        extract_text_pptx_like,
        extract_images_pptx_like,
    ),  # .pptx
    "application/vnd.openxmlformats-officedocument.presentationml.slideshow": (
        extract_text_pptx_like,
        extract_images_pptx_like,
    ),  # .ppsx
    "application/vnd.ms-powerpoint.presentation.macroenabled.12": (
        extract_text_pptx_like,
        extract_images_pptx_like,
    ),  # .pptm
    "application/epub+zip": (extract_text_epub, extract_images_epub),
    "application/postscript": (extract_text_ps, lambda _: []),
}

# Image mime types handled as base64
image_mime_types = {
    "image/png",
    "image/gif",
    "image/heic",
    "image/heif",
    "image/x-icon",
    "image/vnd.microsoft.icon",
    "image/avif",
    "image/bmp",
}

# Code file extensions (treated as plain text)
code_file_exts = (
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".kt",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rb",
    ".php",
    ".pl",
    ".sh",
    ".swift",
    ".scala",
    ".lua",
    ".f90",
    ".f95",
    ".erl",
    ".exs",
    ".bat",
    ".yml",
    ".yaml",
    ".json",
    ".xml",
    ".rst",
    ".sql",
    ".lisp",
    ".vb",
)
