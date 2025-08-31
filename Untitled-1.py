from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Output file
pdf_path = "EEE_Timetable_With_Breaks.pdf"

# Data with corrected time intervals
data = [
    ["Time", "Monday (DO1)", "Tuesday (DO2)", "Wednesday (DO3)", "Thursday (DO4)", "Friday (DO5)"],
    ["08:00 - 08:50", "Engineering Graphics & Design (Lab)", "Calculus & Linear Algebra (Theory)", "", "Semiconductor Physics & Computer Org. (Lab)", ""],
    ["08:50 - 09:40", "Engineering Graphics & Design (Lab)", "Calculus & Linear Algebra (Theory)", "", "Semiconductor Physics & Computer Org. (Lab)", ""],
    ["09:45 - 10:35", "Engineering Graphics & Design (Lab)", "", "Programming for Problem Solving (Lab)", "Calculus & Linear Algebra (Theory)", "Semiconductor Physics & Computer Org. (Lab)"],
    ["10:40 - 11:30", "Engineering Graphics & Design (Lab)", "", "Programming for Problem Solving (Lab)", "Programming for Problem Solving (Lab)", "Semiconductor Physics & Computer Org. (Lab)"],
    ["11:35 - 12:25", "", "", "", "Electrical & Electronics Engineering (Theory)", ""],
    ["12:30 - 13:20", "", "", "Electrical & Electronics Engineering (Theory)", "", "Programming for Problem Solving (Lab)"],
    ["13:25 - 14:15", "", "Constitution of India (Online)", "Electrical & Electronics Engineering (Theory)", "", "Programming for Problem Solving (Lab)"],
    ["14:20 - 15:10", "Communicative English (Theory)", "Environmental Science (Online)", "", "", "Electrical & Electronics Engineering (Theory)"],
    ["15:15 - 16:05", "Communicative English (Theory)", "", "Semiconductor Physics & Computer Org. (Lab)", "", "Communicative English (Theory)"],
    ["16:10 - 17:00", "", "", "Calculus & Linear Algebra (Theory)", "", "Semiconductor Physics & Computer Org. (Lab)"]
]

# Create PDF
doc = SimpleDocTemplate(pdf_path, pagesize=landscape(A3))

# Create table
table = Table(data, repeatRows=1)

# Table style
style = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 12),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
])

# Color coding for each cell
for row_idx in range(1, len(data)):
    for col_idx in range(1, len(data[row_idx])):
        cell_value = data[row_idx][col_idx]
        if "Lab" in cell_value:
            style.add("BACKGROUND", (col_idx, row_idx), (col_idx, row_idx), colors.lightpink)
        elif "Online" in cell_value:
            style.add("BACKGROUND", (col_idx, row_idx), (col_idx, row_idx), colors.lightgreen)
        elif "Theory" in cell_value:
            style.add("BACKGROUND", (col_idx, row_idx), (col_idx, row_idx), colors.lightblue)
        elif cell_value.strip() == "":
            style.add("BACKGROUND", (col_idx, row_idx), (col_idx, row_idx), colors.lightgrey)

# Apply style
table.setStyle(style)

# Build PDF
doc.build([table])

print(f"Timetable saved as {pdf_path}")
