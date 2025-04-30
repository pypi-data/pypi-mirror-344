=================
Fabric Scheduler
=================

.. _url_definitions:

.. URLs for badges and documentation references
.. These are hidden from direct view but used throughout documentation

.. _url_docs: https://fabric-scheduler.readthedocs.io/en/stable/
.. _url_pypi: https://pypi.org/project/fabric-scheduler/
.. _url_pypi_downloads: https://pypi.org/project/fabric-scheduler/#files
.. _url_python: https://www.python.org/
.. _url_pyscaffold: https://pyscaffold.org/
.. _url_opensource: https://opensource.org/
.. _url_github: https://github.com/shahlaukik/fabric_scheduler
.. _url_releases: https://github.com/shahlaukik/fabric_scheduler/releases/latest
.. _url_issues: https://github.com/shahlaukik/fabric_scheduler/issues


.. image:: https://readthedocs.org/projects/fabric_scheduler/badge/?version=latest
    :alt: ReadTheDocs
    :target: url_docs_
.. image:: https://img.shields.io/pypi/v/fabric-scheduler.svg
    :alt: PyPI-Server
    :target: url_pypi_
.. image:: https://img.shields.io/pypi/dm/fabric-scheduler
    :alt: PyPI - Downloads
    :target: url_pypi_downloads_
.. image:: https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=ffffff
    :alt: Python
    :target: url_python_
.. image:: https://img.shields.io/pypi/l/fabric-scheduler
    :alt: PyPI - License

|

**Fabric Scheduler** is a comprehensive Python API wrapper that simplifies the scheduling of Microsoft Fabric artifacts (Notebooks, Dataflows, Pipelines) using the Fabric REST API.

.. note::
    This package is designed exclusively for use within Microsoft Fabric notebooks and integrates with the Microsoft Fabric REST API.

Key Features
============

- **Automated Scheduling**: Create and manage schedules for Fabric artifacts with minimal code
- **Multiple Input Methods**: Use dictionaries, CSV files, or CSV strings to define schedules
- **Validation & Error Handling**: Robust validation with clear error messages
- **Schedule Management**: Create, retrieve, and delete schedules with ease

Use Cases
=========

Fabric Scheduler addresses several common challenges in Microsoft Fabric environments:

- **Efficiency in Multi-Workspace Environments**: Manually scheduling artifacts across multiple workspaces is time-consuming. Fabric Scheduler automates this process.

- **Support for Git Integration**: As engineering teams emphasize Git integration and deployment pipelines, Fabric Scheduler ensures schedules can be version-controlled and deployed alongside artifacts.

- **Schedule Preservation**: When deploying artifacts to different workspaces, Fabric's native tools don't carry forward schedules. Fabric Scheduler solves this by allowing you to programmatically define and apply schedules.

- **Multiple Schedule Support**: Fabric's UI doesn't support creating multiple schedules for the same artifact. Fabric Scheduler enables more complex scheduling patterns.

- **Standardization Across Teams**: Implement consistent scheduling practices across engineering teams with a code-based approach.

Installation
============

.. code-block:: bash

    pip install fabric_scheduler

Getting Started
===============

Basic Usage
-----------

.. code-block:: python

    from fabric_scheduler import ArtifactScheduler

    # Initialize scheduler
    scheduler = ArtifactScheduler()
    # OR ArtifactScheduler(workspace_id="your-workspace-id")

    # Set artifacts to schedule from list of dictionaries
    artifacts = [
        {
            "displayName": "DailyAnalytics",
            "schedule": {
                "enabled": True,
                "config": {
                    "type": "Daily",
                    "times": ["08:00", "17:00"]
                }
            }
        },
        {
            "displayName": "WeeklyReport",
            "schedule": {
                "enabled": True,
                "config": {
                    "type": "Weekly",
                    "weekdays": ["Monday", "Wednesday"],
                    "times": ["10:00"]
                }
            }
        },
    ]
    scheduler.set_artifacts(artifacts)

    # Create schedules
    scheduler.create_schedules()

Input Methods
=============

Dictionary Input
----------------

Define a list of dictionaries with familiar notation like JSON, and pass it to the ``set_artifacts`` method.

.. code-block:: python

    scheduler.set_artifacts([
        {
            "displayName": "MyNotebook",
            "type": "Notebook",
            "schedule": {
                "enabled": True,
                "config": {
                    "type": "Cron",
                    "interval": 240,
                    "localTimeZone": "India Standard Time",
                }
            }
        },
    ])

CSV File Input
--------------

Upload the CSV file and pass the file name to the ``load_artifacts_from_csv`` method.

.. code-block:: python

    scheduler.load_artifacts_from_csv("artifact_schedule.csv")

Example CSV structure:

.. code-block::

    displayName,type,enabled,schedule type,localTimeZone,startDate,startTime,endDate,endTime,interval,times,weekdays
    SalesReportNotebook,Notebook,true,Cron,,3/30/2025,2:00,,,240,,
    DataPipelineETL,Pipeline,true,Daily,,,,,,,"08:00,17:00",
    WeeklyAnalyticsDataflow,Dataflow,true,Weekly,,,,,,,"08:00","Monday,Wednesday"

CSV String Input
----------------

Pass a CSV string directly to the ``load_artifacts_from_csv`` method.

.. code-block:: python

    csv_content = '''
    displayName,type,enabled,schedule type,localTimeZone,startDate,startTime,endDate,endTime,interval,times,weekdays
    SalesReportNotebook,Notebook,true,Cron,,3/30/2025,2:00,,,240,,
    DataPipelineETL,Pipeline,true,Daily,,,,,,,"08:00,17:00",
    WeeklyAnalyticsDataflow,Dataflow,true,Weekly,,,,,,,"08:00","Monday,Wednesday"
    '''
    scheduler.load_artifacts_from_csv(csv_content)

Advanced Usage
==============

For more detailed examples and advanced usage scenarios, please refer to the `detailed guide <https://fabric-scheduler.readthedocs.io/en/stable/detailed_guide.html>`_ section of our documentation.

API Reference
=============

For comprehensive API documentation, please visit the `API reference <https://fabric-scheduler.readthedocs.io/en/stable/api/modules.html>`_ section of our documentation.

Contributing
============

Contributions are welcome! Please see our `contributing guide <https://fabric-scheduler.readthedocs.io/en/stable/contributing.html>`_ for details on how to get started.

License
=======

This project is licensed under the MIT License - see the `license file <https://fabric-scheduler.readthedocs.io/en/stable/license.html>`_ for details.
