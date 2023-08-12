#!/bin/python3

from threading import Timer


def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        timer = None
        def debounced(*args, **kwargs):
            nonlocal timer
            def call_it():
                fn(*args, **kwargs)
            if timer is not None:
                timer.cancel()
            timer = Timer(wait, call_it)
            timer.start()
        return debounced
    return decorator


if __name__ == "__main__":
    
    @debounce(4)
    def print_count(count):
        print(count)

    print("Start")
            
    for i in range(10):
        print_count(i)

    print("End")