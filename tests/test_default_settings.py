import logging
from pathlib import Path

import jsonschema
import requests
import yaml
from copier.main import copy
from plumbum import local

logger = logging.getLogger(__name__)


def get_schema():
    """This function loads the given schema available"""
    schema_url = "https://json.schemastore.org/github-workflow.json"
    schema_path = "github-workflow.json"
    # Try to fetch directly from server to get latest version
    try:
        logger.info(f"Trying to fetch data from {schema_url}")
        data = requests.get(schema_url).content
    except requests.exceptions.RequestException:
        logger.info(f"Fetching from URL failed, using file {schema_path}")
        with open(schema_path, "r") as file:
            data = file.read()
    schema = yaml.safe_load(data)
    return schema


def validate_schema(yaml_data):
    """Validate yaml based on schema."""
    expected_schema = get_schema()
    try:
        jsonschema.validate(instance=yaml_data, schema=expected_schema)
    except jsonschema.exceptions.ValidationError as err:
        logger.error(err)
        return False
    return True


def test_default_settings(tmp_path: Path, cloned_template: Path):
    """Test that a template can be rendered from zero."""
    with local.cwd(cloned_template):
        copy(
            ".",
            str(tmp_path),
            vcs_ref="test",
            force=True,
            data={},
        )
    with local.cwd(tmp_path):
        # Check that files exist
        assert Path(".github", "workflows", "ci.yml").exists()
        assert Path(".copier-answers.image-template.yml").exists()
        # Tests are included by default
        assert Path("pytest.ini").exists()
        assert Path("pyproject.toml").exists()
        assert Path("tests/conftest.py").exists()
        # Validate CI config
        with Path(".github", "workflows", "ci.yml").open("r") as f:
            content = f.read()
            processed_content = content.replace(
                "\non:", "\n'on':"
            )  # HACK: pyyaml interprets "on" key as "True", causing a false negative on the validation function
            assert validate_schema(yaml.safe_load(processed_content))
