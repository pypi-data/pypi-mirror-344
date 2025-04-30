import csv
import json
import os
import re

from dask import dataframe as dd
from ordered_set import OrderedSet

from .dictutils import Dict
# from cchenutils import Dict
csv.field_size_limit(10_000_000)


def csv_write(fp, data, headers=None):
    writeheader = not os.path.exists(fp) and headers is not None
    rows = data if isinstance(data, list) else [data]
    rows = (dict(zip(headers, Dict(d).gets(headers, serialize=True))) for d in rows)

    with open(fp, 'a', encoding='utf-8') as o:
        writer = csv.DictWriter(o, fieldnames=headers, lineterminator='\n')
        if writeheader:
            writer.writeheader()
        writer.writerows(rows)


def jsonl_write(fp, data):
    rows = data if isinstance(data, list) else [data]
    with open(fp, 'a', encoding='utf-8') as o:
        o.writelines(json.dumps(d) + '\n' for d in rows)


def write(fp, data, *args):
    """
    Writes data to a file based on its extension.

    Supported formats:
    - For CSV files (.csv), the tuple contains:
      - `fp` (str): The file path.
      - `data` (dict or list of dicts): The data to be written.
      - `headers` (iterable): The headers for the CSV columns.
      - `scrape_time` (optional, datetime in str): The time of scraping, added as the first column.
    - For JSON Line (.jsonl) files, the tuple contains:
      - `fp` (str): The file path.
      - `data` (dict or list of dicts): The data to be written.
    """
    if not data:
        return False
    data = data if isinstance(data, list) else [data]
    match os.path.splitext(fp)[1].lower():
        case '.csv':
            match len(args):
                case 0:
                    headers = None
                case 1:
                    headers = args[0]
                case _:
                    headers = ['scrape_time'] + args[0]
                    for d in data:
                        d['scrape_time'] = args[1]
            csv_write(fp, data, headers)
        case '.jsonl':
            jsonl_write(fp, data)
        case _:
            print(f'Unsupported file type for {fp}')
    return True


def read_id(fp, ids, dtype=None, *, agg=None, filters=None, agg_filters=None) -> Dict | OrderedSet:
    """
    Read data from a CSV file based on specified ID field(s), with optional filtering and aggregation.

    Args:
        fp (str): The file path to the CSV file.
        ids (str | iterable[str]): Field name(s) used to group the rows.
        dtype (dict, optional): Optional dictionary specifying column types.
        agg (dict, optional): Aggregation to apply, specified as a {field: aggregation} dictionary.
            Currently only one field-aggregation pair is supported.
            Use 'range' to return (min, max) tuples.
        filters (dict, optional): Filter conditions on individual rows, as {field: condition}.
            The condition can be:
              - A scalar (for exact match),
              - A bool (True for not-null, False for null),
              - A regex pattern (re.Pattern),
              - A callable (returns True/False per value).
        agg_filters (dict, optional): Filter rows based on agg'd data, as {field: (agg, condition)}.
            Conditions are same as above.

    Returns:
        Dict | OrderedSet:
            - If `agg` is provided, returns a Dict mapping ID(s) to aggregated values.
                If 'range' is used in the agg, values will be (min, max) tuples
            - Otherwise, returns an OrderedSet of distinct ID(s) after filtering.

    Example:
        > read_id(r"D:\weibo_data\comments.csv", 'mid', filters={'cid': lambda x: int(x) > 5159662870334851}, agg_filters={'cid': ('count', lambda x: x > 99))

        > read_id('data.csv', 'mid', agg={'cid': 'range'})
        {'A': (1, 5), 'B': (2, 8)}

        > read_id('data.csv', ['mid', 'uid'], agg={'likes': 'sum'})
        {('A', '1'): 10, ('B', '2'): 15}

        > read_id('data.csv', 'mid', filters={'status': 'active'})
        ['A', 'B', 'C']

        > read_id('data.csv', 'mid', agg_filters={'likes': ('count', lambda x: x > 5)})
        ['A', 'C']
    """
    if not os.path.exists(fp):
        return Dict() if agg is not None else OrderedSet()

    if isinstance(ids, str):
        ids = [ids]
    else:
        ids = list(ids)

    cols = set(ids)
    if agg is not None:
        cols |= set(agg.keys())
    if filters is not None:
        cols |= set(filters.keys())
    if agg_filters is not None:
        cols |= set(agg_filters.keys())

    if dtype is None:
        dtype = {}
    dtype |= {idf: str for idf in ids if idf not in dtype}
    if filters is not None:
        dtype |= {k: 'object' for k, v in filters.items()
                  if k not in dtype and (agg is None or k not in agg) and (agg_filters is None or k not in agg_filters)}

    ddf = dd.read_csv(fp,
                      dtype=dtype,
                      usecols=list(cols),
                      encoding='utf-8')

    def _apply_filter(ddf, field, expected):
        match expected:
            case bool():  # True or False
                ddf = ddf[ddf[field].notnull()] if expected else ddf[ddf[field].isnull()]
            case re.Pattern():  # Regex filter
                ddf = ddf[ddf[field].str.contains(expected)]
            case func if callable(func):  # Custom function filter
                ddf = ddf.map_partitions(lambda df: df[df[field].map(func)], meta=ddf)
                # ddf = ddf[ddf[field].apply(expected, meta=(None, 'bool'))]
            case _:  # Exact match
                ddf = ddf[ddf[field] == expected]
        return ddf

    if filters:
        for field, expected in filters.items():
            ddf = _apply_filter(ddf, field, expected)

    if agg is not None:
        k, v = agg.popitem()
        if v == 'range':
            return Dict(ddf.groupby(ids).agg({k: ['min', 'max']}).compute()
                        .apply(lambda row: (row[(k, 'min')], row[(k, 'max')]), axis=1).to_dict())
        else:
            return Dict(ddf.groupby(ids).agg({k: v}).compute()
                        .apply(lambda row: row[k], axis=1).to_dict())

    if agg_filters is not None:
        # {'created_at_ts': ('count', lambda x: x > 5)}
        ddf = ddf.groupby(ids).agg({k: a for k, (a, v) in agg_filters.items()})
        for k, (a, v) in agg_filters.items():
            ddf = _apply_filter(ddf, k, v)
        ddf = ddf.reset_index()

    if len(ids) == 1:
        return OrderedSet(ddf[ids[0]].drop_duplicates().compute().tolist())
    else:
        return OrderedSet(ddf[ids].drop_duplicates().compute().apply(tuple, axis=1).tolist())


# def _read_id_matches(expected, value):
#     match expected:
#         case True:
#             return bool(value)
#         case False:
#             return not bool(value)
#         case list() | set() | tuple():
#             return value in expected
#         case re.Pattern():
#             return bool(value and expected.search(value))
#         case func if callable(func):
#             return func(value)
#         case _:
#             return value == expected
#
#
# def _read_id_row_passes_filter(row, filter):
#         if not filter:
#             return True
#         for field, expected in filter.items():
#             value = row.get(field)
#             if _read_id_matches(expected, value) is False:
#                 return False
#         return True
#
#
# def read_id(fp, usecols, filter=None) -> OrderedSet:
#     """
#     Reads specific columns from a CSV file, optionally filtering the rows based on specified conditions.
#
#     The function loads data from a CSV file (`fp`) and extracts values from the specified columns (`usecols`).
#     Rows can be filtered according to conditions specified in the `filter` argument. The function returns a
#     set of unique values from the selected columns, based on the filtering criteria.
#
#     Args:
#         fp (str): The file path to the CSV file.
#         usecols (str | iterable): The column name(s) to extract from the CSV file.
#                                   Can be one name (str) or names (iterable) for multiple fields.
#         filter (dict, optional): A dictionary specifying filtering conditions for the rows. The dictionary should
#                                  have 'include' and/or 'exclude' as keys, with the associated values being
#                                  dictionaries where keys are column names and values are the expected value(s).
#                                  If not provided, no filtering is applied.
#
#     Returns:
#         set: A list of unique values extracted from the specified columns, with rows filtered according to the filter.
#
#     Example:
#         # Read a single column "mid" from the CSV file with `status`=='active
#         read_id('data.csv', 'mid', filter={'include': {'status': 'active'}})
#
#         # Read multiple columns ("mid", "cid") with `status` being empty
#         read_id('data.csv', ('mid', 'cid'), filter={'exclude': {'status': True}})
#     """
#     if not os.path.exists(fp):
#         return OrderedSet()
#
#     if isinstance(usecols, str):
#         usecols = (usecols,)
#
#     with open(fp, encoding='utf-8') as f:
#         csvreader = csv.DictReader(f)
#         return OrderedSet(tuple(row[col] for col in usecols) if len(usecols) > 1 else row[usecols[0]]
#                           for row in csvreader if _read_id_row_passes_filter(row, filter))
#
#
# def _read_id_agg(fp, id_field, agg_field, mode) -> Dict:
#     """
#     Reads a CSV file and obtains the minimum and maximum for a specified range field, grouped by an ID field.
#
#     The function loads data from a CSV file (`fp`), and for each unique value in the `id_field`, it calculates the
#     minimum and maximum values from the `range_field`. The `range_field` values must be convertible to integers.
#     The results are returned as a dictionary where the keys are the values from the `id_field`, and the values are
#     tuples containing the minimum and maximum values of the `range_field`.
#
#     Args:
#         fp (str): The file path to the CSV file.
#         id_field (str): The name of the field used to group the rows.
#         agg_field (str): The name of the field whose minimum and maximum values are calculated for each group.
#                          The values in this field must be convertible to integers.
#         mode (str): Mode of extraction. Options:
#             - 'range' (default): Return (min, max) tuple of values.
#             - 'first': Return the first encountered value.
#             - 'last': Return the last encountered value.
#             - 'count': counts the number of occurrences of the `agg_field` for each `id_field`
#
#     Returns:
#         Dict: A dictionary where the keys are the values from the `id_field`, and the values are tuples with the
#               minimum and maximum values from the `range_field` for each unique `id_field`.
#
#     Example:
#         # Read a CSV and calculate the min and max values of 'cid' for each 'mid' field
#         > read_id_range('data.csv', 'mid', 'cid')
#         {'A': (1, 5), 'B': (2, 8)}
#     """
#     if not os.path.exists(fp):
#         return Dict()
#
#     match mode:
#         case 'range':
#             def init(new_value):
#                 return int(new_value), int(new_value)
#             def agg(current_value, new_value):
#                 current_min, current_max = current_value
#                 new_value = int(new_value)
#                 return min(current_min, new_value), max(current_max, new_value)
#         case 'first':
#             def init(new_value):
#                 return new_value
#             def agg(current_value, new_value):
#                 return current_value
#         case 'last':
#             def init(new_value):
#                 return new_value
#             def agg(current_value, new_value):
#                 return new_value
#         case 'count':
#             def init(new_value):
#                 return 1
#             def agg(current_value, new_value):
#                 return current_value + 1
#         case _:
#             raise ValueError(f"Invalid mode: {mode}")
#
#     result = {}
#     with open(fp, encoding='utf-8') as f:
#         csvreader = csv.DictReader(f)
#         for row in csvreader:
#             id_value = row[id_field]
#             agg_value = row[agg_field]
#             result[id_value] = init(agg_value) if id_value not in result else agg(result[id_value], agg_value)
#     return Dict(result)


if __name__ == '__main__':
    fp = r"D:\weibo_data\comments.csv"
    ids = ('mid', 'cid')
    agg = {'cid': 'range'}
    id_fields = 'mid'
    filter = {'cid': lambda x: x > 5159662870334851}  #  '5159585070449585': (5159653379673776, 5160212470431950)
    a = read_id(fp, ids,
                # agg=agg,
                filters={'cid': True}
                )
    a = read_id(r"D:\weibo_data\comments.csv", 'mid', filters={'cid': lambda x: int(x) > 5159662870334851},
                agg_filters={'cid': ('count', lambda x: x > 99)})
