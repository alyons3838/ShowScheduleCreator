"""
PDF Parser for extracting show schedule data from table-based PDFs
"""
import pdfplumber
from typing import List, Dict, Any
import re


class ShowScheduleParser:
    """Parse show schedules from table-based PDF files"""

    # Patterns to filter out (header/footer junk)
    JUNK_PATTERNS = [
        r'SMASH',
        r'Find Orders & Quotes',
        r'Find Contacts by',
        r'Save On Branson',
        r'\(\d{3}\)\s*\d{3}-\d{4}',  # Phone numbers
        r'TMGStandard',
        r'v\d+\.\d+\.\d+',  # Version numbers
        r'^\d{5}\s+[A-Z]{2}$',  # Zip codes with state
        r'If you have questions',
        r'Don\'t hesitate',
        r'give us a call',
        r'2005 W 76 Country',  # Address
        r'Branson, Missouri \d{5}',  # City/zip
    ]

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.raw_text = ""
        self.table_data = None
        self.schedule_data = []

    def extract_text(self) -> str:
        """Extract all text from the PDF"""
        with pdfplumber.open(self.pdf_path) as pdf:
            text_parts = []
            for page in pdf.pages:
                text_parts.append(page.extract_text())
            self.raw_text = "\n".join(text_parts)
        return self.raw_text

    def _is_junk_text(self, text: str) -> bool:
        """Check if text matches junk patterns and should be filtered"""
        if not text or not isinstance(text, str):
            return True
        text = text.strip()
        if not text or len(text) < 2:
            return True
        for pattern in self.JUNK_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _clean_cell_text(self, text: str) -> str:
        """Clean up text from a table cell"""
        if not text:
            return ""

        text = str(text).strip()

        # Remove bullet points and numbers
        text = re.sub(r'^[#\d\s■●▪•]+', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def extract_table(self) -> List[List[str]]:
        """Extract table from PDF"""
        with pdfplumber.open(self.pdf_path) as pdf:
            all_tables = []

            for page in pdf.pages:
                # Extract tables from the page
                tables = page.extract_tables()

                if tables:
                    for table in tables:
                        # Filter out junk rows
                        clean_table = []
                        for row in table:
                            # Check if entire row is junk
                            row_text = ' '.join([str(cell) if cell else '' for cell in row])
                            if not self._is_junk_text(row_text):
                                # Clean individual cells
                                clean_row = [self._clean_cell_text(cell) if cell else '' for cell in row]
                                # Only keep rows with some content
                                if any(clean_row):
                                    clean_table.append(clean_row)

                        if clean_table:
                            all_tables.append(clean_table)

            # Return the first (usually largest) table
            if all_tables:
                # Sort by size and return largest
                all_tables.sort(key=lambda t: len(t) * len(t[0]) if t else 0, reverse=True)
                return all_tables[0]

            return []

    def parse_schedule(self) -> Dict[str, Any]:
        """
        Parse the schedule table from PDF.
        Returns a dictionary with headers and rows for table-based rendering.
        """
        table = self.extract_table()

        if not table or len(table) < 2:
            # Fallback to text extraction if no table found
            self.extract_text()
            return {
                'type': 'list',
                'headers': [],
                'rows': [],
                'data': []
            }

        # First row is typically headers (days of the week)
        headers = table[0]

        # Remaining rows are the schedule data
        rows = table[1:]

        # Store the structured data
        self.table_data = {
            'type': 'table',
            'headers': headers,
            'rows': rows
        }

        return self.table_data

    def get_title(self) -> str:
        """Extract a title from the document"""
        if not self.raw_text:
            self.extract_text()

        lines = self.raw_text.split('\n')
        for line in lines:
            line = line.strip()
            # Skip junk and find first meaningful line
            if len(line) > 5 and not self._is_junk_text(line):
                # Clean up the title
                title = re.sub(r'^\d{1,2}/\d{1,2}/\d{2,4}', '', line)  # Remove dates
                title = re.sub(r'\d{1,2}:\d{2}\s*(?:AM|PM)', '', title)  # Remove times
                title = title.strip()
                if len(title) > 3:
                    return title
        return "Show Schedule"

    def get_metadata(self) -> Dict[str, str]:
        """Extract metadata like dates, venue, etc."""
        if not self.raw_text:
            self.extract_text()

        metadata = {
            'title': self.get_title(),
            'date': self._extract_date(),
            'venue': 'Branson, Missouri'
        }
        return metadata

    def _extract_date(self) -> str:
        """Try to extract date information from the text"""
        # Common date patterns
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
            r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',
            r'(\d{1,2}-\d{1,2}-\d{2,4})'
        ]

        for pattern in date_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                return match.group(1)

        return ""
