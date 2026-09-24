# Roborregos@Home Docs

RoBorregos Official Documentation for the RoboCup@Home competition.

This documentation is based on mkdocs, using the material theme.

## Run locally

To run the documentation locally, you need to have python installed.

1. Clone the repository

```bash
git clone https://github.com/RoBorregos/Home-Docs.git
```

2. Install the requirements

```
pip install -r requirements.txt -r requirements-docs.txt
```

`requirements.txt` holds what the chatbot needs at runtime (it is what the host
bundles into the function); `requirements-docs.txt` holds the site toolchain.

3. Run the server

```bash
mkdocs serve
```

4. If you encounter issues with the command not being found try the following

```bash
python -m mkdocs serve
```

5. Open the browser and go to http://localhost:8000

## Test

Run formatting tests

```bash
pip install -r requirements_test.txt
# At root directory of project
pytest
```