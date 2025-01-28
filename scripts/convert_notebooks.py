# %%
import os
import base64
import html
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


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


def save_plot_as_image(img_data, img_filename, output_dir):
    """Saves the plot image to the specified directory."""
    img_path = os.path.join(output_dir, img_filename)
    with open(img_path, "wb") as img_file:
        img_file.write(base64.b64decode(img_data))
    return


def extract_html_from_notebook(notebook, output_dir, use_base64=False):
    """Extracts HTML for cell contents and outputs,
    including code and markdown."""
    html_output = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            # add code cell contents
            html_output.append(
                f"<div class='code-cell'><pre>{cell['source']}</pre></div>"
            )

            # add code cell outputs
            for output in cell.get("outputs", []):
                # handle plain outputs (e.g., function returns)
                if "text/plain" in output.get("data", {}):
                    text_output = output["data"]["text/plain"]
                    # escape the '<' and '>' characters which can be
                    # incorrectly interpreted as HTML tags
                    escaped_text_output = html.escape(text_output)
                    html_output.append(
                        "<div class='output-cell'><pre>"
                        f"{escaped_text_output}</pre></div>"
                    )

                # handle stdout (e.g., outputs from print statements)
                if output.get("output_type") == "stream" \
                        and output.get("name") == "stdout":
                    stream_output = output.get("text", "")
                    # escape < and > characters
                    escaped_stream_output = html.escape(stream_output)
                    html_output.append(
                        "<div class='output-cell'><pre>"
                        f"{escaped_stream_output}</pre></div>"
                    )

                # handle image outputs (e.g., plots) using either Base64
                # encoding or .png files
                if "image/png" in output.get("data", {}):
                    img_data = output["data"]["image/png"]

                    if use_base64:
                        # optional Base64 encoding for image embedding
                        html_output.append(
                            "<div class='output-cell'>"
                            "<img src='data:image/png;base64,"
                            f"{img_data}'/></div>"
                        )
                    else:
                        # save the image as a file and reference it in HTML
                        img_filename = (
                            f"{output.get('metadata', {}).get('name', 'plot')}"
                            ".png"
                        )
                        save_plot_as_image(
                            img_data,
                            img_filename,
                            output_dir
                        )
                        html_output.append(
                            "<div class='output-cell'>"
                            f"<img src='{img_filename}'/></div>"
                        )

                # handle errors
                if output.get("output_type") == "error":
                    error_message = "\n".join(output.get("traceback", []))
                    html_output.append(
                        "<div class='output-cell error'>"
                        f"<pre>{error_message}</pre></div>"
                    )

        elif cell["cell_type"] == "markdown":
            # escape < and > characters
            markdown_content = html.escape(cell["source"])
            html_output.append(
                "<div class='markdown-cell'>"
                f"<pre>{markdown_content}</pre></div>"
            )

    return "\n".join(html_output)


def convert_notebooks_to_html(
    input_folder,
    output_folder,
    use_base64=False,
):
    """Executes and converts .ipynb files in the input folder to HTML."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        path = os.path.join(input_folder, filename)
        if filename.endswith(".ipynb"):
            print(f"Processing notebook: {filename}")
            executed_notebook = execute_notebook(path)

            html_content = extract_html_from_notebook(
                executed_notebook,
                output_folder,
                use_base64
            )

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

    convert_notebooks_to_html(
        input_folder,
        output_folder,
        use_base64=False,
    )


test_nb_conversion()

# %%
