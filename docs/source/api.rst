API
===

.. py:module:: terrarium

This section details the classes and functions made available by Terrarium.


Resources
---------

.. autoclass:: App
   :members:

.. autoclass:: Environment
   :members:

.. autoclass:: RuntimeProfile
   :members:

Resource Managers
-----------------

.. autoclass:: AppManager
   :members:

.. autoclass:: EnvironmentManager
   :members:

.. autoclass:: RuntimeProfileManager
   :members:

Utilities
---------

.. autofunction:: apply_environment

.. autofunction:: build_cmd

.. autofunction:: execute

.. autofunction:: generate_bat

IO - JSON
---------

.. py:module:: terrarium._resource_io.json_io

.. autofunction:: import_app

.. autofunction:: export_app

.. autofunction:: import_environment

.. autofunction:: export_environment

.. autofunction:: import_runtime_profile

.. autofunction:: export_runtime_profile
