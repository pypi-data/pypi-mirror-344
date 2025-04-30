import random
import time
import traceback

from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout, Timeout

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


def scraper(func, *func_args, proxy_list=None, stderr=None, **kwargs):
    retries = kwargs.pop('retries', 3)
    debug = kwargs.pop('debug', None)
    if proxy_list is None:
        retries = min([1, retries])
    for _ in range(retries):
        proxy = random.choice(proxy_list) if proxy_list else None
        try:
            return func(*func_args, **kwargs, proxy=proxy)
        except (ProxyError, ConnectTimeout, ReadTimeout, Timeout):
            try:
                proxy_list.remove(proxy)
                if stderr is not None:
                    write(stderr, proxy)
            except TypeError:
                pass
        except Exception as e:
            print(proxy, *func_args)
            if debug:
                print(traceback.print_exc())
                time.sleep(300)
    return None
