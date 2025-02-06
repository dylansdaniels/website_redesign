# %%
import os
import pypandoc
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

    for page, path in page_paths.items():
        page_components = html_parts.copy()

        # get path only
        out_path = path.split(page)[0]

        # ENHANCEMENT
        '''
        # remove instances of `##_` from out_path
        # build html to separate `build` folder
        # this will make the urls look neater
        '''
        # out_path = re.sub(r"\d\d_", "", out_path)

        # remove leading `##_` from page
        page = page.split("_", 1)[1]

        # change file extension for page
        page = page.split(".md")[0] + ".html"

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
        out_path = out_path + page

        # Update header with the relative stylesheet path
        page_components['header'] = page_components['header'].replace(
            '<link rel="stylesheet" href="styles.css">',
            f'<link rel="stylesheet" href="{relative_css_path}">'
        )

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

    return


# %%
content_path = os.path.join(os.getcwd(), "content")
hash_path = os.path.join(os.getcwd(), "scripts", "notebook_hashes.json")

_ = convert_notebooks_to_html(
    input_folder=content_path,
    hash_path=hash_path,
)
page_paths = get_page_paths()
generate_page_html(page_paths)
