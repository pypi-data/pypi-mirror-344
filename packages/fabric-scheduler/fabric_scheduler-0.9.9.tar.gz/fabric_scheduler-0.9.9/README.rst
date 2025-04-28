.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/fabric_scheduler.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/fabric_scheduler
    .. image:: https://readthedocs.org/projects/fabric_scheduler/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://fabric_scheduler.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/pypi/v/fabric_scheduler.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/fabric_scheduler/

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=================
Fabric Scheduler
=================


Artifact Scheduler for Microsoft Fabric
=======================================

A Python API wrapper for scheduling Fabric artifacts (Notebooks, Dataflows, Pipelines) using the Fabric REST API. This module provides:

- Automated scheduling of Fabric artifacts
- Input validation and error handling
- Multiple input methods (dictionary, CSV file, CSV string)
- Schedule management (create, retrieve, delete)

.. note::
    This package is designed exclusively for use within Microsoft Fabric notebooks and integrates with the Microsoft Fabric REST API.

Getting Started
================

Prerequisites
-------------

- Python 3.8+
- Required packages:

  - pandas
  - sempy.fabric

Installation & Setup
--------------------

1. Install the package:

   .. code-block:: bash

      pip install fabric_scheduler

2. Import the module:

   .. code-block:: python

      from fabric_scheduler import ArtifactScheduler

Basic Usage
===========

.. code-block:: python

    # Initialize scheduler
    scheduler = ArtifactScheduler()
    # OR ArtifactScheduler(workspace_id="your-workspace-id")

    # Set artifacts to schedule from list of dictionaries
    artifacts = [
        {
            "displayName": "MyNotebook",
            "type": "Notebook",
            "schedule type": "Daily",
            "times": ["08:00", "17:00"]
        },
        {
            "displayName": "MyDataflow",
            "type": "Dataflow",
            "schedule type": "Weekly",
            "weekdays": ["Monday", "Wednesday"],
            "times": ["10:00"]
        }
    ]
    scheduler.set_artifacts(artifacts)

    # Create schedules
    scheduler.create_schedules()


Input Methods
-------------

1. **Dictionary Input**:
   Define a list of dictionaries with familiar notation like JSON,
   and pass it to the ``set_artifacts`` method.

   .. code-block:: python

      scheduler.set_artifacts([{artifact_dict}])

2. **CSV File Path**:
   Upload the CSV file and pass the file name to the ``load_artifacts_from_csv`` method.

   .. code-block:: python

      scheduler.load_artifacts_from_csv("artifact_schedule.csv")

3. **CSV String**:
   Pass a CSV string directly to the ``load_artifacts_from_csv`` method.

   .. code-block:: python

      csv_content = '''
      displayName,type,enabled,schedule type,localTimeZone,startDate,startTime,endDate,endTime,interval,times,weekdays
      MyNotebook,Notebook,true,Cron,,3/30/2025,2:00,,,240,,
      MyDataflow,Dataflow,true,Cron,,,,,,240,,
      '''
      scheduler.load_artifacts_from_csv(csv_content)

Development
===========

This project uses modern Python development tools for quality assurance:

- **tox**: For automating testing, linting, and build tasks
- **pre-commit**: For automated code quality checks before commits
- **sphinx**: For documentation generation

For details on setting up the development environment, see the `CONTRIBUTING.rst` file and the `docs/pre-commit.md` document.
