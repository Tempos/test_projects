import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        stop_time = time.time()
        print(f"Time spent: {stop_time-start_time}")
        return func
    return wrapper


def logit(func):
    def wrapper(*args, **kwargs):
        print(f"Starting {func.__name__}.")
        func(*args, **kwargs)
        print(f"{func.__name__} ".capitalize() + "finished it's work.")
        return func
    return wrapper


def modify(*mod_args):
    def wrapper(func):
        def modify_it(*args, **kwargs):
            args = list(args)
            for i in range(min(len(mod_args), len(args))):
                args[i] = args[i] / mod_args[i]
            func(*args, **kwargs)
            return func
        return modify_it
    return wrapper


# def override(*override_args, **override_kwargs):
#     def wrapper(func):
#         def override(*args, **kwargs):
#             min_args_len = min(len(args), len(override_args))
#             args = [override_args[i] for i in range(min_args_len)]
#             kwargs.update(override_kwargs)
#             return func(*args, **kwargs)
#         return override
#     return wrapper


# @override(100, 50)
@modify(2, 4)
# @logit
# @timeit
def my_func(a, b):
    print(f"Result is: {a + b}")


my_func(10, 5)
