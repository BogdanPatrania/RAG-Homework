.PHONY: help lint test format run-jupyter

help:
	@echo "Available targets:"
	@echo "  env          Create conda env from environment.yml"
	@echo "  jupyter      Launch Jupyter Lab"
	@echo "  test         Run unit tests"
	@echo "  format       Auto-format with black (if installed)"
	@echo "  lint         Run flake8 (if installed)"

env:
	conda env create -f environment.yml || echo "Env may already exist"
	conda activate llm-assignment

jupyter:
	jupyter lab

test:
	pytest -q

format:
	black src tests || true

lint:
	flake8 src tests || true
