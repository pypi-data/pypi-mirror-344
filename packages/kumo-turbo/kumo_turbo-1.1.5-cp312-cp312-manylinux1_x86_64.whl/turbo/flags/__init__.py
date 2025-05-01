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
"""This package is used to define and parse command line flags.

This package defines a *distributed* flag-definition policy: rather than
an application having to define all flags in or near main(), each Python
module defines flags that are useful to it.  When one Python module
imports another, it gains access to the other's flags.  (This is
implemented by having all modules share a common, global registry object
containing all the flag information.)

Flags are defined through the use of one of the DEFINE_xxx functions.
The specific function used determines how the flag is parsed, checked,
and optionally type-converted, when it's seen on the command line.
"""

import sys

from turbo.flags import _argument_parser
from turbo.flags import _defines
from turbo.flags import _exceptions
from turbo.flags import _flag
from turbo.flags import _flagvalues
from turbo.flags import _helpers
from turbo.flags import _validators

__all__ = (
    'DEFINE',
    'DEFINE_flag',
    'DEFINE_string',
    'DEFINE_boolean',
    'DEFINE_bool',
    'DEFINE_float',
    'DEFINE_integer',
    'DEFINE_enum',
    'DEFINE_enum_class',
    'DEFINE_list',
    'DEFINE_spaceseplist',
    'DEFINE_multi',
    'DEFINE_multi_string',
    'DEFINE_multi_integer',
    'DEFINE_multi_float',
    'DEFINE_multi_enum',
    'DEFINE_multi_enum_class',
    'DEFINE_alias',
    # Flag validators.
    'register_validator',
    'validator',
    'register_multi_flags_validator',
    'multi_flags_validator',
    'mark_flag_as_required',
    'mark_flags_as_required',
    'mark_flags_as_mutual_exclusive',
    'mark_bool_flags_as_mutual_exclusive',
    # Flag modifiers.
    'set_default',
    'override_value',
    # Key flag related functions.
    'declare_key_flag',
    'adopt_module_key_flags',
    'disclaim_key_flags',
    # Module exceptions.
    'Error',
    'CantOpenFlagFileError',
    'DuplicateFlagError',
    'IllegalFlagValueError',
    'UnrecognizedFlagError',
    'UnparsedFlagAccessError',
    'ValidationError',
    'FlagNameConflictsWithMethodError',
    # Public classes.
    'Flag',
    'BooleanFlag',
    'EnumFlag',
    'EnumClassFlag',
    'MultiFlag',
    'MultiEnumClassFlag',
    'FlagHolder',
    'FlagValues',
    'ArgumentParser',
    'BooleanParser',
    'EnumParser',
    'EnumClassParser',
    'ArgumentSerializer',
    'FloatParser',
    'IntegerParser',
    'BaseListParser',
    'ListParser',
    'ListSerializer',
    'EnumClassListSerializer',
    'CsvListSerializer',
    'WhitespaceSeparatedListParser',
    'EnumClassSerializer',
    # Helper functions.
    'get_help_width',
    'text_wrap',
    'flag_dict_to_args',
    'doc_to_help',
    # The global FlagValues instance.
    'FLAGS',
)

# Initialize the FLAGS_MODULE as early as possible.
# It's only used by adopt_module_key_flags to take SPECIAL_FLAGS into account.
_helpers.FLAGS_MODULE = sys.modules[__name__]

# Add current module to disclaimed module ids.
_helpers.disclaim_module_ids.add(id(sys.modules[__name__]))

# DEFINE functions. They are explained in more details in the module doc string.
# pylint: disable=invalid-name
DEFINE = _defines.DEFINE
DEFINE_flag = _defines.DEFINE_flag
DEFINE_string = _defines.DEFINE_string
DEFINE_boolean = _defines.DEFINE_boolean
DEFINE_bool = DEFINE_boolean  # Match C++ API.
DEFINE_float = _defines.DEFINE_float
DEFINE_integer = _defines.DEFINE_integer
DEFINE_enum = _defines.DEFINE_enum
DEFINE_enum_class = _defines.DEFINE_enum_class
DEFINE_list = _defines.DEFINE_list
DEFINE_spaceseplist = _defines.DEFINE_spaceseplist
DEFINE_multi = _defines.DEFINE_multi
DEFINE_multi_string = _defines.DEFINE_multi_string
DEFINE_multi_integer = _defines.DEFINE_multi_integer
DEFINE_multi_float = _defines.DEFINE_multi_float
DEFINE_multi_enum = _defines.DEFINE_multi_enum
DEFINE_multi_enum_class = _defines.DEFINE_multi_enum_class
DEFINE_alias = _defines.DEFINE_alias
# pylint: enable=invalid-name

# Flag validators.
register_validator = _validators.register_validator
validator = _validators.validator
register_multi_flags_validator = _validators.register_multi_flags_validator
multi_flags_validator = _validators.multi_flags_validator
mark_flag_as_required = _validators.mark_flag_as_required
mark_flags_as_required = _validators.mark_flags_as_required
mark_flags_as_mutual_exclusive = _validators.mark_flags_as_mutual_exclusive
mark_bool_flags_as_mutual_exclusive = _validators.mark_bool_flags_as_mutual_exclusive

# Flag modifiers.
set_default = _defines.set_default
override_value = _defines.override_value

# Key flag related functions.
declare_key_flag = _defines.declare_key_flag
adopt_module_key_flags = _defines.adopt_module_key_flags
disclaim_key_flags = _defines.disclaim_key_flags

# Module exceptions.
# pylint: disable=invalid-name
Error = _exceptions.Error
CantOpenFlagFileError = _exceptions.CantOpenFlagFileError
DuplicateFlagError = _exceptions.DuplicateFlagError
IllegalFlagValueError = _exceptions.IllegalFlagValueError
UnrecognizedFlagError = _exceptions.UnrecognizedFlagError
UnparsedFlagAccessError = _exceptions.UnparsedFlagAccessError
ValidationError = _exceptions.ValidationError
FlagNameConflictsWithMethodError = _exceptions.FlagNameConflictsWithMethodError

# Public classes.
Flag = _flag.Flag
BooleanFlag = _flag.BooleanFlag
EnumFlag = _flag.EnumFlag
EnumClassFlag = _flag.EnumClassFlag
MultiFlag = _flag.MultiFlag
MultiEnumClassFlag = _flag.MultiEnumClassFlag
FlagHolder = _flagvalues.FlagHolder
FlagValues = _flagvalues.FlagValues
ArgumentParser = _argument_parser.ArgumentParser
BooleanParser = _argument_parser.BooleanParser
EnumParser = _argument_parser.EnumParser
EnumClassParser = _argument_parser.EnumClassParser
ArgumentSerializer = _argument_parser.ArgumentSerializer
FloatParser = _argument_parser.FloatParser
IntegerParser = _argument_parser.IntegerParser
BaseListParser = _argument_parser.BaseListParser
ListParser = _argument_parser.ListParser
ListSerializer = _argument_parser.ListSerializer
EnumClassListSerializer = _argument_parser.EnumClassListSerializer
CsvListSerializer = _argument_parser.CsvListSerializer
WhitespaceSeparatedListParser = _argument_parser.WhitespaceSeparatedListParser
EnumClassSerializer = _argument_parser.EnumClassSerializer
# pylint: enable=invalid-name

# Helper functions.
get_help_width = _helpers.get_help_width
text_wrap = _helpers.text_wrap
flag_dict_to_args = _helpers.flag_dict_to_args
doc_to_help = _helpers.doc_to_help

# Special flags.
_helpers.SPECIAL_FLAGS = FlagValues()

DEFINE_string(
    'flagfile', '',
    'Insert flag definitions from the given file into the command line.',
    _helpers.SPECIAL_FLAGS)  # pytype: disable=wrong-arg-types

DEFINE_string('undefok', '',
              'comma-separated list of flag names that it is okay to specify '
              'on the command line even if the program does not define a flag '
              'with that name.  IMPORTANT: flags in this list that have '
              'arguments MUST use the --flag=value format.',
              _helpers.SPECIAL_FLAGS)  # pytype: disable=wrong-arg-types

#: The global FlagValues instance.
FLAGS = _flagvalues.FLAGS
