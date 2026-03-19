# Recursive-ToM: Procedural Benchmark for Higher-Order Social Inference

> *"Measuring cognitive collapse in LLMs under recursive social reasoning"*

**Status**: Under Development  
**Team**: Pietro Maietta (Independent Researcher / Pietro Maietta Lab)  
**Competition**: Kaggle - Measuring Progress Toward AGI

## Overview
Current ToM benchmarks are static and shallow. This project introduces a dynamic, procedurally generated sandbox to evaluate recursive social inference (e.g., “I know that you know that he knows...”).

## Planned Features
- Procedural scenario generator (Python)
- Multi-level ToM questioning engine
- Cognitive collapse metric
- Open evaluation suite for LLMs

## Timeline
- Q1 2025: Core engine development
- Q2 2025: Pilot testing
- Q3 2025: Public release

## Repository Structure
- `recursive_tom/`:
  - `engine.py`: motore logico rigoroso per scenari di Teoria della Mente ricorsiva (agent/beliefs).
  - `game_theory.py`: strumenti di teoria dei giochi (es. matrice good cop / bad cop).
  - `evaluation.py`: sistema di valutazione a consiglio di pari (good cop, bad cop, giudice strategico).
- `recursive_tom_engine.py`: compat layer per importare il motore (`RecursiveToMEngine`) da script esterni/legacy.
- `recursive_tom_generator.py`: versione script del motore logico (utile per test manuali/CLI).
- `generate_dataset.py`: genera un dataset JSON di esempi (`sample_benchmark.json`) usando il motore logico.
- `generator.py`: semplice generatore narrativo (`SocialScenarioGenerator`) per scenari high-level ToM.
- `main_experiment.py`: pipeline di benchmark (simulata) che produce `benchmark_raw_results.csv`.
- `reinforced_cognition_experiment.py`: demo di "cognizione rinforzata" con consiglio di pari e matrice good cop / bad cop.
- `statistical_analysis.py`: analisi statistica/plot del collasso cognitivo a partire da `benchmark_raw_results.csv`.
- `src/benchmark.py`: wrapper Kaggle (`kaggle_benchmarks`) per esportare il benchmark ufficiale.

## Installazione Rapida
Richiede Python 3.9+.

Installazione dipendenze principali (locale o su Kaggle Notebook):

```bash
pip install -r requirements.txt
```

> Nota: il modulo `kaggle_benchmarks` è fornito dall'ambiente della competition Kaggle e non è incluso in `requirements.txt`.

## Come Eseguire

- Test rapido del motore logico (scenari ToM ricorsivi):
  ```bash
  python recursive_tom_generator.py
  ```

- Demo di cognizione rinforzata (consiglio di pari + teoria dei giochi):
  ```bash
  python reinforced_cognition_experiment.py
  ```

- Generare un piccolo dataset JSON di esempio:
  ```bash
  python generate_dataset.py
  ```
  Output: `sample_benchmark.json` + anteprima a schermo.

- Lanciare il benchmark simulato (mock LLM) e salvare i risultati grezzi:
  ```bash
  python main_experiment.py
  ```
  Output: `benchmark_raw_results.csv` con performance per livello di ToM.

- Eseguire l'analisi statistica e visualizzare il grafico di collasso cognitivo:
  ```bash
  python statistical_analysis.py
  ```
  Output: summary ANOVA, regressione logistica e figura `tom_cognitive_collapse_analysis.png`.

- Registrare il benchmark sulla piattaforma Kaggle (nell'ambiente ufficiale):
  ```bash
  python src/benchmark.py
  ```
  Richiede Kaggle CLI configurata e il package `kaggle_benchmarks` disponibile.
