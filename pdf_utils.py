import unicodedata
from fpdf import FPDF

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
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

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
    # Use the custom PDF class with header/footer
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15) # Enable auto page break

    # --- User Context Section --- 
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 220, 255) # Light blue background for section header
    pdf.cell(0, 10, 'Your Financial Profile', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0) # Reset text color

    # Create a table-like structure for context
    col_width_label = 40
    col_width_value = 150 # Total width = 190 (standard A4 content width)
    line_height = 8

    profile_data = {
        "Age:": str(user_context.get('age', 'N/A')),
        "Income:": f"${float(user_context.get('income', 0)):,.2f}",
        "Expenses:": sanitize_text(user_context.get('expenses', 'N/A')),
        "Goals:": sanitize_text(user_context.get('goals', 'N/A')),
        "Country:": sanitize_text(user_context.get('country', 'N/A'))
    }

    for label, value in profile_data.items():
        pdf.set_font('Arial', 'B', 11) # Bold label
        pdf.cell(col_width_label, line_height, label, border=0)
        pdf.set_font('Arial', '', 11) # Regular value
        # Use multi_cell for value in case it wraps
        current_x = pdf.get_x()
        current_y = pdf.get_y()
        pdf.multi_cell(col_width_value, line_height, value, border=0)
        # Reset Y position for next line, ensuring alignment
        pdf.set_y(current_y + line_height) 
        # Reset X position (needed after multi_cell)
        pdf.set_x(pdf.l_margin) 
    
    pdf.ln(10)
    
    # --- Latest Insights Section --- 
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 220, 255) # Light blue background
    pdf.cell(0, 10, 'Latest Financial Insights', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0) # Reset text color

    # Use multi_cell for insights to handle paragraphs and wrapping
    sanitized_insights = sanitize_text(insights)
    # Replace potential markdown-like list markers with standard ones for PDF
    sanitized_insights = sanitized_insights.replace('\\n-', '\\n  • ').replace('\\n*', '\\n  • ')
    
    pdf.multi_cell(0, 6, sanitized_insights) # 0 width = full width, 6 = line height
    pdf.ln(5)

    # Return PDF as bytes
    # Important: FPDF generates latin-1 by default. If you need full UTF-8, 
    # you might need a different library or configure FPDF differently (more complex).
    return pdf.output(dest='S').encode('latin-1') 