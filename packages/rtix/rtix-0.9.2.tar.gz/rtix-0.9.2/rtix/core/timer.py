# Copyright (c) 2025 Velodex Robotics, Inc and RTIX Developers.
# Licensed under Apache-2.0. http://www.apache.org/licenses/LICENSE-2.0

import time


def getTimestampNs():
    """Returns the current time since epoch (ns)"""
    return time.time_ns()


def nsToMs(time_ns: int) -> int:
    """Convert nanoseconds to milliseconds"""
    return int(time_ns * 1e-6)


class Timer:
    """
    A timer to keep track of elapsed time and sleep the thread.

    NOTE: Unlike the C++ version, the Python timer does not provide an option
    to spinlock the thread because Python processes should not be expected to
    perform with this level of precision.  If such precision is needed, use C++
    """
    MS_PER_S = 1e3
    US_PER_S = 1e6
    NS_PER_S = 1e9

    def __init__(self):
        self.start()

    def start(self):
        self._tic = time.time()

    def getElapsedS(self) -> float:
        toc = time.time()
        return toc - self._tic

    @staticmethod
    def Sleep(duration_s: float):
        time.sleep(duration_s)
