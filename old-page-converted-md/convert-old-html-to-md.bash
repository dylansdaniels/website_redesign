#!/bin/bash

convert-to-md () {
    pandoc \
        --from=html \
        --to=markdown \
        $1.html \
        --output=../old-page-converted-md/$1.md
}

cd ../old-page-html

# Only converting the pages that have content we actually care about integrating into the Tutorial
# Redesign
convert-to-md assumptions-validations
convert-to-md getting-started
convert-to-md hnn-core
convert-to-md hnn-gui-tutorials
convert-to-md hnn-template-model
convert-to-md home
convert-to-md installation
convert-to-md overview-and-uniqueness
convert-to-md presentations
convert-to-md publications
convert-to-md running-hnn-on-oscar
