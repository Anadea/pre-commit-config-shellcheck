pre-commit-config-shellcheck documentation
==========================================

*pre-commit-config-shellcheck is a tool for checking entry points in pre-commit config with shellcheck.*


Installation
------------

In order to use the tool you should first clone it from the source:

.. code-block:: bash

    $ git clone https://newgit.anadea.co/anadea/randd/pre-commit-config-shellcheck.git

Then you should install project dependencies with

.. code-block:: bash

    $ python ./setup.py install

or

.. code-block:: bash

    $ pip install pre-commit-config-shellcheck

The installation is done and as simple as that.


Usage
-----

To run the program you should start it from terminal and provide with a config file to check:

.. code-block:: bash

    $ python pre_commit_config_shellcheck.py .pre-commit-config.yaml

You could change a default shellcheck call with directory access with the ``-s`` or ``--shellcheck`` argument:

.. code-block:: bash

    $ python pre_commit_config_shellcheck.py .pre-commit-config.yaml -s /bin/shellcheck

The output from tool usage is sent to the stdout or stderr depending on the operation result.


Contributing
------------

- Fork the repository
- Install `GNU Make <https://www.gnu.org/software/make/>`_
- Install and configure `pyenv <https://github.com/pyenv/pyenv/>`_ and `pyenv-virtualenv plugin <https://github.com/pyenv/pyenv-virtualenv/>`_
- Install and configure `direnv <https://github.com/direnv/direnv/>`_
- Create environment config from example

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

- Create a new Pull Request


Licensing
---------

pre-commit-config-shellcheck uses the MIT license. Please check the MIT-LICENSE file for more details.


Contacts
--------

**Project Website**: https://newgit.anadea.co/anadea/randd/pre-commit-config-shellcheck

**Author**: Anadea

For contributors list see CONTRIBUTORS file.
