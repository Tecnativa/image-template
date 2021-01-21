import pytest
import yaml
from plumbum import local
from plumbum.cmd import git

with open("copier.yml") as copier_fd:
    COPIER_SETTINGS = yaml.safe_load(copier_fd)


@pytest.fixture()
def cloned_template(tmp_path_factory):
    """This repo cloned to a temporary destination.
    The clone will include dirty changes, and it will have a 'test' tag in its HEAD.
    It returns the local `Path` to the clone.
    """
    patches = [git("diff", "--cached"), git("diff")]
    with tmp_path_factory.mktemp("cloned_template_") as dirty_template_clone:
        git("clone", ".", dirty_template_clone)
        with local.cwd(dirty_template_clone):
            git("config", "commit.gpgsign", "false")
            for patch in patches:
                if patch:
                    (git["apply", "--reject"] << patch)()
                    git("add", ".")
                    git(
                        "commit",
                        "--author=Test<test@test>",
                        "--message=dirty changes",
                        "--no-verify",
                    )
            git("tag", "--force", "test")
        yield dirty_template_clone
