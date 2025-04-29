# TaxonLib

## Precommit gitleaks

This project has been protected by [gitleaks](https://github.com/gitleaks/gitleaks).
The pipeline is configured to scan on leaked secrets.

To be sure you do not push any secrets,
please [follow our guidelines](https://docs.aob.naturalis.io/standards/secrets/),
install [precommit](https://pre-commit.com/#install)
and run the commands:

- `pre-commit autoupdate`
- `pre-commit install`

## Installation

```bash
conda create -n taxonlib python==3.10.17
```

```bash
conda activate taxonlib
```

```bash
pip install -r requirements.txt
```