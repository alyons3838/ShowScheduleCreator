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

    def generate_schedule(self, schedule_data: List[Dict[str, Any]], metadata: Dict[str, str]):
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

    def _create_schedule_table(self, schedule_data: List[Dict[str, Any]]) -> List:
        """Create a beautifully formatted schedule table"""
        if not schedule_data:
            return [Paragraph("No schedule data available", self.styles['BrandBody'])]

        elements = []

        # Determine if we have time-based schedule
        has_times = any(item.get('time') for item in schedule_data)

        if has_times:
            # Create table with time column
            table_data = [['Time', 'Show', 'Details']]

            for item in schedule_data:
                row = [
                    Paragraph(f"<b>{item.get('time', '')}</b>", self.styles['BrandBody']),
                    Paragraph(item.get('show', ''), self.styles['BrandBody']),
                    Paragraph(item.get('details', ''), self.styles['BrandBody'])
                ]
                table_data.append(row)

            col_widths = [1.2*inch, 3*inch, 2.3*inch]
        else:
            # Create simple list table
            table_data = [['Show']]

            for item in schedule_data:
                row = [Paragraph(item.get('show', ''), self.styles['BrandBody'])]
                table_data.append(row)

            col_widths = [6.5*inch]

        # Create and style the table
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        # Apply brand styling
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(*BRAND_COLORS_RGB['primary_red'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.Color(*BRAND_COLORS_RGB['white'])),
            ('FONTNAME', (0, 0), (-1, 0), PRIMARY_FONT_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.Color(*BRAND_COLORS_RGB['white'])),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.Color(*BRAND_COLORS_RGB['charcoal_black'])),
            ('FONTNAME', (0, 1), (-1, -1), PRIMARY_FONT),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),

            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
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
