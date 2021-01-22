import logging
from pathlib import Path

import jsonschema
import yaml
from copier.main import copy
from plumbum import local

logger = logging.getLogger(__name__)


def get_gh_workflows_schema(cloned_template: Path):
    """This function loads the given GH Workflows schema available"""
    schema_file = Path(
        cloned_template,
        "tests",
        "schemastore",
        "src",
        "schemas",
        "json",
        "github-workflow.json",
    )
    with schema_file.open("r") as file:
        data = file.read()
    schema = yaml.safe_load(data)
    return schema


def validate_schema(yaml_data, cloned_template: Path):
    """Validate GH Workflows yaml based on expected schema."""
    expected_schema = get_gh_workflows_schema(cloned_template)
    jsonschema.validate(instance=yaml_data, schema=expected_schema)


def test_default_settings(tmp_path: Path, cloned_template: Path):
    """Test that a template can be rendered from zero."""
    with local.cwd(cloned_template):
        copy(
            ".",
            str(tmp_path),
            vcs_ref="test",
            force=True,
            data={
                "project_name": "docker-test",
                "project_owner": "Test",
                "dockerhub_image": "test/test",
            },
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
            yaml_data = yaml.safe_load(content)
            # Ensure project data propagated
            assert (
                yaml_data["jobs"]["build-push"]["env"]["DOCKERHUB_IMAGE_NAME"]
                == "test/test"
            )
            # Validate according to Github Actions expected syntax
            validate_schema(yaml_data, cloned_template)


def test_no_pytest_settings(tmp_path: Path, cloned_template: Path):
    """Test that a template can be rendered from zero with different input data."""
    with local.cwd(cloned_template):
        copy(
            ".",
            str(tmp_path),
            vcs_ref="test",
            force=True,
            data={
                "project_name": "docker-test",
                "project_owner": "Test",
                "dockerhub_image": "test/test",
                "pytest": False,
            },
        )
    with local.cwd(tmp_path):
        # Check that files exist
        assert Path(".github", "workflows", "ci.yml").exists()
        assert Path(".copier-answers.image-template.yml").exists()
        # Tests shouldn't exist
        assert not Path("pytest.ini").exists()
        assert not Path("pyproject.toml").exists()
        assert not Path("tests/conftest.py").exists()
        # Validate CI config
        with Path(".github", "workflows", "ci.yml").open("r") as f:
            content = f.read()
            yaml_data = yaml.safe_load(content)
            # Validate according to Github Actions expected syntax
            validate_schema(yaml_data, cloned_template)
