# Python Lab 6 - OOP Monaco Report

This Python application implements the **Monaco Racing Report** using an object-oriented programming (OOP) approach.

---

## Table of Contents
- [Installation](#installation)
- [Examples](#examples)
  - [Run from a Python Script](#run-from-a-python-script)
  - [Run from the Command Line Interface (CLI)](#run-from-the-command-line-interface-cli)
- [Publishing to PyPI](#publishing-to-pypi)

---

## Installation

You can install the package using either `uv` or `pip`:

### Using `uv`:

```bash
uv pip install lab6_monaco_oleksiisaiun
```

### Using `pip`:

```bash
pip3 install lab6_monaco_oleksiisaiun
```

---

## Examples

### Run from a Python Script

```python
from lab6_monaco_oleksiisaiun.race_report import get_monaco_race_records

print(get_monaco_race_records())
```

---

### Run from the Command Line Interface (CLI)

```bash
python3 -c "from lab6_monaco_oleksiisaiun.race_report import get_monaco_race_records; print(get_monaco_race_records())"
```

---

## Publishing to PyPI

You can publish the package to PyPI using `uv`.

### Step 1: Navigate to the Root Folder

```bash
cd /path/to/your/package
```

### Step 2: Build and Publish

```bash
uv build
uv publish --token [YOUR_PYPI_TOKEN]
```

---
