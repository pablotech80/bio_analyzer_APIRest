from flask import Blueprint, render_template, make_response, session, request
from xhtml2pdf import pisa
import io
from flask import current_app
import os

bp = Blueprint("generate_pdf", __name__)

@bp.route("/generate_pdf")
def generate_pdf():
    resultados = session.get("resultados")
    interpretaciones = session.get("interpretaciones")

    if not resultados:
        return "No hay datos para generar el PDF", 400
    logo_path = os.path.join(current_app.root_path, "static", "img", "bio_analyze.jpg")

    html = render_template(
        "resultados_pdf.html",
        resultados = resultados,
        interpretaciones = interpretaciones,
        logo_path = f"file://{logo_path}"
        )

    pdf_stream = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_stream)

    if pisa_status.err:
        return "Error al generar el PDF", 500

    response = make_response(pdf_stream.getvalue())
    response.headers["Content-Type"] = "application/pdf"

    descargar = request.args.get("descargar")
    disposition = "attachment" if descargar else "inline"
    response.headers["Content-Disposition"] = f"{disposition}; filename=analysis_bioanalyze.pdf"

    return response
  
