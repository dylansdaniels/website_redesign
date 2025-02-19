
.PHONY: all build clean create-conda-env

all: build

build:
	python build.py

clean:
	rm -rf content/*.html
	rm -rf content/*/*.html

create-conda-env:
	conda env create --yes --file environment.yml
	conda run -n website-redesign-mpi pip install 'hnn_core[dev]==0.4rc4'

create-conda-env-mpi:
	conda env create --yes --file environment.yml --name website-redesign-mpi
	conda install -y -n website-redesign-mpi conda-forge::openmpi conda-forge::mpi4py
	@CONDA_ENV_PATH=$$(conda run -n website-redesign-mpi python -c "import os; print(os.environ['CONDA_PREFIX'])"); \
	mkdir -p "$$CONDA_ENV_PATH/etc/conda/activate.d $$CONDA_ENV_PATH/etc/conda/deactivate.d"; \
	echo "export OLD_DYLD_FALLBACK_LIBRARY_PATH=\$$DYLD_FALLBACK_LIBRARY_PATH" >> "$$CONDA_ENV_PATH/etc/conda/activate.d/env_vars.sh"; \
	echo "export DYLD_FALLBACK_LIBRARY_PATH=\$$DYLD_FALLBACK_LIBRARY_PATH:$$CONDA_ENV_PATH/lib" >> "$$CONDA_ENV_PATH/etc/conda/activate.d/env_vars.sh"; \
	echo "export DYLD_FALLBACK_LIBRARY_PATH=\$$OLD_DYLD_FALLBACK_LIBRARY_PATH" >> "$$CONDA_ENV_PATH/etc/conda/deactivate.d/env_vars.sh"; \
	echo "unset OLD_DYLD_FALLBACK_LIBRARY_PATH" >> "$$CONDA_ENV_PATH/etc/conda/deactivate.d/env_vars.sh"; \
	conda run -n website-redesign-mpi pip install 'hnn_core[dev]==0.4rc4'; \
	echo "Conda environment 'website-redesign-mpi' successfully created."