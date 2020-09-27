**Personnel Status Tracking Site**
-----------------------------------

This website aims to digitalise attendance taking and tracking of a group of users. This is done through 2
main components:
    - by providing a public interface for personnel to update their individual statuses conveniently, and
    - providing a protected overview page that summarises the data.


Requirements
---------------
- Python 3.x installation


Installation
-------------
Upon cloning this repository, the virtual environment as well as the required python packages are installed
by running the setup script for `Windows`_ or `Linux`_.

.. _Windows: https://github.com/HiIAmTzeKean/semb-proj/blob/Master/requirements/setup_venv.bat

.. _Linux: https://github.com/HiIAmTzeKean/semb-proj/blob/Master/requirements/setup_venv.sh


Package Management
-------------------
This repository uses `pip-tools`_ to synchronise python packages across computers. To add a new Python Package:

    1. Insert the name of the python package in ``requirements.in``.
    2. Then run `pip-compile` so that ``requirements.txt`` can be updated.
    3. Finally, run `pip-sync` to download the new packages.

.. _pip-tools: https://github.com/jazzband/pip-tools

