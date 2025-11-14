"""
Branded PDF Generator for Thousand Hills Vacations
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from typing import List, Dict, Any
import os
from config import BRAND_COLORS_RGB, PRIMARY_FONT, PRIMARY_FONT_BOLD, BRAND_NAME, BRAND_TAGLINE


class BrandedPDFGenerator:
    """Generate beautifully branded PDFs for show schedules"""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.width, self.height = letter
        self.styles = self._create_styles()

    def _create_styles(self):
        """Create custom paragraph styles matching brand guidelines"""
        styles = getSampleStyleSheet()

        # Custom title style
        styles.add(ParagraphStyle(
            name='BrandTitle',
            parent=styles['Heading1'],
            fontName=PRIMARY_FONT_BOLD,
            fontSize=24,
            textColor=colors.Color(*BRAND_COLORS_RGB['primary_red']),
            alignment=TA_CENTER,
            spaceAfter=12
        ))

        # Custom heading style
        styles.add(ParagraphStyle(
            name='BrandHeading',
            parent=styles['Heading2'],
            fontName=PRIMARY_FONT_BOLD,
            fontSize=16,
            textColor=colors.Color(*BRAND_COLORS_RGB['charcoal_black']),
            spaceAfter=10
        ))

        # Custom body style
        styles.add(ParagraphStyle(
            name='BrandBody',
            parent=styles['Normal'],
            fontName=PRIMARY_FONT,
            fontSize=11,
            textColor=colors.Color(*BRAND_COLORS_RGB['charcoal_black']),
            spaceAfter=8
        ))

        # Tagline style
        styles.add(ParagraphStyle(
            name='BrandTagline',
            parent=styles['Normal'],
            fontName=PRIMARY_FONT,
            fontSize=12,
            textColor=colors.Color(*BRAND_COLORS_RGB['golf_green']),
            alignment=TA_CENTER,
            spaceAfter=20
        ))

        return styles

    def generate_schedule(self, schedule_data: Dict[str, Any], metadata: Dict[str, str]):
        """Generate a branded show schedule PDF"""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        story = []

        # Add header
        story.extend(self._create_header(metadata))

        # Add schedule content
        story.extend(self._create_schedule_table(schedule_data))

        # Add footer
        story.extend(self._create_footer())

        # Build the PDF with custom page template
        doc.build(story, onFirstPage=self._add_decorative_elements,
                  onLaterPages=self._add_decorative_elements)

    def _create_header(self, metadata: Dict[str, str]) -> List:
        """Create the branded header"""
        elements = []

        # Add logo if available
        logo_path = os.path.join('static', 'logo.png')
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2.5*inch, height=None, kind='proportional')
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 0.2*inch))
            except Exception:
                pass  # If logo fails to load, continue without it

        # Brand name
        brand_title = Paragraph(f"<b>{BRAND_NAME}</b>", self.styles['BrandTitle'])
        elements.append(brand_title)

        # Tagline
        tagline = Paragraph(BRAND_TAGLINE, self.styles['BrandTagline'])
        elements.append(tagline)

        # Add a spacer
        elements.append(Spacer(1, 0.2*inch))

        # Document title
        title = metadata.get('title', 'Show Schedule')
        title_para = Paragraph(f"<b>{title}</b>", self.styles['BrandHeading'])
        elements.append(title_para)

        # Date and venue if available
        if metadata.get('date'):
            date_para = Paragraph(f"<i>{metadata['date']}</i>", self.styles['BrandBody'])
            elements.append(date_para)

        if metadata.get('venue'):
            venue_para = Paragraph(f"<i>{metadata['venue']}</i>", self.styles['BrandBody'])
            elements.append(venue_para)

        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_schedule_table(self, schedule_data: Dict[str, Any]) -> List:
        """Create a beautifully formatted schedule table"""
        elements = []

        # Check if we have table data
        if not schedule_data or schedule_data.get('type') != 'table':
            return [Paragraph("No schedule data available", self.styles['BrandBody'])]

        headers = schedule_data.get('headers', [])
        rows = schedule_data.get('rows', [])

        if not headers or not rows:
            return [Paragraph("No schedule data available", self.styles['BrandBody'])]

        # Build table data with Paragraph objects for proper formatting
        table_data = []

        # Add header row (days of the week)
        header_row = []
        for header in headers:
            header_row.append(Paragraph(f"<b>{header}</b>", self.styles['BrandBody']))
        table_data.append(header_row)

        # Add data rows (times and shows)
        for row in rows:
            formatted_row = []
            for i, cell in enumerate(row):
                # First column is usually the time - make it bold
                if i == 0:
                    formatted_row.append(Paragraph(f"<b>{cell}</b>", self.styles['BrandBody']))
                else:
                    # Wrap text for better formatting
                    formatted_row.append(Paragraph(cell if cell else '', self.styles['BrandBody']))
            table_data.append(formatted_row)

        # Calculate column widths dynamically based on number of columns
        num_cols = len(headers)
        available_width = 6.5 * inch

        if num_cols > 0:
            # First column (time) gets 1 inch, rest divide remaining space
            if num_cols == 1:
                col_widths = [available_width]
            else:
                first_col_width = 1.0 * inch
                remaining_width = available_width - first_col_width
                other_col_width = remaining_width / (num_cols - 1)
                col_widths = [first_col_width] + [other_col_width] * (num_cols - 1)
        else:
            col_widths = None

        # Create and style the table
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        # Apply brand styling
        table.setStyle(TableStyle([
            # Header row styling (days of the week)
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(*BRAND_COLORS_RGB['primary_red'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.Color(*BRAND_COLORS_RGB['white'])),
            ('FONTNAME', (0, 0), (-1, 0), PRIMARY_FONT_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),

            # First column (times) styling
            ('BACKGROUND', (0, 1), (0, -1), colors.Color(*BRAND_COLORS_RGB['highlight_yellow'], alpha=0.2)),
            ('FONTNAME', (0, 1), (0, -1), PRIMARY_FONT_BOLD),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),

            # Data cells styling
            ('BACKGROUND', (1, 1), (-1, -1), colors.Color(*BRAND_COLORS_RGB['white'])),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.Color(*BRAND_COLORS_RGB['charcoal_black'])),
            ('FONTNAME', (1, 1), (-1, -1), PRIMARY_FONT),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),

            # Alternating row colors (skip header)
            ('ROWBACKGROUNDS', (1, 1), (-1, -1),
             [colors.Color(*BRAND_COLORS_RGB['white']),
              colors.Color(0.95, 0.95, 0.95)]),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(*BRAND_COLORS_RGB['gray'])),
            ('BOX', (0, 0), (-1, -1), 2, colors.Color(*BRAND_COLORS_RGB['primary_red'])),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_footer(self) -> List:
        """Create branded footer"""
        elements = []

        footer_text = (
            f"<i>For reservations and information, visit ThousandHills.com or call 1-800-BRANSON</i>"
        )
        footer_para = Paragraph(footer_text, self.styles['BrandBody'])

        elements.append(Spacer(1, 0.2*inch))
        elements.append(footer_para)

        return elements

    def _add_decorative_elements(self, canvas_obj, doc):
        """Add decorative branded elements to each page"""
        canvas_obj.saveState()

        # Top accent bar
        canvas_obj.setFillColor(colors.Color(*BRAND_COLORS_RGB['highlight_yellow']))
        canvas_obj.rect(0, self.height - 10, self.width, 10, fill=True, stroke=False)

        # Bottom accent bar
        canvas_obj.setFillColor(colors.Color(*BRAND_COLORS_RGB['golf_green']))
        canvas_obj.rect(0, 0, self.width, 10, fill=True, stroke=False)

        # Page number
        canvas_obj.setFillColor(colors.Color(*BRAND_COLORS_RGB['charcoal_black']))
        canvas_obj.setFont(PRIMARY_FONT, 9)
        page_num = canvas_obj.getPageNumber()
        text = f"Page {page_num}"
        canvas_obj.drawRightString(self.width - 0.75*inch, 0.5*inch, text)

        canvas_obj.restoreState()
