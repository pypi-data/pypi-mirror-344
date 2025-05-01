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
# distutils: language = c++
from libcpp cimport bool
from libcpp.string cimport string as c_string
from enum import Enum

cdef extern from "turbo/utility/status.h" namespace "turbo":
    cpdef enum class CStatusCode "turbo::StatusCode"(int):
        kOk = 0,
        kCancelled = 1,
        kUnknown = 2,
        kInvalidArgument = 3,
        kDeadlineExceeded = 4,
        kNotFound = 5,
        kAlreadyExists = 6,
        kPermissionDenied = 7,
        kResourceExhausted = 8,
        kFailedPrecondition = 9,
        kAborted = 10,
        kOutOfRange = 11,
        kUnimplemented = 12,
        kInternal = 13,
        kUnavailable = 14,
        kDataLoss = 15,
        kUnauthenticated = 16,
        kIOError = 17

'''
cpdef public enum StatusCode:
    Ok = <int>CStatusCode.kOk,
    Cancelled = <int>CStatusCode.kCancelled,
    Unknown = <int>CStatusCode.kUnknown,
    InvalidArgument = <int>CStatusCode.kInvalidArgument,
    DeadlineExceeded = <int>CStatusCode.kDeadlineExceeded,
    NotFound = <int>CStatusCode.kNotFound,
    AlreadyExists = <int>CStatusCode.kAlreadyExists,
    PermissionDenied = <int>CStatusCode.kPermissionDenied,
    ResourceExhausted = <int>CStatusCode.kResourceExhausted,
    FailedPrecondition = <int>CStatusCode.kFailedPrecondition,
    Aborted = <int>CStatusCode.kAborted,
    OutOfRange = <int>CStatusCode.kOutOfRange,
    Unimplemented = <int>CStatusCode.kUnimplemented,
    Internal = <int>CStatusCode.kInternal,
    Unavailable = <int>CStatusCode.kUnavailable,
    DataLoss = <int>CStatusCode.kDataLoss,
    Unauthenticated = <int>CStatusCode.kUnauthenticated,
    IOError = <int>CStatusCode.kIOError
'''

cdef extern from "turbo/utility/status.h" namespace "turbo":
    cdef cppclass CStatus "turbo::Status":

        bool ok() const

        int code() const

        c_string message() const

        const c_string &to_string() const

cdef extern from "turbo/utility/status.h" namespace "turbo":
    cdef cppclass CResult "turbo::Status"[T]:

        bool ok() const
        CStatus status()