![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jonaspleyer/cr_bayesian_optim/paper.yml?style=flat-square&label=Paper)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jonaspleyer/cr_bayesian_optim/CI.yml?style=flat-square&label=Build)
![GitHub License](https://img.shields.io/github/license/jonaspleyer/cr_bayesian_optim?style=flat-square&label=License)
[![Docs](https://img.shields.io/github/actions/workflow/status/jonaspleyer/cr_bayesian_optim/sphinx_doc.yml?label=Docs&style=flat-square)](https://github.com/jonaspleyer/cr_bayesian_optim/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/cr_bayesian_optim?style=flat-square)]()

# cr_bayesian_optim

This project combines Bayesian Optimization with Agent-Based simulations of cellular systems done by
cellular_raza.

## Usage

```python
if __name__ == "__main__":
    print("Hello, World!")
```

## Installation
This project uses [maturin](https://github.com/PyO3/maturin) to install all required dependencies.
We recommend, to pair this with the [`uv`](https://github.com/astral-sh/uv) package manager.

### From [pypi](https://pypi.org/)

```bash
uv pip install cr_bayesian_optim
```

### From Source

Once you have cloned the repository
```bash
git clone https://github.com/jonaspleyer/cr_bayesian_optim
```
you should move the respective directory and create a new virtual environment.

```bash
cd cr_bayesian_optim
python -m venv .venv
```

Afterwards, activate the environment and install the package.
```bash
source .venv/bin/activate
maturin develop -r --uv
```
