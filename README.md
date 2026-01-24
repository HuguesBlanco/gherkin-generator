# Gherkin Generator

A proof-of-concept Python app using LangGraph to convert Playwright recorder scripts into Gherkin tests.

## 1. Initial Setup (One-time)

Do these steps only once after cloning the project.

### 1.1 Prerequisites (Debian/Ubuntu)

If you haven't already, install the virtual environment support:

```bash
sudo apt update
sudo apt install python3.13-venv
```

### 1.2 Create Virtual Environment

```bash
python3 -m venv venv
```

### 1.3 Install Dependencies

```bash
# This installs the project in "editable" mode (-e)
# Changes to your files will be reflected immediately without re-installing.
source venv/bin/activate
pip install -e .
```

## 2. Daily Development (Every session)

Do these steps every time you open a new terminal to work on the project.

### 2.1 Activate Environment

```bash
source venv/bin/activate
```

### 2.2 Running the App

```bash
python main.py
```
