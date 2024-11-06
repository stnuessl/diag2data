=========
diag2data
=========

.. image:: https://github.com/stnuessl/diag2data/actions/workflows/build.yaml/badge.svg
   :alt: Build
   :target: https://github.com/stnuessl/diag2data/actions

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :alt: License: MIT
   :target: https://opensource.org/licenses/MIT

Transform C compiler diagnostics to easy to process data formats and vice versa.

.. contents::


Motivation
==========

In some projects it is common to automatically process diagnostic messages
emitted by invoked tools. However, usually these messages are in a plain text
format and a transformation into a more useful data format needs to be performed
beforehand. This python package aims to minimize the effort that needs to be
spent for achieving the transformation.


Limitations
===========

Transforming diagnostics between different compiler output formats might lead
to surprising results as their structures are not trivially mappable to each
other.

Output
======

JSON
----

.. code-block:: json

    [
        {
            "Path": "src/file-util.c"
            "Line": "136",
            "Column": "15",
            "Severity": "warning",
            "Message": "'readdir_r' is deprecated",
            "Diagnostic": "-Wdeprecated-declarations"
        },
        {
            "Path": "/usr/include/dirent.h",
            "Line": "188",
            "Column": "28",
            "Severity": "note",
            "Message": "'readdir_r' has been explicitly marked deprecated here",
            "Diagnostic": ""
        },
        {
            "Path": "/usr/include/sys/cdefs.h",
            "Line": "510",
            "Column": "51",
            "Severity": "note",
            "Message": "expanded from macro '__attribute_deprecated__'",
            "Diagnostic": ""
        }
    ]

CSV
---

.. code-block:: csv

    "Path","Line","Column","Severity","Message","Diagnostic"
    "src/file-util.c","136","15","warning","'readdir_r' is deprecated","-Wdeprecated-declarations"
    "/usr/include/dirent.h","188","28","note","'readdir_r' has been explicitly marked deprecated here",""
    "/usr/include/sys/cdefs.h","510","51","note","expanded from macro '__attribute_deprecated__'",""


Examples
========


.. code-block:: sh

    gcc -c file.c 2>&1 diags.txt
    python -m diag2data -o diags.json --input-kind gcc diags.txt

Via standard input:

.. code-block:: sh

   gcc -c file.c 2>&1 | python -m diag2data -o diags.csv --input-kind gcc


.. code-block:: sh

   make 2>&1 | python -m diag2data -o diags.csv --input-kind gcc

