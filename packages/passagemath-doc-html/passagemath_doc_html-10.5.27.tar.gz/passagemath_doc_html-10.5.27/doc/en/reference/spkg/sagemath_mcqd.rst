.. _spkg_sagemath_mcqd:

=====================================================================================
sagemath_mcqd: Finding maximum cliques with mcqd
=====================================================================================

About SageMath
--------------

   "Creating a Viable Open Source Alternative to
    Magma, Maple, Mathematica, and MATLAB"

   Copyright (C) 2005-2024 The Sage Development Team

   https://www.sagemath.org

SageMath fully supports all major Linux distributions, recent versions of
macOS, and Windows (Windows Subsystem for Linux).

See https://doc.sagemath.org/html/en/installation/index.html
for general installation instructions.


About this pip-installable source distribution
----------------------------------------------

This pip-installable source distribution ``sagemath-mcqd`` is a small
optional distribution for use with ``sagemath-standard``.

It provides a Cython interface to the ``mcqd`` library,
providing a fast exact algorithm for finding a maximum clique in
an undirected graph.

Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_cysignals`
- :ref:`spkg_cython`
- :ref:`spkg_mcqd`
- :ref:`spkg_memory_allocator`
- :ref:`spkg_pkgconfig`
- :ref:`spkg_sage_setup`

Version Information
-------------------

package-version.txt::

    10.5.27

version_requirements.txt::

    passagemath-mcqd ~= 10.5.27.0


Equivalent System Packages
--------------------------

(none known)

