from pathlib import Path


def generate_path(mode, filename: str) -> str:
    root = Path.cwd()
    paths = {
        "model": root / "upscale" / filename,
        "input": root / "files" / "input_images" / filename,
        "output": root / "files" / "output_images" / filename,
        "test": root / "files" / "test_file" / filename,
    }
    if mode not in paths:
        raise ValueError("Unsupported mode.")

    return str(paths.get(mode, root))


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description
