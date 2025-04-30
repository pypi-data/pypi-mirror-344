# Mistral PDF to Markdown Converter

A simple command-line tool to convert PDF files into Markdown format using the Mistral AI OCR API.
This tool also extracts embedded images and saves them in a subdirectory relative to the output markdown file.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/arcangelo7/mistral-pdf-to-markdown.git
    cd mistral-pdf-to-markdown 
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

## Usage

1.  **Set your Mistral API Key:**
    You can set your API key as an environment variable:
    ```bash
    export MISTRAL_API_KEY='your_api_key_here'
    ```
    Alternatively, you can create a `.env` file in the project root directory with the following content:
    ```
    MISTRAL_API_KEY=your_api_key_here
    ```
    You can also pass the API key directly using the `--api-key` option.

2.  **Run the conversion:**
    The main command is `convert`.
    ```bash
    poetry run pdf2md convert <path/to/your/document.pdf> [options]
    ```
    Or, if you have activated the virtual environment (`poetry shell`):
    ```bash
    pdf2md convert <path/to/your/document.pdf> [options]
    ```

**Options:**

*   `--output` or `-o`: Specify the path for the output Markdown file. If not provided, it defaults to the same name as the input PDF but with a `.md` extension (e.g., `document.md`).
*   `--api-key`: Provide the Mistral API key directly.

**Image Handling:**

The script will attempt to extract images embedded in the PDF.
*   Images are saved in a subdirectory named `<output_filename_stem>_images` (e.g., if the output is `report.md`, images will be in `report_images/`).
*   The generated Markdown file will contain relative links pointing to the images in this subdirectory.

**Example:**

```bash
poetry run pdf2md convert ./my_report.pdf -o ./output/report.md
```
This command will create:
*   `./output/report.md` (the markdown content)
*   `./output/report_images/` (a directory containing extracted images)

An example output generated from `example.pdf` (included in the repository) can be found in `example.md`, with its corresponding images located in the `example_images/` directory.

## Development

Use `poetry shell` to activate the virtual environment for development.

Run tests (if any) using:
```bash
poetry run pytest
```

## License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.