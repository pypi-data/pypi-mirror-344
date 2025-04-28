# 🧪 How to Build the HTML Documentation for SOMOs (with Sphinx)

This guide explains how to build a full HTML documentation for the SOMOs package using **Sphinx**.

---

## ✅ 1. Install Required Packages

```bash
pip install sphinx sphinx_rtd_theme myst-parser numpydoc

```

Optional:
```bash
pip install sphinx-autodoc-typehints
```

---

## 🛠️ 2. Initialize the Sphinx project

In the root folder of the project:

```bash
sphinx-quickstart docs
```

Answers:
- Separate source and build dirs → yes
- Project name → SOMOs
- Author name → Romuald Poteau
- Use Makefile → yes

---

## ✏️ 3. Edit `docs/source/conf.py`

Make sure it includes:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'myst_parser',
    'numpydoc',
]

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
html_extra_path = ['_static']
```

---

## 🛠️ Explanation: `html_static_path` vs `html_extra_path`

- `html_static_path = ['_static']`
  - ➔ Tells Sphinx where to find **static assets** like CSS files, JS files, and local images used for theming or layout.
- `html_extra_path = ['_static']`
  - ➔ Tells Sphinx to **copy raw files (PDFs, datasets, etc.)** into the final built HTML folder, so they are downloadable.

✅ You can safely use both for `_static/` if you want to include custom styles **and** downloadable files like `.pdf`.

---

## 🧱 4. Edit `docs/source/index.rst`

```rst
Welcome to SOMOs's documentation!
=================================

.. automodule:: somos.io
   :members:
   :undoc-members:

.. automodule:: somos.cosim
   :members:
   :undoc-members:

.. automodule:: somos.proj
   :members:
   :undoc-members:
```

---

## 🚀 5. Build the documentation

From the `docs/` directory:

```bash
make html
```

Open the generated file:

```
docs/build/html/index.html
```

That's your full HTML documentation!

✅ You can check your site locally before publishing.

---

## 🌍 6. Publish on ReadTheDocs

### 🔹 Step 1: Create an Account on ReadTheDocs

- Go to [https://readthedocs.org/](https://readthedocs.org/)
- Sign up (you can use your GitHub account directly).

### 🔹 Step 2: Connect Your GitHub Repository

- Import a project.
- Authorize ReadTheDocs to access your GitHub repositories.
- Select `gSOMOs` from your repositories list.

### 🔹 Step 3: Configure the Build

- Branch: `main`
- Documentation path: `docs/`
- Configuration file: `docs/source/conf.py`

✅ RTD will detect your `.readthedocs.yaml` (if any) or default settings.

### 🔹 Step 4: Trigger First Build

- Save the configuration.
- ReadTheDocs will fetch your GitHub project, install dependencies, build HTML, and publish it.

✅ Your doc will be available at:
```
https://gsomos.readthedocs.io/
```

---

# ✅ You are done!

You now have:
- A locally buildable documentation (`make html`)
- A publicly accessible website (`https://gsomos.readthedocs.io/`)
- Automatic rebuild on every GitHub push 🚀

---



