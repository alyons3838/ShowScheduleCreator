# Sample Show Schedule Format

This document describes the expected format for input PDFs.

## Expected Structure

The PDF parser is designed to work with show schedules that follow common patterns:

### Time-Based Schedules

```
Show Schedule for Saturday, December 16, 2024
Branson, Missouri

8:00 AM    Breakfast & Registration
           Continental breakfast in the lobby

10:00 AM   Morning Show - "Country Music Legends"
           Main Theater

12:30 PM   Lunch Break

2:00 PM    Afternoon Show - "Magic & Comedy"
           Side Stage Theater

5:00 PM    Dinner Service

7:30 PM    Evening Show - "Grand Ole Opry"
           Main Theater
```

### Simple List Format

```
Today's Shows
Branson Entertainment Schedule

Country Music Legends - Main Theater
Magic & Comedy Hour - Side Stage
The Grand Ole Opry Experience - Main Theater
Comedy Night Special - Comedy Club
Christmas Spectacular - Grand Theater
```

## Parsing Features

The parser will:
- Extract times (12:00 AM/PM format)
- Identify show names and descriptions
- Preserve event details
- Handle multiple formats gracefully

## Tips for Best Results

1. **Consistent Formatting**: Keep similar items formatted the same way
2. **Clear Times**: Use standard time format (10:00 AM, 2:30 PM)
3. **Show Names**: Keep show names on the same line as times
4. **Additional Details**: Place details on following lines

## What Gets Branded

The output PDF will include:
- Thousand Hills Vacations header with logo colors
- Branded color scheme (Red, Yellow, Green)
- Professional table formatting
- Decorative accent bars
- Contact information footer

## Testing Your PDF

1. Upload your current show schedule PDF
2. Check the preview to ensure all information was captured
3. If data is missing, the PDF may need reformatting
4. Contact support if you need help adjusting the parser
