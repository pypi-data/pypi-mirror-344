from openpyxl import load_workbook
from .utils import BaseParser

class Parser(BaseParser):
    """Extract text from Excel files (.xlsx)
    """

    def extract(self, filename, **kwargs):
        workbook = load_workbook(filename, data_only=True)
        output = "\n"
        
        for worksheet in workbook.worksheets:
            for row in worksheet.rows:
                new_output = []
                for cell in row:
                    value = cell.value
                    if value is None:
                        value = ""  # Preserve blank cells
                    elif isinstance(value, (int, float)):
                        value = str(value)
                    new_output.append(value)
                # Only skip rows if they are entirely empty
                if any(val != "" for val in new_output):
                    output += ' '.join(str(item) for item in new_output) + '\n'
                    
        return output