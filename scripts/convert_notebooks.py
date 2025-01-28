# %%
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import html


def execute_notebook(notebook_path):
    """Executes a Jupyter notebook and returns the
    executed notebook object."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(
        notebook, {"metadata": {"path": os.path.dirname(notebook_path)}}
    )
    return notebook


def extract_html_from_notebook(notebook):
    """Extracts HTML for cell contents and outputs,
    including code and markdown."""
    html_output = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            # Add the code cell
            html_output.append(
                f"<div class='code-cell'><pre>{cell['source']}</pre></div>"
            )

            # Add outputs
            for output in cell.get("outputs", []):
                # Handle text/plain outputs (e.g., print statements,
                # function returns)
                if "text/plain" in output.get("data", {}):
                    text_output = output["data"]["text/plain"]
                    # Escape < and > characters
                    escaped_text_output = html.escape(text_output)
                    html_output.append(
                        "<div class='output-cell'><pre>"
                        f"{escaped_text_output}</pre></div>"
                    )

                # Handle stdout (stream output from print statements)
                if output.get("output_type") == "stream" \
                        and output.get("name") == "stdout":
                    stream_output = output.get("text", "")
                    # Escape < and > characters
                    escaped_stream_output = html.escape(stream_output)
                    html_output.append(
                        "<div class='output-cell'><pre>"
                        f"{escaped_stream_output}</pre></div>"
                    )

                # Handle image outputs (e.g., plots)
                # with Base64-encoded images
                if "image/png" in output.get("data", {}):
                    img_data = output["data"]["image/png"]
                    html_output.append(
                        "<div class='output-cell'>"
                        "<img src='data:image/png;base64,"
                        f"{img_data}'/></div>"
                    )

                # Handle errors (tracebacks)
                if output.get("output_type") == "error":
                    error_message = "\n".join(output.get("traceback", []))
                    html_output.append(
                        "<div class='output-cell error'>"
                        f"<pre>{error_message}</pre></div>"
                    )

        elif cell["cell_type"] == "markdown":
            # Add the markdown cell content
            # Escape < and > characters
            markdown_content = html.escape(cell["source"])
            html_output.append(
                "<div class='markdown-cell'>"
                f"<pre>{markdown_content}</pre></div>"
            )

    return "\n".join(html_output)


def convert_notebooks_to_html(input_folder, output_folder):
    """Executes and converts .ipynb files in the input folder to HTML."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        path = os.path.join(input_folder, filename)
        if filename.endswith(".ipynb"):
            print(f"Processing notebook: {filename}")

            # Execute the notebook
            executed_notebook = execute_notebook(path)

            # Extract HTML content
            html_content = extract_html_from_notebook(executed_notebook)

            # Save to HTML file
            output_file = os.path.join(
                output_folder, f"{os.path.splitext(filename)[0]}.html"
            )
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("<html><body>\n")
                f.write(html_content)
                f.write("\n</body></html>")

            print(f"Converted: {filename} -> {output_file}")


# %%
def test_nb_conversion():

    input_folder = "../tests"
    output_folder = "../tests"

    convert_notebooks_to_html(input_folder, output_folder)


test_nb_conversion()

# %%
