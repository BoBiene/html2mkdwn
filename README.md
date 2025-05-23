# HTML to Markdown Conversion Service

This service provides an API endpoint for converting HTML content into Markdown format. It leverages FastAPI for the web framework and Trafilatura for the conversion process, all containerized using Docker for easy deployment and scalability.

## Quick Start (using prebuilt image)

You can use the prebuilt Docker image from the GitHub Container Registry without cloning or building:

```bash
docker run -d --name html2mkdwn -p 8000:8000 ghcr.io/bobiene/html2mkdwn:latest
```

The service is now available at `http://localhost:8000`.

---

## Features

* Fast and efficient HTML to Markdown conversion
* RESTful API endpoint
* Dockerized for easy deployment
* Built with FastAPI and Trafilatura

## Getting Started

To set up the project for local development or to build your own image:

### Prerequisites

* Docker

### Installing (build your own image)

Clone the repository:

```bash
git clone https://github.com/kauffinger/html2mkdwn.git
```

Build the Docker image:

```bash
docker build -t html_to_markdown .
```

Run the Docker container:

```bash
docker run -d --name html_to_markdown_container -p 8000:8000 html_to_markdown
```

The service should now be running and accessible at `http://localhost:8000`.

## Usage

To convert HTML to Markdown, send a POST request to the `/html/` endpoint with the HTML content.

Example using `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/html/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"html_content": "<p>Hello, world!</p>"}'
```

Response:

```json
{
  "markdown": "Hello, world!\n"
}
```

## Development

To contribute or set up a development environment, follow the standard GitHub fork and pull request workflow.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* FastAPI for the incredibly fast and efficient web framework.
* Trafilatura for the robust HTML to Markdown conversion.
* Docker for simplifying deployment and environment management.
