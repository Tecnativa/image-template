
[![Copier template](https://img.shields.io/badge/template%20engine-copier-informational)][copier]
[![MIT Software License](https://img.shields.io/github/license/tecnativa/image-template)](LICENSE)
![latest version](https://img.shields.io/github/v/release/Tecnativa/image-template?sort=semver)
# Image Template

This template aims at making it easier to configure your projects that use Docker and Python (for example, for testing) to work with Github Actions and support a CI workflow.

It uses [Copier][] to keep your projects updated with a unified GH Actions structure and configuration.

[copier]: https://copier.readthedocs.io/

## What this project adds and configures

1. **Docker automated builds with Github Actions**
1. **Python project structure for [Pytest][] with [Poetry][]** (optional)

[Pytest]: https://docs.pytest.org/
[Poetry]: https://python-poetry.org/

## 1st usage

1. [Install Copier](https://copier.readthedocs.io/en/stable/#installation)
1. Enter your project folder: `cd my-project`
1. Make it a git repo: `git init`
1. Run `copier copy https://github.com/Tecnativa/image-template.git .`
1. Answer questions
1. Commit: `git commit -am 'Apply image template'` (repeat if some pre-commit configuration you have (e.g. https://github.com/copier-org/autopretty) reformats
   anything and makes the update fail)

## Get updates

1. Enter your project folder: `cd my-project`
1. Update: `copier -a .copier-answers.image-template.yml update`
1. Answer questions, if anything changed
1. Commit: `git commit -am 'Update image template'` (repeat if pre-commit reformats
   anything and makes the update fail)
