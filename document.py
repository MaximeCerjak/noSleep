from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def creer_pdf(contenu, filename='document_veille.pdf'):
    c = canvas.Canvas(filename, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)
    text.textLines(contenu)
    c.drawText(text)
    c.showPage()
    c.save()
