"""
PDF Parser for extracting show schedule data from bland PDFs
"""
import pdfplumber
from typing import List, Dict, Any
import re


class ShowScheduleParser:
    """Parse show schedules from PDF files"""

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

    def parse_schedule(self) -> List[Dict[str, Any]]:
        """
        Parse the schedule data from extracted text.
        This is a flexible parser that looks for common patterns in show schedules.
        """
        if not self.raw_text:
            self.extract_text()

        lines = self.raw_text.split('\n')
        schedule_items = []

        # Common patterns for show schedules
        # This will need to be adjusted based on your actual PDF format
        time_pattern = r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)'

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Look for time patterns (common in schedules)
            time_match = re.search(time_pattern, line)
            if time_match:
                time = time_match.group(1)
                # The rest of the line is likely the show name/description
                show_info = line.replace(time, '').strip()

                # Try to extract additional details from following lines
                details = []
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    # If next line doesn't have a time, it's probably additional info
                    if not re.search(time_pattern, next_line) and next_line:
                        details.append(next_line)

                schedule_items.append({
                    'time': time,
                    'show': show_info,
                    'details': ' '.join(details),
                    'raw_line': line
                })

        # If no time-based items found, try to extract as simple list
        if not schedule_items:
            schedule_items = self._parse_as_list(lines)

        self.schedule_data = schedule_items
        return schedule_items

    def _parse_as_list(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Fallback parser that treats content as a simple list"""
        items = []
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:  # Skip very short lines
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
            if len(line) > 5:  # First substantial line is likely the title
                return line
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
