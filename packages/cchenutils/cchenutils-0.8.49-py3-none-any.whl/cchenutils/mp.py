import random
import time
import traceback

from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout, Timeout

from .files import write, txt_write


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
        while True:
            try:
                write(*args)
                break
            except PermissionError:
                time.sleep(1)


def scraper(func, *func_args, proxy_list=None, proxyerr=None, stderr=None, **kwargs):
    retries = kwargs.pop('retries', 3)
    debug = kwargs.pop('debug', None)
    if proxy_list is None:
        retries = min(1, retries)
    for _ in range(retries):
        proxy = random.choice(proxy_list) if proxy_list else None
        try:
            return func(*func_args, **kwargs, proxy=proxy)
        except (ProxyError, ConnectTimeout, ReadTimeout, Timeout):
            try:
                proxy_list.remove(proxy)
                if proxyerr is not None:
                    txt_write(proxyerr, proxy)
            except TypeError:
                pass
        except Exception:
            if stderr:
                txt_write(stderr, [proxy, *func_args, traceback.format_exc()])
            else:
                print(proxy, *func_args)
            if debug:
                traceback.print_exc()
                time.sleep(300)
    return None
