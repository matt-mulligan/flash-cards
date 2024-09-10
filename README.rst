Flash Cards
=============

CLI application for running flash cards and rote memorisation


Project Toolchain
------------------

This project aims to follow software engineering best practices wherever possible and makes heavy use of automated
tooling to enable/enforce this. Below is the chosen toolchain for this project

* Build System - `Poetry <https://python-poetry.org/docs/>`__
* Dependency Management - `Poetry <https://python-poetry.org/docs/>`__
* Test Framework - `Pytest <https://docs.pytest.org/en/8.2.x/>`__
* Code Linting - `Ruff Linter <https://docs.astral.sh/ruff/linter/>`__
* Code Formatting - `Ruff Formatter <https://docs.astral.sh/ruff/formatter/>`__
* Type Checking - `MyPy <https://www.mypy-lang.org/>`__
* Pre Commit Checks - `Pre-Commit <https://pre-commit.com/>`__
* CICD - `Github Actions <https://github.com/features/actions>`__


Build System - Poetry
^^^^^^^^^^^^^^^^^^^^^^

*Build System* defines what tool is responsible for building your python project into a distribution. For this project
we use `Poetry <https://python-poetry.org/docs/>`__ to build this product into a wheel file. Poetry was chosen
because of its simple interface and ability to also manage dependencies (both production and development) as well as
the ability to publish direct to PyPi should we wish to publish this product in the future.

Configuration of poetry as our build system is managed within the ``pyproject.toml`` file of this project.


Dependency / Venv Management - Poetry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Dependency Management* refers to managing what external packages are required for your python product to run, as
well as what additional dependencies are required while developing and testing your product. For this project we use
`Poetry <https://python-poetry.org/docs/>`__ to manage our dependencies. Poetry was chosen because of its
simple interface and ability to group dependencies to allow for cleaner install sets in different environments.

Configuration of poetry as our dependency management system is managed within the ``pyproject.toml`` file
of this project.


Test Framework - Pytest
^^^^^^^^^^^^^^^^^^^^^^^^

*Test Frameworks* are libraies responsible for enabling and running automated testing on the product.
For this project we use `Pytest <https://docs.pytest.org/en/8.2.x/>`__ as our test framework. Pytest was chosen
for its incredible flexibility and extensive plugin library.

Configuration for pytest can be found in ``conftest.py`` files within our ``/tests`` folders


Code Linting - Ruff
^^^^^^^^^^^^^^^^^^^^

*Code Linting* is the process of performing static code analysis to flag programming errors, bugs, stylistic errors
and suspicious constructs. This project uses the `Ruff Linter <https://docs.astral.sh/ruff/linter/>`__ to
perform linting over the entire codebase. Ruff was chosen as it is extremely fast (written in rust) and has the
ability to replace multiple other tools used in previous projects. In terms of linting, ruff linter can replace
the following other tools typically used in python projects:

* `Flake8 <https://docs.astral.sh/ruff/faq/#how-does-ruffs-linter-compare-to-flake8>`__
* `Isort <https://docs.astral.sh/ruff/faq/#how-does-ruffs-import-sorting-compare-to-isort>`__
* `Pylint <https://docs.astral.sh/ruff/faq/#how-does-ruffs-linter-compare-to-pylint>`__
* `Bandit <https://github.com/astral-sh/ruff/issues/1646>`__
* `Pyupgrade <https://docs.astral.sh/ruff/rules/#pyupgrade-up>`__

The ruff linter should be used with the ``ruff check --fix`` option when used on developer environments to
ensure all safe fixes are automatically applied. In CICD environments fixes will not be automatically applied.

Configuration of ruff as our linting tool is managed within the ``pyproject.toml`` file of this project.


Code Formatting - Ruff
^^^^^^^^^^^^^^^^^^^^^^^

*Code Formatting* is the process of ensuring all modules within a product follow the same standards and conventions
for layout to ensure that all modules have a cohesive look and feel, making PR diffs much simpler to reason.
This project uses `Ruff Formatter <https://docs.astral.sh/ruff/formatter/>`__ to perform formatting on all modules.
Ruff formatter was chosen for this project for its ease of use and its
`black-compliant code conventions <https://docs.astral.sh/ruff/formatter/#black-compatibility>`__

Configuration of ruff as our formatting tool is managed within the ``pyproject.toml`` file of this project.


Type Checking - MyPy
^^^^^^^^^^^^^^^^^^^^^

*Type Checking* is the process of validating via static code analysis that type hinting is provided and accurate
for all methods and functions when compared to the code of the method/function. This project uses
`MyPy <https://www.mypy-lang.org/>`__ to perform type checking. MyPy was chosen for this project due to its
flexibility and ability to detect incorrect usage of typed functions/methods.

Configuration of MyPy as our type checking tool is managed within the ``pyproject.toml`` file of this project.


Pre Commit Checks - Pre-Commit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Pre Commit Checks* are a way of running automated checks on developers workstations before any commit to git occurs.
This is done to ensure certain standards are always met for the project. This project uses
`Pre-Commit <https://pre-commit.com/>`__ to configure the pre-commit checks required for all commits.
This library was chosen for its flexibility to incorporate multiple different checks and wide-spread support for
the above tools in our toolchain.

Pre-commits for this project cover the following areas and tools:

* Code Linting (with safe fixes)
* Code Formatting (with safe fixes)
* Type Checking
* Unit Testing

Configuration of Pre Commit for this project is managed within the ``.pre-commit-config.yaml`` file of this project.


CICD - Github Actions
^^^^^^^^^^^^^^^^^^^^^^

*CICD* refers to "Continuous Integration, Continuous Deployment" which are automated processes triggered by
commits and PRs within a source repository that run standard checks and evaluations on code. This project uses
`Github Actions <https://github.com/features/actions>`__ to orchestrate its CICD workflows. Github actions was
chosen for this project as we already use GitHub for our source code repository and Github actions was a simple
integration choice.
