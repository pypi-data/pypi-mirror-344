from pathlib import Path
from typing import Generator
from urllib.parse import urlparse
import hashlib
import frontmatter
from chercher import Document, hookimpl


@hookimpl
def ingest(uri: str) -> Generator[Document, None, None]:
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme != "file":
        return

    path = Path(parsed_uri.path).resolve()
    if not path.exists() or not path.is_file() or path.suffix != ".md":
        return

    with path.open("rb") as f:
        content = f.read()
        hash = hashlib.sha256(content)
        post = frontmatter.loads(content.decode("utf-8"))

    yield Document(
        uri=path.as_uri(),
        title=path.stem,
        body=post.content,
        hash=hash.hexdigest(),
        metadata=post.metadata,
    )
