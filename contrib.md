# Contribution Guide

## Setting up the project

1. Fork the repository to your account
2. Clone the repository to your local machine
3. Set up the project

```bash
make setup
```

This will create a virtual environment and install all the dependencies for you.

If you do not have `make` installed, you can run the following commands:

```bash
python3 -m venv venv # Create a virtual environment
source venv/bin/activate # Activate the virtual environment
pip install -r requirements.txt # Install the dependencies
```

4. Create a new branch, preferably with the name of the feature you are working on

```bash
git checkout -b <branch-name>
```

5. Make your changes
6. Run the linters and tests

```bash
make lint
make test
```

If you do not have `make` installed, you can run the following commands:

```bash
# first activate your virtual environment if you haven't already
source venv/bin/activate

# now, run the following commands
python -m mypy app --ignore-missing-imports --config-file pyproject.toml
python -m ruff check app --fix # Run the linters
python -m pytest app # Run the tests
```

7. Commit your changes

```bash
git commit -m "Your commit message"
```

8. Push your changes to your fork

```bash
git push origin <branch-name>
```

9. Create a pull request to the `main` branch of the original repository
10. Wait for the maintainers to review your changes