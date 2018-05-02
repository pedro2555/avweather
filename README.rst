Aviation Weather Tools
======================

Provides METAR and SPECI parser as specified in the Annex 3 to the Convetion on Internation Civil Aviation as published by ICAO.

Install
=======

.. code-block::
pip install avweather

Usage
=====

METAR Parser
------------

All metar information is parsed to python primitive data types with no transformations. For convenience all values are exposed via namedtuples.

>>> from avweather import metar
>>> result = metar.parse('METAR LPPT 020000Z 24003KT 9999 FEW015 10/07 Q1018')
>>> result.report.pressure
1018
>>> result.location
'LPPT'
>>> result.report.sky.clouds
(Cloud(amount='FEW', height=15, type=None),)

Changelog
=========

0.0.6

- Added support for unavailable and variable wind reports
- Added support for unavailable wind speed reports

0.0.5

- Added METAR parsing module based on ICAO Annex 3 documentation
