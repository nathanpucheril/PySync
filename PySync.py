import threading
from functools import wraps


def _optional_arg_decorator(fn):
    @wraps(fn)
    def wrapped_decorator(*args, **kwds):
        if len(args) == 1 and callable(args[0]):
            return fn(args[0])
        else:
            def real_decorator(decoratee):
                return fn(decoratee, *args)
            return real_decorator
    return wrapped_decorator







class ConcurrencyManager(object):
    pass


class FunctionCM(ConcurrencyManager):
    """docstring for FunctionCM."""
    def __init__(self):
        super(FunctionCM).__init__()

    @staticmethod
    @_optional_arg_decorator
    def lock(fn, **acquire_args):
        """Lock.
        """
        return FunctionCM._acquirer(fn, threading.Lock(), acquire_args)

    @staticmethod
    @_optional_arg_decorator
    def rlock(fn, **acquire_args):
        """Reentrant Lock.
        """
        return FunctionCM._acquirer(fn, threading.RLock(), acquire_args)

    @staticmethod
    @_optional_arg_decorator
    def sema(fn, init_value = 1, **acquire_args):
        """Reentrant Lock.
        """
        return FunctionCM._acquirer(fn, threading.Semaphore(init_value), acquire_args)

    @staticmethod
    @_optional_arg_decorator
    def bounded_sema(fn, bound = 1, **acquire_args):
        """Bounded Semaphore.
        """
        return FunctionCM._acquirer(fn, threading.BoundedSemaphore(bound), acquire_args)

    @staticmethod
    def cv():
        """Bounded Semaphore.
        """
        return threading.Condition()


    @staticmethod
    @_optional_arg_decorator
    def cv_wait_until(fn, cv, condition_fn, timeout = None, **acquire_args):
        """Bounded Semaphore.
        """
        assert callable(fn), 'fn parameter must be callable'
        @wraps(fn)
        def waiter(*args, **kwds):
            cv.acquire()
            cv.wait_for(condition_fn, timeout)
            ret = fn(*args, **kwds)
            cv.release()
            return ret
        return waiter

    @staticmethod
    @_optional_arg_decorator
    def cv_notify(fn, cv, **acquire_args):
        """Bounded Semaphore.
        """
        assert callable(fn), 'fn parameter must be callable'
        @wraps(fn)
        def notifier(*args, **kwds):
            print("notify")
            cv.acquire()
            print("inside notify lock")
            ret = fn(*args, **kwds)
            cv.notify()
            print("release notify lock")
            cv.release()
            return ret
        return notifier

    @staticmethod
    @_optional_arg_decorator
    def cv_notify_all(fn, cv, **acquire_args):
        """Bounded Semaphore.
        """
        assert callable(fn), 'fn parameter must be callable'
        @wraps(fn)
        def notifier(*args, **kwds):
            cv.acquire()
            ret = fn(*args, **kwds)
            cv.notify_all()
            cv.release()
            return ret
        return notifier






    @staticmethod
    def _acquirer(fn, toacquire, acquire_args):
        assert callable(fn), 'fn parameter must be callable'
        @wraps(fn)
        def _acquire_and_release(*args, **kwds):
            toacquire.acquire(**acquire_args)
            ret =  fn(*args, **kwds)
            toacquire.release()
            return ret
        return _acquire_and_release






cm = FunctionCM()
consumer = cm.cv()

q = []




def notempty():
    return len(q) > 0



# @cm.cv_wait(cv, condition_fn)
def printer(i):
    print(i)



def add(q):
    # print("add")
    q.append(1)
    # print(q)

@cm.cv_wait_until(consumer, notempty)
def rem(q):
    # print("remove")
    q.pop()
    # print(q)

def thread1():
    for i in range(1000000):
        add(q)
        print(1)
        # printer(1)

def thread2():
    for i in range(1000000):
        rem(q)
        print(2)
        # print(len(q))
        # printer(2)


# def thread3():
#     for i in range(1000000):
#         print(3)
#         add(q)
#         # printer(3)


t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)
# t3 = threading.Thread(target=thread3)

t1.start()
t2.start()
# t3.start()
# lock(3)
#
# test()
