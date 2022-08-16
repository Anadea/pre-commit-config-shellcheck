pre-commit-config-shellcheck documentation
==========================================

|GitHub|_ |Coveralls|_ |pypi-license|_ |pypi-version|_ |pypi-python-version|_ |pypi-format|_ |pypi-wheel|_ |pypi-status|_

*pre-commit-config-shellcheck is a tool for checking entry points in the pre-commit config with ShellCheck.*

.. contents::

Installation
------------
In order to use the tool you should first clone it from the source:

.. code-block:: bash

    $ git clone https://github.com/Anadea/pre-commit-config-shellcheck.git

Then you should install project dependencies with

.. code-block:: bash

    $ python ./setup.py install

or

.. code-block:: bash

    $ pip install pre-commit-config-shellcheck

The installation is done and as simple as that.

Usage
-----
To run the program you should start it from the terminal and provide a config file to check:

.. code-block:: bash

    $ pre_commit_config_shellcheck.py .pre-commit-config.yaml

You could change a default ShellCheck call with directory access with the ``-s`` or ``--shellcheck`` argument:

.. code-block:: bash

    $ pre_commit_config_shellcheck.py .pre-commit-config.yaml -s /bin/shellcheck

The output from tool usage is sent to the stdout or stderr depending on the operation result.

Usage as a pre-commit hook
--------------------------
Also, it can be used as a `pre-commit <https://pre-commit.com/>`_ hook out of the box. Just add it to yours ``.pre-commit-config.yaml``:

.. code-block:: yaml

  - repo: "https://github.com/Anadea/pre-commit-config-shellcheck"
    rev: "0.3.4"
      hooks:
        - id: "pre-commit-config-shellcheck"

Usage as GitHub action
----------------------
Also, it can be used as a `GitHub action <https://github.com/features/actions/>`_ out of the box. Just add it to yours workflow:

.. code-block:: yaml

  - name: "pre-commit-config-shellcheck"
    uses: "actions/pre-commit-config-shellcheck@0.3.4"
    id: "pre-commit-config-shellcheck"
    with:
      config: ".pre-commit-config.yaml"


Contributing
------------

- `Fork it <https://github.com/Anadea/pre-commit-config-shellcheck/>`_
- Install `GNU Make <https://www.gnu.org/software/make/>`_
- Install and configure `pyenv <https://github.com/pyenv/pyenv/>`_ and `pyenv-virtualenv plugin <https://github.com/pyenv/pyenv-virtualenv/>`_
- Install and configure `direnv <https://github.com/direnv/direnv/>`_
- Create environment config from the example

.. code-block:: bash

    cp .env.example .env

- Install development dependencies:

.. code-block:: bash

    make install

- Create your fix/feature branch:

.. code-block:: bash

    git checkout -b my-new-fix-or-feature

- Check code style and moreover:

.. code-block:: bash

    make check

- Run tests:

.. code-block:: bash

    make test

- Push to the branch:

.. code-block:: bash

    git push origin my-new-fix-or-feature

- `Create a new Pull Request <https://github.com/Anadea/pre-commit-config-shellcheck/compare/>`_


Licensing
---------
pre-commit-config-shellcheck uses the MIT license. Please check the MIT-LICENSE file for more details.


Contacts
--------
**Project Website**: https://github.com/Anadea/pre-commit-config-shellcheck/

**Author**: Anadea

For contributors list see CONTRIBUTORS file.


.. |GitHub| image:: https://github.com/Anadea/pre-commit-config-shellcheck/workflows/build/badge.svg
    :alt: GitHub
.. |Coveralls| image:: https://coveralls.io/repos/github/Anadea/pre-commit-config-shellcheck/badge.svg?branch=master
    :alt: Coveralls
.. |pypi-license| image:: https://img.shields.io/pypi/l/pre-commit-config-shellcheck
    :alt: License
.. |pypi-version| image:: https://img.shields.io/pypi/v/pre-commit-config-shellcheck
    :alt: Version
.. |pypi-python-version| image:: https://img.shields.io/pypi/pyversions/pre-commit-config-shellcheck
    :alt: Supported Python version
.. |pypi-format| image:: https://img.shields.io/pypi/format/pre-commit-config-shellcheck
    :alt: Package format
.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/pre-commit-config-shellcheck
    :alt: Python wheel support
.. |pypi-status| image:: https://img.shields.io/pypi/status/pre-commit-config-shellcheck
    :alt: Package status
.. _GitHub: https://github.com/Anadea/pre-commit-config-shellcheck/actions/
.. _Coveralls: https://coveralls.io/github/Anadea/pre-commit-config-shellcheck?branch=master
.. _pypi-license: https://pypi.org/project/pre-commit-config-shellcheck/
.. _pypi-version: https://pypi.org/project/pre-commit-config-shellcheck/
.. _pypi-python-version: https://pypi.org/project/pre-commit-config-shellcheck/
.. _pypi-format: https://pypi.org/project/pre-commit-config-shellcheck/
.. _pypi-wheel: https://pypi.org/project/pre-commit-config-shellcheck/
.. _pypi-status: https://pypi.org/project/pre-commit-config-shellcheck/
