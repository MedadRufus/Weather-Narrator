###############################################
#
# Created: 04/08/2020
# Author: Medad Newman
#
# Taken from octoprint
# https://github.com/OctoPrint/OctoPrint/blob/master/src/octoprint/util/__init__.py
################################################
import threading
from threading import Timer


class RepeatedTimer(threading.Thread):
    """
    This class represents an action that should be run repeatedly in an interval. It is similar to python's
    own :class:`threading.Timer` class, but instead of only running once the ``function`` will be run again and again,
    sleeping the stated ``interval`` in between.
    RepeatedTimers are started, as with threads, by calling their ``start()`` method. The timer can be stopped (in
    between runs) by calling the :func:`cancel` method. The interval the time waited before execution of a loop may
    not be exactly the same as the interval specified by the user.
    For example:
    .. code-block:: python
       def hello():
           print("Hello World!")
       t = RepeatedTimer(1.0, hello)
       t.start() # prints "Hello World!" every second
    Another example with dynamic interval and loop condition:
    .. code-block:: python
       count = 0
       maximum = 5
       factor = 1
       def interval():
           global count
           global factor
           return count * factor
       def condition():
           global count
           global maximum
           return count <= maximum
       def hello():
           print("Hello World!")
           global count
           count += 1
       t = RepeatedTimer(interval, hello, run_first=True, condition=condition)
       t.start() # prints "Hello World!" 5 times, printing the first one
                 # directly, then waiting 1, 2, 3, 4s in between (adaptive interval)
    Arguments:
        interval (float or callable): The interval between each ``function`` call, in seconds. Can also be a callable
            returning the interval to use, in case the interval is not static.
        function (callable): The function to call.
        args (list or tuple): The arguments for the ``function`` call. Defaults to an empty list.
        kwargs (dict): The keyword arguments for the ``function`` call. Defaults to an empty dict.
        run_first (boolean): If set to True, the function will be run for the first time *before* the first wait period.
            If set to False (the default), the function will be run for the first time *after* the first wait period.
        condition (callable): Condition that needs to be True for loop to continue. Defaults to ``lambda: True``.
        on_condition_false (callable): Callback to call when the timer finishes due to condition becoming false. Will
            be called before the ``on_finish`` callback.
        on_cancelled (callable): Callback to call when the timer finishes due to being cancelled. Will be called
            before the ``on_finish`` callback.
        on_finish (callable): Callback to call when the timer finishes, either due to being cancelled or since
            the condition became false.
        daemon (bool): daemon flag to set on underlying thread.
    """

    def __init__(self, interval, function, args=None, kwargs=None,
                 run_first=False, condition=None, on_condition_false=None,
                 on_cancelled=None, on_finish=None, daemon=True):
        threading.Thread.__init__(self)

        if args is None:
            args = []
        if kwargs is None:
            kwargs = dict()
        if condition is None:
            condition = lambda: True

        if not callable(interval):
            self.interval = lambda: interval
        else:
            self.interval = interval

        self.function = function
        self.finished = threading.Event()
        self.args = args
        self.kwargs = kwargs
        self.run_first = run_first
        self.condition = condition

        self.on_condition_false = on_condition_false
        self.on_cancelled = on_cancelled
        self.on_finish = on_finish

        self.daemon = daemon

    def cancel(self):
        self._finish(self.on_cancelled)

    def run(self):
        while self.condition():
            if self.run_first:
                # if we are to run the function BEFORE waiting for the first time
                self.function(*self.args, **self.kwargs)

                # make sure our condition is still met before running into the downtime
                if not self.condition():
                    break

            # wait, but break if we are cancelled
            self.finished.wait(self.interval())
            if self.finished.is_set():
                return

            if not self.run_first:
                # if we are to run the function AFTER waiting for the first time
                self.function(*self.args, **self.kwargs)

        # we'll only get here if the condition was false
        self._finish(self.on_condition_false)

    def _finish(self, *callbacks):
        self.finished.set()

        for callback in callbacks:
            if not callable(callback):
                continue
            callback()

        if callable(self.on_finish):
            self.on_finish()



class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
