# %%
import os
import re
import pypandoc
import json
from scripts.create_page_index import update_page_index
from scripts.create_navbar import generate_navbar_html
from scripts.convert_notebooks import convert_notebooks_to_html


def compile_page_components():
    """Compile base html components for building webpage"""

    templates_folder = os.path.join(os.getcwd(), 'templates')
    templates = ['header', 'topbar', 'script']
    html_parts = {}

    for template in templates:
        templates_path = os.path.join(templates_folder, f'{template}.html')
        with open(templates_path, 'r') as f:
            html_parts[template] = f.read()

    update_page_index()
    html_parts['navbar'] = generate_navbar_html()

    return html_parts


def get_page_paths(path=None):
    """Get paths to all .md pages to be converted to html"""

    md_pages = {}
    if path is None:
        path = os.path.join(os.getcwd(), "content")
    directories = os.listdir(path)
    for item in directories:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            # add items from new dict into md_pages
            md_pages.update(get_page_paths(item_path))
        else:
            if not item == "README.md" and item.endswith(".md"):
                md_pages[item] = item_path

    return md_pages


def generate_page_html(page_paths):
    html_parts = compile_page_components()
    order = [
        'header',
        'navbar',
        'topbar',
        'body',
        'script',
    ]

    for md_page, path in page_paths.items():
        page_components = html_parts.copy()

        # get path only
        out_path = path.split(md_page)[0]

        # ENHANCEMENT
        '''
        # remove instances of `##_` from out_path
        # build html to separate `build` folder
        # this will make the urls look neater
        '''
        # out_path = re.sub(r"\d\d_", "", out_path)

        # remove leading `##_` from page
        html_page = md_page.split("_", 1)[1]

        # change file extension for page
        html_page = html_page.split(".md")[0] + ".html"

        # get relative path to the stylesheet
        css_path = os.path.join(
            os.getcwd(),
            "content",
            "assets",
            "styles.css"
        )
        relative_css_path = os.path.relpath(
            css_path,
            start=out_path
        )

        # combine path and page
        out_path = out_path + html_page

        # Update header with the relative stylesheet path
        page_components['header'] = page_components['header'].replace(
            '<link rel="stylesheet" href="styles.css">',
            f'<link rel="stylesheet" href="{relative_css_path}">'
        )

        def get_html_from_json(
                nb_name,
                nb_path,
                ):
            """"""
            html_output = []
            json_path = nb_path.split('.ipynb')[0] + '.json'
            with open(json_path, 'r') as file:
                nb_outputs = json.load(file)
                nb_outputs = nb_outputs.get(nb_name, {})
                print(nb_outputs)
                agg_html = ''
                for section, content in nb_outputs.items():
                    if isinstance(content, dict) and 'html' in content:
                        agg_html += content['html']

            for line in agg_html.splitlines():
                html_output.append(line)

            return html_output

        def add_html_notebooks_to_markdown():
            """Pending"""
            # regex pattern match for "[[notebook_name.ipynb]" with only
            # a single closing bracket, as additional parameters may be
            # included in the notebook specification line
            nb_match_pattern = re.compile(r"\[\[(.+?\.ipynb)\]")
            # notebook specifications with additional arguments will
            # match the exact pattern ".ipynb][" as defined below
            nb_arguments_pattern = ".ipynb]["

            with open(path, 'r') as file:
                for line in file:
                    match = nb_match_pattern.search(line)
                    args = nb_arguments_pattern in line
                    if match and args:
                        print(f'nb with args found: {line}')
                    elif match:
                        notebook_name = match.group(1)
                        nb_path = path.split(md_page)[0] + notebook_name
                        new_lines = get_html_from_json(
                            notebook_name,
                            nb_path,
                        )
                        print(new_lines)
                    else:
                        continue
            return

        add_html_notebooks_to_markdown()

        # use pypandoc to convert md to html
        try:
            converted = pypandoc.convert_file(
                path,
                to='html',
                extra_args=["--mathml"],
            )
        except Exception as ex:
            # download Pandoc dependency if needed
            if "No pandoc was found" in ex:
                print("Downloading pandoc dependency")
                pypandoc.download_pandoc()
                converted = pypandoc.convert_file(
                    path,
                    to='html',
                    extra_args=["--mathml"],
                )
            else:
                raise ex

        page_components['body'] = converted

        file_contents = ""
        for section in order:
            file_contents += page_components[section]
        file_contents += '\n</body>\n</html>'

        with open(out_path, 'w') as out:
            out.write(file_contents)

    return converted


# %%
content_path = os.path.join(os.getcwd(), "content")
hash_path = os.path.join(os.getcwd(), "scripts", "notebook_hashes.json")

_ = convert_notebooks_to_html(
    input_folder=content_path,
    hash_path=hash_path,
    write_html=True,
)
page_paths = get_page_paths()
output = generate_page_html(page_paths)
