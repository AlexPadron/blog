# Some Interesting Code Snippets

## Setting a time limit in Python

<pre>
from contextlib import contextmanager
import signal
from typing import Any, Generator


@contextmanager
def time_limit(seconds: int) -> Generator[None, None, None]:
    '''Limit the runtime inside the context'''

    def signal_handler(signum: Any, frame: Any) -> None:
        '''Raise error if there is a timeout'''
        raise RuntimeError('Timeout after {} seconds'.format(seconds))

    old_handler = signal.signal(signal.SIGALRM, signal_handler)

    if signal.alarm(seconds) > 0:
        raise RuntimeError('Overriding an existing alarm')

    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
</pre>

This snippet creates a context manager that sets a SIGALRM handler
for a given time limit. When the context is exited, the alarm is removed.
If the context is not exited in time, a `RuntimeError` is raised. This
snippet can then be used as

<pre>
with time_limit(10):
   do_stuff()
</pre>


## Backoff and Time Limit with GRPC

<pre>
import datetime
import time

import backoff
import grpc


MAX_TRIES = 5
TIMEOUT_MILLISECONDS = 10 * 1000


def _get_time_in_ms():
    """Get time in milliseconds"""
    current_time = pytz.UTC.localize(datetime.datetime.utcnow())
    try:
        return current_time.timestamp() * 1000
    except AttributeError:
        # For py2 compatibility
        return time.mktime(current_time.timetuple()) * 1000


def _backoff_giveup(err):
    """Return True if the client should give up from this error"""
    valid_retry_codes = {grpc.StatusCode.UNAVAILABLE}
    return err.code() not in valid_retry_codes

backoff_wrapper = backoff.on_exception(
    backoff.expo, grpc.RpcError, max_tries=max_tries, giveup=_backoff_giveup)

@backoff_wrapper
def _run_request_with_backoff(start_time, max_milliseconds, method, request):
    """Run a request with backoff"""
   now = _get_time_in_ms()
   max_method_milliseconds = start_time + max_milliseconds - now
   return method(request, timeout=(max_method_milliseconds / 1000))

start = _get_time_in_ms()
_run_request_with_backoff(start, TIMEOUT_MILLISECONDS, grpc_method, grpc_request)
</pre>

This snippet uses the Python backoff library and GRPC's timeouts to provide the
semantics of "Keep retrying requests, until a time limit or number of failures"
We use a similar snippet extensively at Kensho for our GRPC clients.