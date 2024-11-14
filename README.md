# PDF conversion service

Tiny API around [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) and [PyMuPDF4LLM](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/) to convert PDF files to markdown or plain text. Easily deploys to Fly.io, k8s, Dokku, or AWS Lambda with the provided Dockerfile.

## Usage

```sh
uv run uvicorn pdf_service.api:app
```

Then simply POST a file upload to the `/convert` endpoint with the `Accept` header set to the desired output format (`text/markdown` for markdown or `text/plain` for plain text).

Example:

```sh
curl -X POST -H 'Accept: text/markdown' -F file=@myfile.pdf  http://localhost:8000/convert
```

## Docker image

Building:

```sh
docker build -t pdf-service .
```

Running:

```sh
docker run -p 8000:8000 pdf-service
```

## AWS Lambda

You can use the docker image to run the service as an AWS Lambda function. Switch the `CMD` to `pdf_service.lambda` which wraps the Starlette app with [Mangum](https://mangum.io/).
