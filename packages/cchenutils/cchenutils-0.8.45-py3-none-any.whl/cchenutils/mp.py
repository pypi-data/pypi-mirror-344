import random
import traceback

from .files import write


def writer(queue):
    """
    Listens to `queue` for file writing tasks. Expects a tuple:

    - For CSV:
        (fp, data, headers, [optional scrape_time])
    - For JSON/JSONL:
        (fp, data)

    Use 'STOP' to end the loop.
    """
    while True:
        args = queue.get()
        if args == 'STOP':
            break
        if len(args) < 2:
            print(f'[writer] Invalid input: {args}')
            continue
        write(*args)


def scraper(func, *func_args, proxy_list=None, **kwargs):
    retries = kwargs.get('retries', 3)
    if proxy_list is None:
        retries = min([1, retries])
    for _ in range(retries):
        try:
            proxy = random.choice(proxy_list) if proxy_list else None
            return func(*func_args, **kwargs, proxy=proxy)
        except Exception as e:
            print(*func_args, e)
            if kwargs.get('debug'):
                print(traceback.print_exc())
    return None
