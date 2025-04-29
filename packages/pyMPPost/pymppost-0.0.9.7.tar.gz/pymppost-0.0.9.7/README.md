# pyMPPost
[![Static Badge](https://img.shields.io/badge/Dveloped%20by-DNNG_%40_umich-blue)](https://dnng.engin.umich.edu)
[![PyPI - Version](https://img.shields.io/pypi/v/pyMPPost)](https://pypi.org/project/pyMPPost)
[![PyPI - License](https://img.shields.io/pypi/l/pyMPPost)](#License)

This project provides a suite of analysis tools for processing time-resolved particle detection data, particularly for applications involving scintillator detectors, neutron/gamma discrimination, and nuclear nonproliferation measurements. It includes core modules for:

- Calculating **pulse height** using detailed material and detector modeling.
- Measuring **cross-correlation** between detector pairs to assess timing and event structure.
- Computing **multiplicity** statistics using shift-register logic for coincidence counting.
- Executing complete post-processing workflows from MCNP-Polimi simulation outputs via command line.

Each module is optimized for high-throughput data analysis and can be integrated into a larger experimental or simulation pipeline. Where applicable, performance-critical computations are offloaded to Cython extensions, and Dask is used to support scalable distributed processing.

---

## Installation

You can install the latest release from PyPI:

```bash
pip install pyMPPost
```

Or, for development:

```bash
git clone https://github.com/your-org/pyMPPost.git
cd pyMPPost
pip install -e .
```

Ensure you have a working Python 3.9+ environment and Cython installed if you're compiling from source.


## Usage

Run the full MCNP-Polimi analysis pipeline using a TOML configuration file:

```bash
pyMPPost input_config.toml
```

### 🧾 Download Template Files

- 📄 [Download blank `input_config.toml`](https://gitlab.eecs.umich.edu/umich-dnng/pymppost/-/raw/main/.gitlab/downloads/input_config.toml)
- 📄 [Download blank `material_card.toml`](https://gitlab.eecs.umich.edu/umich-dnng/pymppost/-/raw/main/.gitlab/downloads/material_card.toml)
- 📄 [Download example `stopping_power.txt`](https://gitlab.eecs.umich.edu/umich-dnng/pymppost/-/raw/main/.gitlab/downloads/ogsdEdx.txt)

See the [API Reference](https://gitlab.eecs.umich.edu/umich-dnng/pymppost/-/blob/main/docs/Reference.md) below for full module documentation and input expectations.

## Contact

Maintained by the [Detection for Nuclear Nonproliferation Group (DNNG)](https://gitlab.eecs.umich.edu/umich-dnng/pymppost/-/blob/main/docs/Reference.md) at the University of Michigan.

Feel free to open an [issue](https://gitlab.eecs.umich.edu/umich-dnng/pymppost/issues) with bug reports, or suggestions.
