from pathlib import Path
from typing import Generator
from urllib.parse import urlparse
import hashlib
from chercher import Document, hookimpl


def normalize_uri(uri: str) -> Path:
    if uri.startswith("file://"):
        parsed_uri = urlparse(uri)
        return Path(parsed_uri.path).resolve()

    return Path(uri)


@hookimpl()
def ingest(uri: str) -> Generator[Document, None, None]:
    path = normalize_uri(uri)
    if not path.exists() or not path.is_file() or path.suffix != ".txt":
        return

    with path.open("rb") as f:
        content = f.read()
        hash = hashlib.sha256(content)

    yield Document(
        uri=path.as_uri(),
        title=path.stem,
        body=content.decode("utf-8"),
        hash=hash.hexdigest(),
        metadata={},
    )
