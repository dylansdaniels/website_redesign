# %%
import os
import base64
import html
import re
import json
import nbformat
import markdown
import hashlib
from nbconvert.preprocessors import ExecutePreprocessor


def save_plot_as_image(img_data, img_filename, output_dir):
    """Saves the plot image to the specified directory."""
    img_path = os.path.join(output_dir, img_filename)
    with open(img_path, "wb") as img_file:
        img_file.write(base64.b64decode(img_data))
    return


def html_to_json(html: str, filename: str):
    """
    Convert html into hierarchical json
    """
    # variable for processed json output
    contents = {filename: {}}

    # variable to track section content and metadata
    current_html = None
    current_title = None
    current_level = None

    # split html into lines while removing empty lines
    lines = [line.strip() for line in html.splitlines() if line.strip()]

    for i, line in enumerate(lines):
        # identify lines with header tags
        line_match = re.match(r'(<h[1-6]>)(.*?)(</h[1-6]>)', line)

        if line_match:
            # when a new header is found, save the previous section
            if current_title:
                contents[filename][current_title] = {}
                contents[filename][current_title]['level'] = current_level
                contents[filename][current_title]['html'] = \
                    '\n'.join(current_html)

            # get the title, level of the new section
            current_level = line_match.group(1).strip()
            current_level = int(current_level.lstrip('<h').rstrip('>'))
            current_title = line_match.group(2).strip()

            # start a new section with the previous line
            current_html = [lines[i-1]]

        elif current_html is not None:
            # add new html lines
            current_html.append(lines[i-1])

    # save the last section
    if current_title:
        # append the last line
        current_html.append(line)

        # update contants
        contents[filename][current_title] = {}
        contents[filename][current_title]['level'] = current_level
        contents[filename][current_title]['html'] = \
            '\n'.join(current_html)

    return contents


def structure_json(contents):
    """
    Determine the hierarchy of sections based on levels without adding content.
    Returns a list of sections in order of their hierarchy.
    """
    hierarchy = {}

    for filename, sections in contents.items():
        hierarchy[filename] = {}

        # list to track parent sections for potential nesting
        parent_stack = []

        for section_title, section_data in sections.items():
            level = section_data['level']
            html_contents = section_data['html']

            # Create a section dict with 'title', 'level', and 'sub-sections'
            section_info = {
                'title': section_title,
                'level': level,
                'html': html_contents,
                'sub-sections': []
            }

            # Ensure only sections with a level greater than the current
            # section remain in the stack as potential parents
            while parent_stack and parent_stack[-1]['level'] >= level:
                parent_stack.pop()

            if parent_stack:
                # Add the section as a child of the last parent
                parent_stack[-1]['sub-sections'].append(section_info)
            else:
                # Add the section as a top-level section
                hierarchy[filename][section_title] = section_info

            # Add the current section to the parent stack for future nesting
            parent_stack.append(section_info)

    def remove_blank_subsections(sections):
        seek = 'sub-sections'

        for k, v in list(sections.items()):

            if isinstance(v, dict):
                # check for 'sub-sections' key in dict
                if seek in v:

                    # delete empty sub-sections
                    if v[seek] == []:
                        del v[seek]

                    # Recursively check all sub-sections
                    else:
                        for sub_section in v[seek]:
                            remove_blank_subsections(sub_section)

            elif isinstance(v, list):
                # if v is an empty list, delete it
                if v == []:
                    del sections[k]
                # if v is a list of dicts, iterate through the dicts
                else:
                    for dictionary in v:
                        remove_blank_subsections(dictionary)

        return sections

    hierarchy[filename] = remove_blank_subsections(hierarchy[filename])

    return hierarchy


def extract_html_from_notebook(
        notebook,
        input_dir,
        filename,
        use_base64=False
        ):
    """Extracts HTML for cell contents and outputs,
    including code and markdown."""

    html_output = []
    fig_id = 0
    delim = os.path.sep
    aggregated_output = ""

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            # add code cell contents
            html_output.append(
                "<div class='code-cell'>"
                "\n\t<code class='language-python'>"
                f"\n\t\t{cell['source']}"
                "\n\t</code>"
                "\n</div>"
            )

            # add code cell outputs
            for output in cell.get("outputs", []):
                # handle plain outputs (e.g., function returns)
                if "text/plain" in output.get("data", {}):
                    text_output = output["data"]["text/plain"]
                    # escape the '<' and '>' characters which can be
                    # incorrectly interpreted as HTML tags
                    escaped_text_output = html.escape(text_output)

                    # Aggregate plain text outputs
                    aggregated_output += f"\n\t\t{escaped_text_output}"

                # handle stdout (e.g., outputs from print statements)
                if output.get("output_type") == "stream" \
                        and output.get("name") == "stdout":
                    stream_output = output.get("text", "")
                    # escape < and > characters
                    escaped_stream_output = html.escape(stream_output)

                    aggregated_output += f"\n\t\t{escaped_stream_output}"

                # handle image outputs (e.g., plots) using either Base64
                # encoding or .png files
                if "image/png" in output.get("data", {}):
                    # If there are accumulated outputs, output them first
                    if aggregated_output:
                        html_output.append(
                            "<div class='output-cell'>"
                            "<div class='output-label'>"
                            "\n\tOut:"
                            "\n</div>"
                            "\n\t<div class='output-code'>"
                            f"{aggregated_output}"
                            "\n\t</div>"
                            "\n</div>"
                        )
                        aggregated_output = ""

                    img_data = output["data"]["image/png"]

                    if use_base64:
                        # optional Base64 encoding for image embedding
                        html_output.append(
                            "<div class='output-cell'>"
                            "\n\t<img src='data:image/png;base64,"
                            f"{img_data}'/>"
                            "\n</div>"
                        )
                    else:
                        # save the image as a file and reference it in HTML
                        fig_id += 1
                        if fig_id <= 10:
                            img_filename = f"fig_0{fig_id}.png"
                        else:
                            img_filename = f"fig_{fig_id}.png"

                        output_folder = "output_nb_" + \
                            f"{filename.split('.ipynb')[0]}"

                        output_dir = f"{input_dir}{delim}{output_folder}"

                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)

                        save_plot_as_image(
                            img_data,
                            img_filename,
                            output_dir,
                        )
                        html_output.append(
                            "<div class='output-cell'>"
                            f"\n\t<img src='{output_folder}{delim}"
                            f"{img_filename}'/>"
                            "\n</div>"
                        )

                # handle errors
                if output.get("output_type") == "error":
                    error_message = "\n".join(output.get("traceback", []))
                    html_output.append(
                        "<div class='output-cell error'>"
                        "\n\t<pre>"
                        f"\n\t\t{error_message}"
                        "\n\t</pre>"
                        "\n</div>"
                    )

            # If there are any accumulated outputs after processing all
            # outputs for the cell
            if aggregated_output:
                html_output.append(
                    "<div class='output-cell'>"
                    "<div class='output-label'>"
                    "\n\tOut:"
                    "\n</div>"
                    "\n\t<div class='output-code'>"
                    f"{aggregated_output}"
                    "\n\t</div>"
                    "\n</div>"
                )
                aggregated_output = ""

        elif cell["cell_type"] == "markdown":
            # escape < and > characters
            markdown_content = html.escape(cell["source"])

            html_content = markdown.markdown(markdown_content)

            html_output.append(
                "<div class='markdown-cell'>"
                f"\n\t{html_content}"
                "\n</div>"
            )

    html_output = "\n".join(html_output)

    return html_output


def hash_notebook(notebook_path):
    """Generate a SHA256 hash of the notebook"""
    hasher = hashlib.sha256()
    with open(notebook_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_notebook_hashes(hash_path):
    """Load previously-recorded hashes notebook hashes"""
    if os.path.exists(hash_path):
        with open(hash_path, "r") as f:
            return json.load(f)
    return {}


def save_notebook_hashes(
        new_hashes,
        hash_path,
        ):
    """Save updated notebook hashes"""

    # print(f'Saving hashes to {hash_path}')
    with open(hash_path, "w") as f:
        json.dump(new_hashes, f, indent=4)


def get_notebook(
        notebook_path,
        execute,
        timeout=600,
        ):
    """Get a jupyter notebook object and optionally execute it"""
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    if execute:
        ep = ExecutePreprocessor(
            timeout=timeout,
            kernel_name="python3"
        )
        ep.preprocess(
            notebook, {"metadata": {"path": os.path.dirname(notebook_path)}}
        )

    return notebook


def convert_notebooks_to_html(
        input_folder=None,
        use_base64=False,
        write_html=False,
        hash_path="notebook_hashes.json",
        ):
    """Executes and converts .ipynb files in the input folder to HTML."""

    if not input_folder:
        input_folder = os.getcwd().split('scripts')[0]
        input_folder += 'content'

    # load saved notebook hashes
    notebook_hashes = load_notebook_hashes(hash_path)
    # create a copy of the hashes to update and save
    updated_hashes = notebook_hashes.copy()

    # iterate through input directory and process notebooks
    for root, list_folders, list_files in os.walk(input_folder):
        for filename in list_files:
            if filename.endswith(".ipynb"):
                print(
                    f"Processing notebook: {filename}"
                )

                # get current hash of the notebook
                nb_path = os.path.join(root, filename)
                current_hash = hash_notebook(nb_path)

                # skip execution if the notebook hasn't changed, comparing
                # the current hash with the previously-saved hash
                if (filename in notebook_hashes) and \
                        (notebook_hashes[filename] == current_hash):
                    print(
                        f"Skipping execution of unchanged notebook: {filename}"
                    )
                    executed_notebook = get_notebook(
                        nb_path,
                        execute=False,
                    )
                # if the file has been changed or a hash hasn't yet been
                # recorded, execute the notebook and update the hash dict
                else:
                    print(
                        "New or changed notebook detected. Executing "
                        f"the notebook: {filename}"
                    )
                    executed_notebook = get_notebook(
                        nb_path,
                        execute=True,
                    )
                    # update the hash dictionary
                    updated_hashes[filename] = current_hash

                html_content = extract_html_from_notebook(
                    executed_notebook,
                    root,
                    filename,
                    use_base64,
                )

                if write_html:
                    output_file = os.path.join(
                        root, f"{os.path.splitext(filename)[0]}.html"
                    )
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write("<html><body>\n")
                        f.write(html_content)
                        f.write("\n</body></html>")

                # ----------------------------------------
                # generated structured json output
                # ----------------------------------------
                # Note: this section pertains to a planned enhancement
                # to enable inserting sections of a notebook into an
                # html file by specifing the headers to include; e.g.,
                # including [[notebook][start header][end header]] in your
                # .md file would inject only the .html for those header
                # sections into your html output file

                # flat json
                nb_html_json = html_to_json(
                    html_content,
                    filename,
                )
                # nested json
                # nb_html_json = structure_json(
                #     nb_html_json
                # )
                output_json = os.path.join(
                    root, f"{os.path.splitext(filename)[0]}.json"
                )
                with open(output_json, "w") as f:
                    json.dump(nb_html_json, f, indent=4)
                # ----------------------------------------

                print(f"Successfully converted '{filename}'to html\n")

    # save updated hashes
    save_notebook_hashes(
        updated_hashes,
        hash_path,
    )

    return html


# %%
def test_nb_conversion(input_folder=None):

    convert_notebooks_to_html(
        input_folder=input_folder,
        use_base64=False,
        write_html=True,
    )


# _ = test_nb_conversion()
