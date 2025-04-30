===================
Detailed Guide
===================


This document provides examples for using the ``fabric_scheduler`` module to schedule Fabric artifacts like notebooks, dataflows, and pipelines.

Working with ArtifactScheduler
------------------------------

1. Creating an Instance
~~~~~~~~~~~~~~~~~~~~~~~

Create an instance of the ArtifactScheduler class:

.. code-block:: python

    # Default: silent mode (minimal output)
    scheduler = ArtifactScheduler()

    # With verbose output
    scheduler_verbose = ArtifactScheduler(silent=False)

    # With a specific workspace ID
    scheduler = ArtifactScheduler(workspace_id="your_workspace_id")

When you create an instance with ``silent=False``, it will display information about the workspace:

.. code-block:: text

    Workspace: [Workspace Name] ([Workspace ID])
    Items found in workspace: [Count]
    [Table showing workspace items]

2. Setting Artifacts for Scheduling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You have multiple ways to specify which artifacts to schedule:

Option 1: Using dictionaries
++++++++++++++++++++++++++++

.. code-block:: python

    artifacts = [
        {
            "displayName": "artifact1",
            # Type is optional, only needed when multiple artifacts have the same name
            "schedule": {
                "enabled": True,  # Optional: enabled status
                "config": {
                    "type": "Cron",  # Schedule type: "Cron", "Daily", or "Weekly"
                    "interval": 240,  # Minutes between runs for Cron schedules
                    "localTimeZone": "Greenwich Standard Time",  # Optional: timezone
                    "startDate": "4/30/2025",  # Optional: date format MM/DD/YYYY
                    "startTime": "02:00",  # Optional: time format HH:MM
                    "endDate": "4/30/2026",  # Optional: end date
                    "endTime": "23:59"  # Optional: end time
                }
            }
        },
        {
            "displayName": "artifact2",
            "type": "DataPipeline",
            "schedule": {
                "enabled": True,
                "config": {
                    "type": "Weekly",
                    "weekdays": ["Monday", "Wednesday", "Friday"],
                    "times": ["09:00"]
                }
            }
        }
    ]

    scheduler.set_artifacts(artifacts)

Option 2: Using CSV string
+++++++++++++++++++++++++++++

.. code-block:: python

    artifacts_csv = """
    displayName,type,enabled,schedule type,localTimeZone,startDate,startTime,endDate,endTime,interval,times,weekdays
    artifact1,,,Cron,,4/30/2025,2:00,,,240,,
    artifact2,,,Daily,,,,,,,"01:30,07:30,13:30,19:30",
    """

    scheduler.load_artifacts_from_csv(artifacts_csv)

Option 3: Using StringIO
++++++++++++++++++++++++

.. code-block:: python

    import io

    csv_file = io.StringIO("""
    displayName,type,enabled,schedule type,localTimeZone,startDate,startTime,endDate,endTime,interval,times,weekdays
    artifact1,,,Cron,,4/30/2025,2:00,,,240,,
    artifact2,,,Daily,,,,,,,"01:30,07:30,13:30,19:30",
    """)

    scheduler.load_artifacts_from_csv(csv_file)

Option 4: Using CSV file
+++++++++++++++++++++++++

.. code-block:: python

    scheduler.load_artifacts_from_csv("artifacts_to_be_scheduled.csv")

After setting artifacts, you can see what's going to be scheduled:

.. code-block:: text

    Artifacts to be scheduled:
    [Table showing artifacts and their schedule configurations]

3. Creating Schedules
~~~~~~~~~~~~~~~~~~~~~

Once you've specified the artifacts to schedule, create their schedules:

.. code-block:: python

    scheduler.create_schedules()

Output example:

.. code-block:: text

    Creating schedules for 2 artifact(s)...
    Successfully created 2 schedule(s)
    Schedules:
    [Table showing created schedules]

4. Displaying Schedules
~~~~~~~~~~~~~~~~~~~~~~~

View schedules for your artifacts:

.. code-block:: python

    # View schedules only for selected artifacts
    scheduler.display_schedules()

    # View schedules for all artifacts in the workspace
    scheduler.display_schedules(scope="all")

Output example:

.. code-block:: text

    Schedules:
    [Table showing schedule details]

5. Deleting Schedules
~~~~~~~~~~~~~~~~~~~~~

Remove schedules when they're no longer needed:

.. code-block:: python

    # Delete schedules only for selected artifacts
    scheduler.delete_schedules()

    # Delete all schedules in the workspace
    scheduler.delete_schedules(scope="all")

Output example:

.. code-block:: text

    Deleting 2 schedule(s)...
    All schedules deleted successfully

Complete Example
----------------

Here's a complete workflow example:

.. code-block:: python

    from fabric_scheduler import ArtifactScheduler

    # Create a scheduler (with verbose output)
    scheduler = ArtifactScheduler(silent=False)

    # Load artifacts to schedule from a CSV file
    scheduler.load_artifacts_from_csv("artifacts_to_schedule.csv")

    # If needed, delete the previous schedules
    # scheduler.delete_schedules()

    # Create schedules for the loaded artifacts
    scheduler.create_schedules()

    # Display the created schedules
    scheduler.display_schedules()

Schedule Configuration Options
------------------------------

When scheduling artifacts, you can specify various configuration options. The system supports three types of schedules: **Cron**, **Daily**, and **Weekly**.

Common Configuration Options (All Schedule Types):

- **displayName**: Name of the artifact (required)
- **type**: Type of artifact - "Notebook", "Dataflow", or "DataPipeline" (optional, only required when multiple artifacts have the same name)
- **schedule**: A dictionary containing schedule configuration:

  - **enabled**: Whether the schedule is enabled (optional, defaults to True)
  - **config**: A dictionary with the following properties:

    - **type**: Type of schedule - "Cron", "Daily", or "Weekly" (required)
    - **localTimeZone**: Timezone for the schedule (optional, defaults to "Greenwich Standard Time")
    - **startDate**: Start date in MM/DD/YYYY format (optional)
    - **startTime**: Start time in HH:MM format (optional, defaults to "00:00")
    - **endDate**: End date in MM/DD/YYYY format (optional)
    - **endTime**: End time in HH:MM format (optional, defaults to "23:59")
    - **interval**: Minutes between runs for Cron schedules (required for Cron)
    - **times**: Specific times for the schedule (required for Daily and Weekly)
    - **weekdays**: Specific weekdays for the schedule (required for Weekly)

Specific Configuration by Schedule Type:

1. Cron Schedule:
   - **interval**: Minutes between runs (required, must be between 1 and 5270400)

2. Daily Schedule:
   - **times**: List of specific times in HH:MM format when the artifact should run (required)

3. Weekly Schedule:
   - **weekdays**: List of days when the artifact should run (required, must be from: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
   - **times**: List of specific times in HH:MM format when the artifact should run on the specified days (required)

Example Schedule Configurations:

.. code-block:: python

    # Cron schedule - run every 4 hours
    {
        "displayName": "daily_report",
        "type": "Notebook",
        "schedule": {
            "enabled": True,
            "config": {
                "type": "Cron",
                "interval": 240,  # minutes (4 hours)
                "startDate": "4/30/2025",
                "startTime": "08:00",
                "localTimeZone": "Greenwich Standard Time"
            }
        }
    }

    # Daily schedule - run at specific times each day
    {
        "displayName": "hourly_metrics",
        "type": "Dataflow",
        "schedule": {
            "enabled": True,
            "config": {
                "type": "Daily",
                "times": ["08:00", "12:00", "16:00", "20:00"],
                "localTimeZone": "Pacific Standard Time"
            }
        }
    }

    # Weekly schedule - run on Monday and Friday at 9am
    {
        "displayName": "weekly_report",
        "type": "DataPipeline",
        "schedule": {
            "enabled": True,
            "config": {
                "type": "Weekly",
                "weekdays": ["Monday", "Friday"],
                "times": ["09:00"]
            }
        }
    }

.. note::
    For detailed explanations of schedule types, refer to the `Create Item Schedule API documentation <https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/create-item-schedule?tabs=HTTP>`_.
    For a list of valid timezones, see the `Default Time Zones documentation <https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/default-time-zones?view=windows-11>`_.

Best Practices
--------------

1. Consider timezone implications when scheduling artifacts, especially for global teams.
2. Remove unused schedules to keep your workspace clean and prevent unnecessary executions.
3. Delete old schedules before creating new ones, if applicable.
