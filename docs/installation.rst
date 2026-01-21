Installation
============

Requirements
------------

- Python 3.12 or higher
- Git (for development installation)

Standard Installation
---------------------

Install from PyPI using pip::

    pip install nostress

Or using uv (recommended for development)::

    uv pip install nostress

Verify Installation
-------------------

After installation, verify that nostress is working correctly::

    nostress --help

You should see the main help output with available commands.

Development Installation
------------------------

For development or to get the latest features, install from source:

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

::

    git clone https://github.com/4383/nostress.git
    cd nostress

Install in Development Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using uv (recommended)::

    uv pip install -e .

Or using pip::

    pip install -e .

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

Install development dependencies for testing and linting::

    # Install development dependencies
    uv sync --group dev-test

    # Or manually with pip
    pip install -e ".[dev-test]"

Verify Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test that the installation works::

    uv run nostress --help
    uv run nostress keys generate

Run the test suite::

    uv run pytest

Virtual Environment Setup
--------------------------

It's recommended to use a virtual environment to avoid dependency conflicts.

Using uv::

    # Create project with uv (automatically manages virtual environment)
    cd nostress
    uv sync

Using venv::

    # Create virtual environment
    python -m venv venv

    # Activate on Linux/macOS
    source venv/bin/activate

    # Activate on Windows
    venv\Scripts\activate

    # Install nostress
    pip install nostress

Troubleshooting
---------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Python Version Compatibility**
    Nostress requires Python 3.12+. Check your Python version::

        python --version

**Permission Issues**
    If you encounter permission errors, try::

        pip install --user nostress

**Virtual Environment Issues**
    If you have issues with dependencies, try using a fresh virtual environment::

        python -m venv fresh_env
        source fresh_env/bin/activate  # or fresh_env\Scripts\activate on Windows
        pip install nostress

Platform-Specific Notes
~~~~~~~~~~~~~~~~~~~~~~~

**macOS**
    You might need to install build tools::

        xcode-select --install

**Windows**
    Consider using Windows Subsystem for Linux (WSL) for the best experience.

**Linux**
    Most distributions should work out of the box. For older distributions,
    ensure you have Python 3.12+ from a backports repository.

Updating
--------

To update to the latest version::

    pip install --upgrade nostress

Or with uv::

    uv pip install --upgrade nostress

Uninstallation
--------------

To remove nostress::

    pip uninstall nostress

Or with uv::

    uv pip uninstall nostress
