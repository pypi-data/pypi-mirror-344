# modelbase

[![DOI](https://img.shields.io/badge/DOI-10.1186%2Fs12859--021--04122--7-blue)](https://doi.org/10.1186/s12859-021-04122-7)
[![pipeline status](https://gitlab.com/qtb-hhu/modelbase-software/badges/main/pipeline.svg)](https://gitlab.com/qtb-hhu/modelbase-software/-/commits/main)
[![coverage report](https://gitlab.com/qtb-hhu/modelbase-software/badges/main/coverage.svg)](https://gitlab.com/qtb-hhu/modelbase-software/-/commits/main)
[![Documentation](https://img.shields.io/badge/Documentation-Gitlab-success)](https://qtb-hhu.gitlab.io/modelbase-software/)
[![PyPi](https://img.shields.io/pypi/v/modelbase)](https://pypi.org/project/modelbase/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Downloads](https://pepy.tech/badge/modelbase)](https://pepy.tech/project/modelbase)


modelbase is a python package to help you build and analyze dynamic mathematical models of biological systems. It has originally been designed for the simulation of metabolic systems, but can be used for virtually any processes, in which some substances get converted into others.

modelbase incorporates an easy construction method to define 'reactions'. A rate law and the stoichiometry need to be specified, and the system of differential equations is assembled automatically.

modelbase allows 'algebraic modules', which are useful to implement rapid equilibrium or quasi steady-state approximations. In the simplest instance, they allow easy incorporation of conserved quantities.

modelbase also allows a simple construction of isotope-specific models. This class contains a constructor method that automatically construct all isotope specific versions of a particular reaction. Very cool - check it out!

## Release notes

Versions 1.0 and 0.4.0 introduced changes not compatible with the previous official
release 0.2.5. API changes are summarised in [this notebook](docs/source/api-changes.ipynb)

[Version 0.4.5](https://gitlab.com/qtb-hhu/modelbase-software/-/tags/0.4.5) was the prior stable version

[Version 0.2.5](https://gitlab.com/qtb-hhu/modelbase-software/-/tags/initial-release)
is the official release for the submission of the
mansucript "Building mathematical models of biological systems
with modelbase, a Python package for semi-automatic ODE assembly
and construction of isotope-specific models" to the Journal of Open
Research Software.

See changelog.md for details on changes of earlier versions.

## Installation

If you quickly want to test out modelbase, or do not require assimulo support, install modelbase via

```bash
pip install modelbase
```

To enable assimulo support, the easiest way is to install modelbase via conda. We also recommend using the conda-forge channels.

```bash
# recommended to avoid package clashes
conda config --add channels conda-forge

# Create a new environment (not necessary, but recommended)
conda create -n mb39 python=3.9
conda install -c conda-forge modelbase
```

## License

[GPL 3](https://gitlab.com/qtb-hhu/modelbase-software/blob/main/LICENSE)

## Documentation

The official documentation is hosted [here on gitlab](https://qtb-hhu.gitlab.io/modelbase-software/).

## Issues and support

If you experience issues using the software please contact us through our [issues](https://gitlab.com/qtb-hhu/modelbase-software/issues) page.

## Contributing to modelbase

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome. See our [contribution guide](https://gitlab.com/qtb-hhu/modelbase-software/blob/main/CONTRIBUTING.md) for more information.

## How to cite

If you use this software in your scientific work, please cite [this article](https://rdcu.be/ckOSa):

van Aalst, M., Ebenhöh, O. & Matuszyńska, A. Constructing and analysing dynamic models with modelbase v1.2.3: a software update. BMC Bioinformatics 22, 203 (2021)

- [doi](https://doi.org/10.1186/s12859-021-04122-7)
- [bibtex file](https://gitlab.com/qtb-hhu/modelbase-software/blob/main/citation.bibtex)
