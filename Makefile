
.PHONY: all build create-conda-env

all: build

build:
	python build.py

create-conda-env:
	conda env create --yes --file environment.yml
