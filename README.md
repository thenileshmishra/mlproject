# mlproject

A simple machine learning project that trains and evaluates models to predict student performance using the provided Students Performance dataset.

## Dataset

- File: `data/StudentsPerformance.csv` (also available in `notebook/data/`)
- Short description: student demographics and exam scores (math, reading, writing).

## Quick start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Reproduce experiments or train models:

   - Open and run the notebooks in `notebook/` (recommended for step-by-step work), or
   - Use the training pipeline in `src/` (see `src/components/model_trainer.py` and pipeline modules).

3. Use Docker (optional): common commands are in the `Makefile` (e.g., `make build`, `make up`).

## Project structure

- `data/` — dataset files
- `notebook/` — EDA and model training notebooks
- `src/` — code for ingestion, transformation, and model training
- `artifacts/` — generated models and outputs
- `app.py` — small app / entrypoint

---

Keep it simple and reproducible. For more details, open the notebooks or check `src/`.

