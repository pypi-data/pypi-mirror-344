import os
from typing import Union

from yarl import URL

pathlike = Union[str, bytes, os.PathLike]
urllike = Union[str, URL]
