# Copyright (C) 2025 Kumo inc.
# Author: Jeff.li lijippy@163.com
# All rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https:#www.gnu.org/licenses/>.
#

"""Module to convert log levels between Abseil Python, C++, and Python standard.

This converter has to convert (best effort) between three different
logging level schemes:

  * **cpp**: The C++ logging level scheme used in Abseil C++.
  * **turbo**: The turbo.logging level scheme used in Abseil Python.
  * **standard**: The python standard library logging level scheme.

Here is a handy ascii chart for easy mental mapping::

    LEVEL    | cpp |  turbo  | standard |
    ---------+-----+--------+----------+
    DEBUG    |  0  |    1   |    10    |
    INFO     |  0  |    0   |    20    |
    WARNING  |  1  |   -1   |    30    |
    ERROR    |  2  |   -2   |    40    |
    CRITICAL |  3  |   -3   |    50    |
    FATAL    |  3  |   -3   |    50    |

Note: standard logging ``CRITICAL`` is mapped to turbo/cpp ``FATAL``.
However, only ``CRITICAL`` logs from the turbo logger (or turbo.logging.fatal)
will terminate the program. ``CRITICAL`` logs from non-turbo loggers are treated
as error logs with a message prefix ``"CRITICAL - "``.

Converting from standard to turbo or cpp is a lossy conversion.
Converting back to standard will lose granularity.  For this reason,
users should always try to convert to standard, the richest
representation, before manipulating the levels, and then only to cpp
or turbo if those level schemes are absolutely necessary.
"""

import logging

STANDARD_CRITICAL = logging.CRITICAL
STANDARD_ERROR = logging.ERROR
STANDARD_WARNING = logging.WARNING
STANDARD_INFO = logging.INFO
STANDARD_DEBUG = logging.DEBUG

# These levels are also used to define the constants
# FATAL, ERROR, WARNING, INFO, and DEBUG in the
# turbo.logging module.
TURBO_FATAL = -3
TURBO_ERROR = -2
TURBO_WARNING = -1
TURBO_WARN = -1  # Deprecated name.
TURBO_INFO = 0
TURBO_DEBUG = 1

TURBO_LEVELS = {TURBO_FATAL: 'FATAL',
               TURBO_ERROR: 'ERROR',
               TURBO_WARNING: 'WARNING',
               TURBO_INFO: 'INFO',
               TURBO_DEBUG: 'DEBUG'}

# Inverts the TURBO_LEVELS dictionary
TURBO_NAMES = {'FATAL': TURBO_FATAL,
              'ERROR': TURBO_ERROR,
              'WARNING': TURBO_WARNING,
              'WARN': TURBO_WARNING,  # Deprecated name.
              'INFO': TURBO_INFO,
              'DEBUG': TURBO_DEBUG}

TURBO_TO_STANDARD = {TURBO_FATAL: STANDARD_CRITICAL,
                    TURBO_ERROR: STANDARD_ERROR,
                    TURBO_WARNING: STANDARD_WARNING,
                    TURBO_INFO: STANDARD_INFO,
                    TURBO_DEBUG: STANDARD_DEBUG}

# Inverts the TURBO_TO_STANDARD
STANDARD_TO_TURBO = {v: k for (k, v) in TURBO_TO_STANDARD.items()}


def get_initial_for_level(level):
  """Gets the initial that should start the log line for the given level.

  It returns:

  * ``'I'`` when: ``level < STANDARD_WARNING``.
  * ``'W'`` when: ``STANDARD_WARNING <= level < STANDARD_ERROR``.
  * ``'E'`` when: ``STANDARD_ERROR <= level < STANDARD_CRITICAL``.
  * ``'F'`` when: ``level >= STANDARD_CRITICAL``.

  Args:
    level: int, a Python standard logging level.

  Returns:
    The first initial as it would be logged by the C++ logging module.
  """
  if level < STANDARD_WARNING:
    return 'I'
  elif level < STANDARD_ERROR:
    return 'W'
  elif level < STANDARD_CRITICAL:
    return 'E'
  else:
    return 'F'


def turbo_to_cpp(level):
  """Converts an turbo log level to a cpp log level.

  Args:
    level: int, an turbo.logging level.

  Raises:
    TypeError: Raised when level is not an integer.

  Returns:
    The corresponding integer level for use in Abseil C++.
  """
  if not isinstance(level, int):
    raise TypeError(f'Expect an int level, found {type(level)}')
  if level >= 0:
    # C++ log levels must be >= 0
    return 0
  else:
    return -level


def turbo_to_standard(level):
  """Converts an integer level from the turbo value to the standard value.

  Args:
    level: int, an turbo.logging level.

  Raises:
    TypeError: Raised when level is not an integer.

  Returns:
    The corresponding integer level for use in standard logging.
  """
  if not isinstance(level, int):
    raise TypeError(f'Expect an int level, found {type(level)}')
  if level < TURBO_FATAL:
    level = TURBO_FATAL
  if level <= TURBO_DEBUG:
    return TURBO_TO_STANDARD[level]
  # Maps to vlog levels.
  return STANDARD_DEBUG - level + 1


def string_to_standard(level):
  """Converts a string level to standard logging level value.

  Args:
    level: str, case-insensitive ``'debug'``, ``'info'``, ``'warning'``,
        ``'error'``, ``'fatal'``.

  Returns:
    The corresponding integer level for use in standard logging.
  """
  return turbo_to_standard(TURBO_NAMES.get(level.upper()))


def standard_to_turbo(level):
  """Converts an integer level from the standard value to the turbo value.

  Args:
    level: int, a Python standard logging level.

  Raises:
    TypeError: Raised when level is not an integer.

  Returns:
    The corresponding integer level for use in turbo logging.
  """
  if not isinstance(level, int):
    raise TypeError(f'Expect an int level, found {type(level)}')
  if level < 0:
    level = 0
  if level < STANDARD_DEBUG:
    # Maps to vlog levels.
    return STANDARD_DEBUG - level + 1
  elif level < STANDARD_INFO:
    return TURBO_DEBUG
  elif level < STANDARD_WARNING:
    return TURBO_INFO
  elif level < STANDARD_ERROR:
    return TURBO_WARNING
  elif level < STANDARD_CRITICAL:
    return TURBO_ERROR
  else:
    return TURBO_FATAL


def standard_to_cpp(level):
  """Converts an integer level from the standard value to the cpp value.

  Args:
    level: int, a Python standard logging level.

  Raises:
    TypeError: Raised when level is not an integer.

  Returns:
    The corresponding integer level for use in cpp logging.
  """
  return turbo_to_cpp(standard_to_turbo(level))
