User Guide
==========

As Terrarium is still under heavy development, it's not practical to devote
energy to writing a detailed user guide.

What follows is at best a quickstart for understanding the basics.


The Basics
----------

Terrarium handles three types of data (or `Resources`):
  - :class:`~terrarium.Environment`
  - :class:`~terrarium.App`
  - :class:`~terrarium.RuntimeProfile`

Environments
````````````

An :class:`~terrarium.Environment` represents environment variable data.
Environments can be hierarchical, enabling sharing of environment data through
inheritance. They can also expand and contract strings containing environment
variables.

Apps
````

An :class:`~terrarium.App` represents an executable application.

Runtime Profiles
````````````````

A :class:`~terrarium.RuntimeProfile` represents a complete runtime solution
that combines an :class:`~terrarium.App`, :class:`~terrarium.Environment`, and
argumentation.


Meet the Management
-------------------

While it is possible to use the `Resource` classes directly, Terrarium provides
a suite of `Managers` to help manage `Resource` instances.

.. note::

    Currently, Managers are static classes and should not be instantiated.
    All methods related to Managers are class methods.

Terrarium has a manager for each of the three core `Resource` types:
  - :class:`~terrarium.EnvironmentManager`
  - :class:`~terrarium.AppManager`
  - :class:`~terrarium.RuntimeProfileManager`

Managers support the following operations on their respective `Resource` type:
  - Create
  - Get
  - Update
  - Delete
  - Find

See the :doc:`api` documentation for specific call signature information.