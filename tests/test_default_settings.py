from pathlib import Path

from copier.main import copy
from plumbum import local
from plumbum.cmd import git


def test_default_settings(tmp_path: Path, cloned_template: Path):
    """Test that a template can be rendered from zero for each version."""
    with local.cwd(cloned_template):
        copy(
            ".",
            str(tmp_path),
            vcs_ref="test",
            force=True,
            data={},
        )
    with local.cwd(tmp_path):
        # TODO When copier runs pre-commit before extracting diff, make sure
        # here that it works as expected
        Path(".github", "worflows", "ci.yml")
        git("init")
        git("add", ".")
        git("commit", "-am", "Hello World")
