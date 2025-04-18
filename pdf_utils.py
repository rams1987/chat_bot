import unicodedata
from fpdf import FPDF
import re # Import regex for more flexible subheading matching

def sanitize_text(text: str) -> str:
    # Replace special dash-like characters with regular dash
    text = text.replace('\\u2013', '-').replace('\\u2014', '-')
    # Normalize and strip other special characters
    return unicodedata.normalize("NFKD", text).encode("latin1", "ignore").decode("latin1")

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        title = 'Financial Advisory Report'
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180) # Blue frame
        self.set_fill_color(230, 230, 230) # Light gray background
        self.set_text_color(0, 0, 0) # Black text
        # Thickness of frame (e.g., 0.3 mm)
        self.set_line_width(0.3) # Make the line thinner
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)
        # Reset line width to default
        self.set_line_width(0.2)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def generate_pdf(user_context, insights):
    """Generate a more presentable PDF report with user context and latest insights."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- User Context Section --- 
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 220, 255) # Light blue background for section header
    pdf.cell(0, 10, 'Your Financial Profile', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11) # Use slightly smaller font for table content
    pdf.set_text_color(0, 0, 0) # Reset text color

    # Table properties
    col_width_label = 45
    col_width_value = 145 # Total width = 190
    line_height = 8
    table_border = 1 # Draw borders for table cells
    header_fill_color = (230, 230, 230) # Light gray for header (if we add one)
    # Use light blue and white for alternating rows
    row_fill_colors = [(220, 230, 255), (255, 255, 255)] # Light Blue and White
    row_index = 0

    # Table Header (Optional, but adds structure)
    # pdf.set_font('Arial', 'B', 11)
    # pdf.set_fill_color(*header_fill_color)
    # pdf.cell(col_width_label, line_height, 'Category', border=table_border, align='C', fill=True)
    # pdf.cell(col_width_value, line_height, 'Details', border=table_border, align='C', fill=True)
    # pdf.ln(line_height)

    profile_data = {
        "Age": str(user_context.get('age', 'N/A')),
        "Monthly Income": f"${float(user_context.get('income', 0)):,.2f}",
        "Monthly Expenses": sanitize_text(user_context.get('expenses', 'N/A')),
        "Financial Goals": sanitize_text(user_context.get('goals', 'N/A')),
        "Country": sanitize_text(user_context.get('country', 'N/A'))
    }

    for label, value in profile_data.items():
        # Set row fill color
        pdf.set_fill_color(*row_fill_colors[row_index % 2])
        row_index += 1

        # Remember starting position for multi_cell height calculation
        start_y = pdf.get_y()
        start_x = pdf.l_margin

        # Draw label cell (fixed height)
        pdf.set_font('Arial', 'B', 11) # Bold label
        pdf.cell(col_width_label, line_height, label, border=table_border, align='L', fill=True)
        
        # Draw value cell using multi_cell to handle wrapping
        pdf.set_font('Arial', '', 11) # Regular value
        pdf.set_xy(start_x + col_width_label, start_y) # Position for value cell
        pdf.multi_cell(col_width_value, line_height, value, border=table_border, align='L', fill=True)
        
        # Calculate height of the multi_cell
        # This is tricky as FPDF doesn't directly return height of multi_cell
        # We'll advance Y by the fixed line height for simplicity, assuming it won't drastically overflow.
        # For very long values, a more complex height calculation would be needed.
        pdf.set_y(start_y + line_height) # Move down for the next row
        pdf.set_x(start_x) # Reset X position

    pdf.ln(10)
    
    # --- Latest Insights Section --- 
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 220, 255) # Light blue background
    pdf.cell(0, 10, 'Latest Financial Insights', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0) # Reset text color

    # Process insights line by line for subheading formatting
    sanitized_insights = sanitize_text(insights)
    # Replace potential markdown-like list markers with a latin-1 compatible character
    sanitized_insights = sanitized_insights.replace('\n-', '\n- ').replace('\n*', '\n- ') # Ensure space after hyphen
    
    # Define potential subheading patterns (case-insensitive)
    subheading_patterns = [
        r"Understanding the situation",
        r"Immediate Action Items(?: & Recommendations)?", # Optional part
        r"Recommendations", # Simpler version
        r"Long-Term Financial Planning(?: & House Buying Goal)?", # Optional part
        r"House Buying Goal", # Simpler version
        r"Warnings(?: & Areas of Concern)?", # Optional part
        r"Areas of Concern", # Simpler version
        r"Summary"
    ]
    # Combine into a single regex pattern for matching
    subheading_regex = re.compile(r"^(\*\*)?(\d+\.?\s*)?(\"?)(%s)(\"?)(?:[\s*.:]*)\*\*?$" % "|".join(subheading_patterns), re.IGNORECASE)
    
    lines = sanitized_insights.split('\n')
    
    pdf.set_font('Arial', '', 11) # Default font for insights
    line_height_insight = 6

    for line in lines:
        trimmed_line = line.strip()
        if not trimmed_line:
            # pdf.ln(line_height_insight / 2) # Add small space for blank lines if desired
            continue

        match = subheading_regex.match(trimmed_line)
        
        if match:
            # It's a subheading
            pdf.ln(3) # Add space before subheading
            pdf.set_font('Arial', 'B', 11)
            # Extract the actual matched group (trims potential extra chars)
            subheading_text = next(g for g in match.groups()[3:5] if g is not None)
            pdf.multi_cell(0, line_height_insight, subheading_text.strip(), 0, 'L')
            pdf.set_font('Arial', '', 11) # Reset font after subheading
            pdf.ln(1) # Add small space after subheading
        elif trimmed_line.startswith('- '):
            # It's a list item - indent it
            pdf.set_x(pdf.l_margin + 5) # Indent list items
            pdf.multi_cell(0, line_height_insight, trimmed_line, 0, 'L')
            pdf.set_x(pdf.l_margin) # Reset indent
            pdf.ln(0.5) # Smaller space between list items
        else:
            # It's a normal paragraph line
            pdf.multi_cell(0, line_height_insight, trimmed_line, 0, 'L')
            pdf.ln(1) # Space after normal paragraphs

    pdf.ln(5)

    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1') 