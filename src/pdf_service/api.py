from starlette.applications import Starlette
from starlette.datastructures import UploadFile
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from pydantic import BaseModel

import pymupdf
import pymupdf4llm


class ConversionResponse(BaseModel):
    text: str


def root(_request: Request):
    return JSONResponse({"message": "PDF Conversion Service 1.0"})


async def convert(request: Request):
    async with request.form() as form:
        file = form.get("file")
        if not file or not isinstance(file, UploadFile):
            return JSONResponse({"error": "No file provided"}, status_code=400)

        if not file.content_type or not file.content_type.startswith("application/pdf"):
            return JSONResponse({"error": "File must be a PDF"}, status_code=400)

        try:
            contents = await file.read()
            pdf = pymupdf.open(stream=contents, filetype="pdf")
            accept = request.headers.get("accept")

            match accept:
                case "text/markdown":
                    text = pymupdf4llm.to_markdown(pdf)
                case "text/plain" | "*/*":
                    text = ""
                    for page in pdf:
                        text += page.get_text()
                case _:
                    raise ValueError(f"Unsupported accept header: {accept}")
            pdf.close()

            response = ConversionResponse(text=text)
            return JSONResponse(response.model_dump())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)


app = Starlette(
    debug=True,
    routes=[
        Route("/", root, methods=["GET"]),
        Route("/convert", convert, methods=["POST"]),
    ],
)
