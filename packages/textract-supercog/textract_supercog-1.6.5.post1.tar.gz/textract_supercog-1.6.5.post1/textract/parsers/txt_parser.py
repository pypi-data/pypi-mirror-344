from .utils import BaseParser

class Parser(BaseParser):
    """Parse ``.txt`` files"""

    def extract(self, filename, **kwargs):
        try:
            # Try UTF-8 first
            with open(filename, encoding='utf-8') as stream:
                return stream.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 which will never fail
            with open(filename, encoding='latin-1') as stream:
                return stream.read()
