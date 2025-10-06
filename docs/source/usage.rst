Usage
=====

.. _installation:

Installation
------------

To use HOA_INSIGHTS_SURPRISEAZ, first install it using uv from root directory:

.. code-block:: console

   $ uv install .

.. _createdb:

Create Database
---------------

Before running the application, we need to setup the local and remote databases.

This can be done by running the following from the database/setup directory:

.. code-block:: console

   $ uv run db-init.py

   This creates a "__database-setup__" log file located in the database directory.

.. _run:

Running Application
-------------------

To start the application, execute the following command from the package root directory:

.. code-block:: console

   $ uv run main.py
