import os
from typing import Optional
from pathlib import Path
from datetime import datetime


class ElevenLabsMcpError(Exception):
    pass

def make_error(error_text: str):
    raise ElevenLabsMcpError(error_text)

def is_file_writeable(path: Path) -> bool:
    if path.exists():
        return os.access(path, os.W_OK)
    parent_dir = path.parent
    return os.access(parent_dir, os.W_OK)

def make_output_file(
    tool: str, text: str, output_path: Path, extension: str, full_id: bool = False
) -> Path:
    id = text if full_id else text[:5]

    output_file_name = f"{tool}_{id.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    return output_path / output_file_name

def make_output_path(
    output_directory: Optional[str], base_path: Optional[str] = None
) -> Path:
    output_path = None
    if output_directory is None:
        output_path = Path.home() / "Desktop"
    elif not os.path.isabs(output_directory) and base_path:
        output_path = Path(os.path.expanduser(base_path)) / Path(output_directory)
    else:
        output_path = Path(os.path.expanduser(output_directory))
    if not is_file_writeable(output_path):
        make_error(f"Directory ({output_path}) is not writeable")
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        make_error(f"Permission denied creating directory ({output_path})")
    return output_path