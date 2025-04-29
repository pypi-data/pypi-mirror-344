<div style="text-align:center">
<img src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/somos/config/svg/pyPCBanner-C.png" alt="SOMOs" width="1000"/>
</div>

> **Versions [0.9.0] - [1.0.1] - 2024-04-28**
>
> **Changed**
>
> - logo is now gSOMOs instead of SOMOs
> - in the projection scheme (`proj.py`), there are now two criteria to identify a SOMO, namely "SOMO P2v?" (formerly SOMO?) and "SOMO dom. β MO?" (see scientific documentation)
>     - SOMOs identified according to the P^2_virtual criterion are highlighted in green
>     - SOMOs identified only on the basis of a dominant virtual beta MO are highlighted in orange (weaker criterion)
> - Scientific documentation renamed `gSOMOs.pdf`. And content updated
> - gSOMOs-v3.pdf scientific document now downloadable in `gsomos.readthedocs.io`
> - Images in README.md now point to their `https://raw.githubusercontent.com` counterpart
> - Update of `DOCUMENTATION_setup.md`, `PUBLISHING.md`
> - Link toward the Jupyter notebook with examples and a log zip file with two Gaussian logs in `DOCUMENTATION_setup.md` and in `README.md`
> - SOMOs of the iron complex shown in `gSOMOS-v3.pdf`
>
> **Added**
>
> - new analyzis scheme in `proj.py`: bases on the diagonalization of projection matrices
> - new `io.clean_logfile_name()` function (made to solve a prefix issue for X.log.gz files)
> - Short examples in the documentation
> - docstring for `projection_heatmap_from_df`
> - docstring of `show_alpha_to_homo` translated in English
> - updated *Installation* section in `README.md`
> - basic instructions to install miniconda, in `README.md`
> - jMol index of beta virtual MOs in the output of `proj.summarize_somo_candidates()`
>
> **Fixed**
> 
> - minor fixes
> - wrong initialization of `visualID_Eng` at the beginning of the notebook, and tricky issues
> 

# gSOMOs

🔗 Available on [PyPI](https://pypi.org/project/gSOMOs/)

A Python library to identify and analyze Singly Occupied Molecular Orbitals (SOMOs) from Gaussian 09 or Gaussian 16 `.log` files.

[![PyPI version](https://img.shields.io/pypi/v/gSOMOs.svg?color=blue)](https://pypi.org/project/gSOMOs/)
[![Documentation Status](https://readthedocs.org/projects/gsomos/badge/?version=latest)](https://gsomos.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/rpoteau/gSOMOs)](https://github.com/rpoteau/gSOMOs/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-brightgreen.svg)](https://www.python.org/downloads/)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](https://github.com/rpoteau/gSOMOs)


<hr style="height:3px; background-color:#00aaaa; border:none;" />

## 🛠️ Installation

### ⚡ Quickstart

1. Open a terminal:

- On Linux/macOS: open a Terminal (bash)

- On Windows: open PowerShell 

2. (Recommended) Set up a local virtual environment inside your project folder using [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

    ```bash
    # Create, if necessary, a project folder
    mkdir my-project-folder

    # Move to your project directory
    cd my-project-folder

    # Create the virtual environment
    virtualenv gSOMOS-venv # or any other name that has nothing to do with gSOMOS

    # Activate the environment
    source gSOMOS-venv/bin/activate   # On Linux/macOS
    # or
    gSOMOS-venv\Scripts\activate      # On Windows
    ```

3. Install gSOMOs inside the environment:

    ```bash
    pip install gSOMOs
    ```

📦 All necessary Python packages will be installed automatically !

---

### 📋 Requirements

- 🐍 Python ≥ 3.8 (Windows users: [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) is recommended, see installation instructions at the end of this document)
- 📦 A working installation of [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- 🔄 An up-to-date version of `pip` (`python -m pip install --upgrade pip`)

---

### 📝 Notes

- Keeping the virtual environment inside the project folder makes it easier to manage and remove if needed.
- To deactivate the environment at any time, simply type:

    ```bash
    deactivate
    ```


<hr style="height:3px; background-color:#00aaaa; border:none;" />

## 🔎 Capabilities Overview

`SOMOs` is a Python toolkit for analyzing **molecular orbitals** (MOs) from Gaussian log files, with a focus on identifying **SOMOs** (Singly Occupied Molecular Orbitals) in open-shell systems.

---

### 🚀 Main Features

```python
from somos import io # optional
from somos import cosim, proj
```

#### Load Gaussian Log Files
- Parses `.log` and `.log.gz` Gaussian output files
- Extracts orbital energies, coefficients, overlap matrices, and spin

#### Cosine Similarity & SOMO Detection
- Computes cosine similarities between alpha and beta orbitals
- Identifies SOMO candidates from orbital projections

#### Projection-Based Analysis
- Projects occupied and virtual alpha MOs onto virtual beta MOs
- Decomposes projection matrix to extract leading contributions

---

### 📊 Visualization Tools

#### Heatmaps
- Interactive or static heatmaps of MO similarities

<div style="text-align: center;">
  <img src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/doc-latex/H2CO_T1_projection_heatmap-C.png" alt="heatmap" width="600px">
</div>

#### t-SNE (Dimensionality Reduction)
- Projects high-dimensional orbital space to 2D for visual exploration
- Enables inspection of orbital families and similarity patterns

<div style="text-align: center;">
  <img src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/doc-latex/H2CO_T1_tSNE-C.png" alt="tSNE" width="600px">
</div>

---

### 📁 Output
- `.xlsx` tables of SOMO similarity and projections
- `.png` images of heatmaps and projections
- All results saved in the `logs/` folder
- well-organized dataframes and printing

```
=== Summary of SOMO candidates ===

──────────── SOMO Candidate #1 ────────────
  α occupied contributions:
    • α 9 (99.5%)
  β virtual projections:
    • β 9 (96.4%) [jMol: 55]

──────────── SOMO Candidate #2 ────────────
  α occupied contributions:
    • α 8 (89.4%)
  β virtual projections:
    • β 8 (98.4%) [jMol: 54]
```

<hr style="height:3px; background-color:#00aaaa; border:none;" />

## 🧠 Examples and Documentation

### ✅ Examples Used in Notebooks (compressed Gaussian files)
- `logs/H2CO_T1.log.gz`
- `logs/FeComplex.log.gz`

---

### 📓 Example Jupyter Notebook

An example notebook demonstrating gSOMOs usage is available at: [gSOMOs Examples Notebook on GitHub](https://github.com/rpoteau/gSOMOs/blob/main/SOMOs-examples.ipynb). Save it in `my-project-folder`.

Also download the [logs/ folder](https://github.com/rpoteau/gSOMOs/blob/main/logs.zip) with the two examples. Store it also in `my-project-folder`.

---

### 📚 Technical and scientific documentation

This [document](https://github.com/rpoteau/gSOMOs/blob/main/doc-latex/gSOMOS-v3.pdf) describes two complementary methods to identify singly occupied molecular orbitals (SOMOs) in open-shell systems:
- **Orbital projection analysis**, where occupied α orbitals are projected onto the β orbital basis using the AO overlap matrix;
- **Cosine similarity mapping**, which computes the angular similarity between α and β orbitals and matches them using the Kuhn–Munkres (Hungarian) algorithm.

The two examples, which involve finding the SOMOs of the lowest triplet state (*T*<sub>1</sub>) of formaldehyde (H<sub>2</sub>CO) and the lowest quintet state of an iron complex, are discussed in this document.

<hr style="height:3px; background-color:#00aaaa; border:none;" />

# 🛠️ Installing miniconda

## ⬇️ Download the installer

- download the [installer for your OS](https://docs.anaconda.com/miniconda/) (Windows/macOS/linux)

- execute it:
    - **Windows**: go to the download directory, double click on the `Miniconda3-latest-Linux-x86_64.exe` icon
    - **Linux**: open a terminal, `cd` to the download directory, type `bash Miniconda3-latest-Linux-x86_64.sh` 

- during the installation process:
    - validate the license agreement
    - choose the installation folder - or accept the folder defined by default:
        - **Windows**: `C:\Users\<first-letters-of-your-username>\miniconda3`
        - **Linux** : `/home/<your-username>/miniconda3`)
    - finalize the installation
        - **Windows**: select the Advanced Configuration Options. Do not select the "*Add Miniconda3 to my PATH environment variable*" checkbox if you fear a conflict with another python distribution that would you have in your local account.

        <div style="text-align:center"><img width="500px" src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/figs/Anaconda-Miniconda-AdvancedInstallation-C.png"/></div>

        - **Linux**: you need to answer a question about the PYTHONPATH environment variable. Answer no if you fear a conflict with another python distribution that would you have in your local account.
        
        <div style="text-align:center"><img width="700px" src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/figs/Linux-endOfMinicondaInstall-C.png"/></div>

**Whatever the OS of your computer is, you end up with a "base" python distribution, provided and manageable with conda. Given the PATH environment selection chosen during the installation, you might have to activate the python environment**

## 🔄 Activation of a conda environment

### Windows

- search for the **Anaconda Powershell Prompt** application in the search field:
- execute it. You should see a terminal, with a `(base) PS C:\Users\<first-letters-of-your-username>>` prompt:
    <div style="text-align:center"><img width="500px" src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/figs/Windows-AnacondaPowerShellPrompt-C.png"/></div>

### Linux

- open a terminal

- type the command:

    ```bash
    eval "$(/home/<your-username>/miniconda3/bin/conda shell.bash hook)"
    ```

    The prompt should now start with `(base)`:
     <div style="text-align:center"><img width="600px" src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/figs/Linux-activationOfConda-C.png"/></div>

- to deactivate the "base" python environment of conda, type:</span>

    ```bash
    conda deactivate
    ```

<hr style="height:3px; background-color:#00aaaa; border:none;" />

