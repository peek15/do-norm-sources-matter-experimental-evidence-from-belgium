# Do Norm Sources Matter? Experimental Evidence from Belgium

Replication package for Théo Mauroy's master's thesis, *Do Norm Sources Matter? Experimental Evidence from Belgium*.

This repository contains the materials needed to inspect the experimental implementation and reproduce the main Stata analyses from the anonymized thesis dataset.

## Contents

- `experiment/otree_app/`: oTree source code for the online experiment.
- `analysis/stata/`: Stata scripts used for data import, analysis, and figure generation.
- `data/thesis_data.dta`: anonymized analysis dataset.
- `outputs/`: target folder for generated figures and analysis outputs.

## Reproducing the analysis

From the repository root, open Stata and run:

```stata
cd analysis/stata
do analysisV3.do
```

To regenerate Figure 5.1 separately:

```stata
cd analysis/stata
do figure_51_stata.do
```

The figure script exports `outputs/donation_distribution.pdf`.

## Running the oTree experiment

The oTree app is included for transparency and inspection. From `experiment/otree_app/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
otree devserver
```

For production use, set `OTREE_ADMIN_PASSWORD` and `OTREE_SECRET_KEY` as environment variables.

## Data

The public dataset is anonymized and prepared for analysis. Raw administrative exports and local runtime databases are not included in this replication package.

## Citation

If you use this material, please cite:

Mauroy, Théo. 2026. *Do Norm Sources Matter? Experimental Evidence from Belgium*. Master's thesis, UCLouvain, UNamur, and Università degli Studi di Milano.

## License

Code is released under the MIT License. Data and documentation are released under the Creative Commons Attribution 4.0 International License. See `LICENSE_CODE` and `LICENSE_DATA`.
