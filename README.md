# Website Redesign

## Where to access the deployed verison of this website?

Click here: https://dylansdaniels.github.io/website_redesign/content/preface.html

## How to use this repository

1. Content creation step: First, you add or edit the actual content. Specifically, this means adding to or editing the various Markdown (filetype `.md`) files located in `content/`.
   - TODO: We should gradually describe with more detail here.

2. "Building" step: Second, you should "build" the Markdown content into actual HTML pages. This is done automatically when you run `python build.py` or `make` from the main directory. For installation of the python packages/environment, see below.

3. Git push step: At this point, you should be ready to push! Make a PR from your fork so we can then merge your changes.

## Install environment

1. If you have `make` installed (which you can check by running `which make`), and also have Anaconda installed, then this is super easy. You can create a new conda environment simply by running `make create-conda-env`.
   - This will create a conda environment named `website-redesign` which you can use to run all the python code in this repository without needing to install anything else (including Pandoc).
   - If you use this method, then you can run the "build" step simply by typing `make` in the main directory. This is equivalent to running `python build.py`.
   - If you get an error about not having `make` and want to use it, then you can install Xcode Command-Line Tools simply by running the command `xcode-select --install`.

2. If you only have Anaconda installed but not `make`, then you can create the same environment by simply running the following command:

```{bash}
conda env create --yes --file environment.yml
```

3. If you don't use Anaconda, you can use the `requirements.txt` file to install the necessary Python packages, such as by running:

```{bash}
pip install -r requirements.txt
```

- Note that you may have to additionally install Pandoc in this case, such as by running `python -c 'import pypandoc ; pypandoc.download()'` or something similar.
