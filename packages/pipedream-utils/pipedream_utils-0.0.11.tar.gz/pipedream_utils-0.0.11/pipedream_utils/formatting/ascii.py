from typing import Dict

import prettytable as prettytable

default_title_config = {
    'key': {
        'title': 'Event',
        'max_width': 10,
    },
    'value': {
        'title': 'Details',
        'max_width': 10,
    }
}


def _get_value(data, key):
    if type(data) == dict:
        return data[key]

    return getattr(data, key)


def create_key_value_table(data, data_config: Dict, title_config: Dict = None, header=True, footer: bool = False):
    if title_config is None:
        title_config = default_title_config

    table = prettytable.PrettyTable([item['title'] for item in title_config.values()])
    table._max_width = {item['title']: item['max_width'] for item in title_config.values()}

    for item in title_config.values():
        table.align[item['title']] = item.get('align', 'c')

    for attr, config in data_config.items():
        key = config['display_name']
        value = config['formatter'](_get_value(data, attr))
        if not key and not value:
            continue
        table.add_row((key, value))

    table = table.get_string(header=header)

    if footer:
        table = with_table_footer(table)

    return table


def create_key_value_tables(data, data_config: Dict, title_config: Dict = None, footer: bool = False):
    tables = []

    for row in data:
        table = create_key_value_table(row, data_config, title_config, footer)
        tables.append(table)

    return '\n\n'.join(tables)


def with_table_footer(table: str):
    list_of_table_lines = table.split('\n')
    horizontal_line = list_of_table_lines[0]
    result_lines = 1
    msg = "\n".join(list_of_table_lines[:-(result_lines + 1)])
    msg += f'\n{horizontal_line}\n'
    msg += "\n".join(list_of_table_lines[-(result_lines + 1):])
    return msg


def default_formatter(x):
    return x


def float_formatter(x):
    return "{0:.2f}".format(x)


def date_formatter(x):
    try:
        return x.strftime('%d %b')
    except AttributeError:
        return x


def add_title_in_pretty_table(table: str, title: str):
    top_border, table = table.split('\n', 1)
    header_table = prettytable.PrettyTable(['h'])
    header_table._max_width = {'h': len(top_border)-4}
    header_table._min_width = {'h': len(top_border)-4}
    header_table.add_row([title])
    header = '\n'.join(header_table.get_string().splitlines()[2:])
    return '\n'.join([header, table])
