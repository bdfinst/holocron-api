"""CSP Middleware."""
from flask import Response

# list is not all-inclusive, some hashes are considered unsafe
# unsafe hashes require the 'unsafe-hashes' keyword be present
flasgger_inline_style_hashes = [
    "'sha256-1fdCXxcHyanQoxIfyXxjg5BQQ8b9Dm8zrCS6yEdEbrg='",
    "'sha256-b3IrgBVvuKx/Q3tmAi79fnf6AFClibrz/0S5x1ghdGU='",
]

DEFAULT_SRC = "default-src 'self';"
CONNECT_SRC = "connect-src 'self';"
SCRIPT_SRC = "script-src 'self' 'sha256-txrSP/AT5SJ8pKSlYt1LR/a8kXKc0Wjviyc4p3+g4jw=';"
FORM_ACTION = "form-action 'self';"
STYLE_SRC = (
    "style-src 'self' https://fonts.gstatic.com https://fonts.googleapis.com "
    + " ".join(flasgger_inline_style_hashes)
    + ";"
)
FONT_SRC = "font-src 'self' https://fonts.gstatic.com;"
IMG_SRC = "img-src 'self' data: w3.org/sv/2000;"
FRAME_OPTIONS = "frame-ancestors 'none';"

CSP = (
    DEFAULT_SRC
    + CONNECT_SRC
    + SCRIPT_SRC
    + FORM_ACTION
    + STYLE_SRC
    + FONT_SRC
    + IMG_SRC
    + FRAME_OPTIONS
)


def set_csp(response: Response) -> Response:
    """Set CSP header."""
    response.headers["Content-Security-Policy"] = CSP
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
