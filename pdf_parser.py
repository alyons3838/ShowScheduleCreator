"""
PDF Parser for extracting show schedule data from bland PDFs
"""
import pdfplumber
from typing import List, Dict, Any
import re


class ShowScheduleParser:
    """Parse show schedules from PDF files"""

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
        r'^\s*[■●▪•]\s*$',  # Bullet points alone
        r'^\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}\s*(?:AM|PM)$',  # Just timestamps
        r'2005 W 76 Country',  # Address
        r'Branson, Missouri \d{5}',  # City/zip
    ]

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.raw_text = ""
        self.schedule_data = []

    def extract_text(self) -> str:
        """Extract all text from the PDF"""
        with pdfplumber.open(self.pdf_path) as pdf:
            text_parts = []
            for page in pdf.pages:
                text_parts.append(page.extract_text())
            self.raw_text = "\n".join(text_parts)
        return self.raw_text

    def _is_junk_line(self, line: str) -> bool:
        """Check if a line matches junk patterns and should be filtered"""
        for pattern in self.JUNK_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def parse_schedule(self) -> List[Dict[str, Any]]:
        """
        Parse the schedule data from extracted text.
        Handles format: "TIME Show Name TIME TIME" by extracting time/show pairs.
        """
        if not self.raw_text:
            self.extract_text()

        lines = self.raw_text.split('\n')
        schedule_items = []

        # Pattern for time with optional AM/PM
        time_pattern = r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?'

        for line in lines:
            line = line.strip()

            # Skip empty lines and junk
            if not line or self._is_junk_line(line):
                continue

            # Skip lines that are just numbers, bullets, or very short
            if len(line) < 5 or re.match(r'^[\d\s■●▪•]+$', line):
                continue

            # Find all times in the line
            times = re.findall(time_pattern, line)

            if times:
                # Remove all times from the line to get the show name
                show_name = line
                for time in times:
                    show_name = show_name.replace(time, '', 1)

                # Clean up the show name
                show_name = re.sub(r'^[#\d\s■●▪•]+', '', show_name)  # Remove leading numbers/bullets
                show_name = re.sub(r'\s+', ' ', show_name).strip()  # Normalize whitespace

                # Skip if show name is empty or too short after cleaning
                if len(show_name) < 3:
                    continue

                # Use the first time found
                primary_time = times[0].strip()

                schedule_items.append({
                    'time': primary_time,
                    'show': show_name,
                    'details': '',
                    'raw_line': line
                })

        # Remove duplicates while preserving order
        seen = set()
        unique_items = []
        for item in schedule_items:
            # Create a key from time and show name
            key = (item['time'], item['show'])
            if key not in seen:
                seen.add(key)
                unique_items.append(item)

        self.schedule_data = unique_items
        return unique_items

    def _parse_as_list(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Fallback parser that treats content as a simple list"""
        items = []
        for line in lines:
            line = line.strip()
            if line and len(line) > 3 and not self._is_junk_line(line):
                items.append({
                    'show': line,
                    'time': '',
                    'details': '',
                    'raw_line': line
                })
        return items

    def get_title(self) -> str:
        """Extract a title from the document (usually first significant line)"""
        if not self.raw_text:
            self.extract_text()

        lines = self.raw_text.split('\n')
        for line in lines:
            line = line.strip()
            # Skip junk and find first meaningful line
            if len(line) > 5 and not self._is_junk_line(line):
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
