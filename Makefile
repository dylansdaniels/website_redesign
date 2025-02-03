
.PHONY: all build clean create-conda-env

all: build

build:
	python build.py

clean:
	rm -rf content/*.html
	rm -rf content/*/*.html

create-conda-env:
	conda env create --yes --file environment.yml
