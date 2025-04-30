# List all available recipes
default:
    just --list

# Check that all required tools are installed
[group("installation")]
check-versions:
    uv --version  # https://docs.astral.sh/uv/
    just --version  # https://github.com/casey/just

# Create virtual environment and install dependencies
[group("installation")]
create-venv:
    uv sync

# Install pre-commit hooks
[group("installation")]
install-pre-commit:
    uv run pre-commit install

# Run all project setup steps (assumes uv and just are installed)
[group("installation")]
setup: create-venv install-pre-commit

# Run pre-commit hooks
[group("linting, formatting & testing")]
pre-commit:
    uv run pre-commit run --all

# Run tests
[group("linting, formatting & testing")]
test:
    uv run pytest

# Run tests with coverage report
[group("linting, formatting & testing")]
test-cov:
    uv run pytest --cov=src --cov-report=html

# Create a new version tag (will trigger publish.yaml workflow)
[group("packaging")]
publish:
    #!/usr/bin/env bash
    # Get last tag from git
    CURRENT_VERSION=$(git describe --tags --abbrev=0)
    echo "Current version: $CURRENT_VERSION"

    # Remove 'v' prefix if it exists
    VERSION_NUMBER=$(echo $CURRENT_VERSION | sed 's/^v//')

    # Split version into major.minor.patch
    IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION_NUMBER"

    # Increment patch version
    NEW_PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

    # Create git tag (always with 'v' prefix)
    NEW_TAG="v$NEW_VERSION"
    echo "New version: $NEW_TAG"

    # Create and push the new tag
    git tag -a "$NEW_TAG" -m "Release version $NEW_VERSION"
    git push origin "$NEW_TAG"

# Print tree of the project (requires installing tree)
[group("tools")]
tree:
    tree -a -I ".venv|.git|.pytest_cache|.coverage|dist|__pycache__" --dirsfirst
