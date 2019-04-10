#!/usr/bin/env python
# -*- coding: utf-8 -*-

def disable(f):
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:
    >>> memo = disable
    '''
    def disable_wrap(*args, **kwargs):
        f(*args, **kwargs)
    return disable_wrap


def decorator(f):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''
    def decorator_wrap(*args, **kwargs):
        f(*args, **kwargs)

    decorator_wrap.__doc__ = f.__doc__
    return decorator_wrap


def countcalls(f):
    '''Decorator that counts calls made to the function decorated.'''
    def countcalls_wrap(*args, **kwargs):
        countcalls_wrap.calls = getattr(countcalls_wrap, "calls", 0) + 1
        return f(*args, **kwargs)

    countcalls_wrap.__dict__ = f.__dict__ # make nested decorators possible
    return countcalls_wrap


def memo(f):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    def memo_wrap(*args, **kwargs):
        key = args + tuple(kwargs.values())
        val = memo_wrap.cache.get(key, None)

        if not val:
            result = f(*args, **kwargs)
            memo_wrap.cache[key] = result
            return result
        return val

    memo_wrap.__dict__ = f.__dict__
    memo_wrap.cache = {}
    return memo_wrap


def n_ary(f):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''
    def n_ary_wrap(*args):
        if len(args) == 1:
            return args[0]

        elif len(args) == 2:
            return f(args[0], args[1])

        return f(args[0], n_ary_wrap(*args[1:]))

    n_ary_wrap.__dict__ = f.__dict__
    return n_ary_wrap


def trace(indent):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3
    '''

    def trace_wrap(f):
        def trace_wrap2(*args, **kwargs):
            args_strs = (str(x) for x in args)
            args_str = "(" + ", ".join(args_strs) + ")"
            print(str(indent) * trace_wrap2.depth + " --> " + f.__name__ + args_str)
            trace_wrap2.depth += 1
            result = f(*args, **kwargs)
            trace_wrap2.depth -= 1
            print(str(indent) * trace_wrap2.depth + " <-- " + f.__name__ + args_str + " == " + str(result))
            return result
        trace_wrap2.__dict__ = f.__dict__
        trace_wrap2.depth = 0
        return trace_wrap2
    return trace_wrap


@n_ary
@memo
@countcalls
def foo(a, b):
    return a + b


@memo
@n_ary
@countcalls
def bar(a, b):
    return a * b


@trace("####")
@memo
@countcalls
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print(foo(4))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    fib(6)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
