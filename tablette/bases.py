"""
    tablette.bases
    ~~~~~~~~~~~~~~

"""

__all__ = ['Tablette', 'Column']

from math import ceil
from operator import itemgetter
from six import callable, string_types
from termcolor import colored
from .utils import terminal_size


class Column(object):
    """
    Defines a Column.

    :ivar name: name of the column
    :ivar width: initial width of column.
    :ivar template: allows you to format the value field.
                    See `string formatting`_ for the full specification.
    :ivar term: based on termcolor_, it allows to stylizes the displayed field.
                its can be a string, list or a dict.
                Its also mays be a callable that must returns any of the
                previous types. The callable must have this signature::

                     lambda field_value: None

    .. _`string formatting`: http://bit.ly/VS4rQ2
    .. _`termcolor`: http://pypi.python.org/pypi/termcolor
    """

    __slot__ = ['name', 'width', 'template', 'term']

    def __init__(self, name, width, template=None, term=None):
        self.name = name
        self.width = width
        self.template = template or '{:{width}}'
        self.term = term

    def field(self, value):
        return Field(initial=value,
                     width=self.width,
                     template=self.template,
                     term=self.term)

    @property
    def header(self):
        return Header(self.name, self.width)


class Field(object):
    __slot__ = ['initial', 'width', 'template', 'term', 'resolved', 'length']

    def __init__(self, initial, width, template=None, term=None):
        self.initial = initial
        self.width = width
        self.template = template or '{:{width}}'

        if callable(term):
            term = term(initial)

        self.term = term

        self.resolved = self.template.format(self.initial, width=self.width)
        self.length = len(self.resolved)

    def __str__(self):
        return self.resolved

    def __len__(self):
        return self.length


class Header(object):
    __slot__ = ['initial', 'width', 'resolved', 'length']

    def __init__(self, initial, width):
        self.initial = initial
        self.width = width
        self.resolved = '{:{width}}'.format(self.initial, width=self.width)
        self.length = len(self.resolved)

    def __str__(self):
        return self.resolved

    def __len__(self):
        return self.length


class Tablette(object):
    """
    Decorates an iterator with tablette.

    :ivar columns: list of :class:Column
    :ivar data: the iterator
    """

    __slot__ = ['columns', 'data']

    def __init__(self, columns, data=None):
        """
        :param columns: a list where each element will be consumed
                        by :meth:add_column
        :param data: any iterator
        """
        self.data = data or []
        self.columns = []
        for column in columns:
            self.add_column(column)

    def add_column(self, obj):
        """
        Injects a new column.

        :param obj: it can be a string, dict or a Column instance.
        """

        if not isinstance(obj, Column):
            if isinstance(obj, dict):
                name = obj.get('name', '')
                template = obj.get('template', '{:{width}}')
                term = obj.get('term', None)
                if 'width' in obj:
                    width = obj['width']
                elif 'name' in obj:
                    width = len(obj['name'])
                else:
                    width = 1
            else:
                name = obj
                template = '{:{width}}'
                term = None
                width = len('{}'.format(name))
            obj = Column(name=name, width=width, template=template, term=term)
        self.columns.append(obj)

    @property
    def headers(self):
        return [column.header for column in self.columns]

    def __iter__(self):
        for values in self.data:
            fields = []
            for value, column in zip(values, self.columns):
                fields.append(column.field(value))
            yield fields

    def printer(self):
        return Printer(self)


class Printer(object):
    __slot__ = ['tablette', 'height', 'width']

    def __init__(self, tablette):
        self.tablette = tablette
        self.height = 50
        self.width = 50

    def __iter__(self):
        self.width, self.height = terminal_size()
        buffer = []
        for i, fields in enumerate(self.tablette):
            buffer.append(fields)
            if i and (i % self.height) == 0:
                for row in self.resolve_buffer(buffer):
                    yield row
        while buffer:
            for row in self.resolve_buffer(buffer):
                yield row

    def resolve_buffer(self, buffer):
        self.width, self.height = terminal_size()
        headers = self.tablette.headers
        rows = []

        # define optimistic length
        lengths = Length([header.length for header in headers])
        for fields in buffer:
            lengths.register([field.length for field in fields])

        sizes = lengths.caped(self.width)

        # do the heading fu
        rows.append('+-' + '-+-'.join('-' * size for size in sizes) + '-+')

        squares, lines = compartment(headers, sizes)
        for y in range(0, lines + 1):
            row = []
            for x, size in enumerate(sizes):
                row.append('{:{width}}'.format(squares.get((x, y), ' '),
                                               width=size))
            rows.append('| ' + ' | '.join(row) + ' |')
        rows.append('+-' + '-+-'.join('-' * size for size in sizes) + '-+')

        consumed_values = 0
        for fields in buffer:
            block = []
            squares, lines = compartment(fields, sizes)
            for y in range(0, lines + 1):
                row = []
                for x, size in enumerate(sizes):
                    response = '{:{width}}'.format(squares.get((x, y), ' '),
                                                   width=size)
                    term = fields[x].term
                    if isinstance(term, list):
                        response = colored(response, *term)
                    elif isinstance(term, dict):
                        response = colored(response, **term)
                    elif isinstance(term, string_types):
                        response = colored(response, term)
                    row.append(response)
                block.append('| ' + ' | '.join(row) + ' |')

            if len(rows) + len(block) < (self.height - 1):
                rows.extend(block)
                consumed_values += len(block)
            else:
                break
        rows.append('+-' + '-+-'.join('-' * size for size in sizes) + '-+')

        for i in range(len(rows), self.height - 1):
            rows.append('')

        buffer[:consumed_values] = []
        return rows


class Length(object):
    __slots__ = ['buffer']

    def __init__(self, sizes):
        self.buffer = [[size] for size in sizes]

    def register(self, sizes):
        for i, size in enumerate(sizes):
            self.buffer[i].append(size)

    @property
    def max(self):
        return [max(*d) for d in self.buffer]

    def caped(self, width):
        sizes = self.max[:]

        for i in range(10):
            # try to find the best match 10 times
            total = sum(sizes) + (len(sizes) * 2) + len(sizes) + 1
            if total <= width:
                break
            index, value = max(enumerate(sizes), key=itemgetter(1))
            sizes[index] = int(ceil(value / 2))
            total = sum(sizes) + (len(sizes) * 2) + len(sizes) + 1
            if total < width:
                sizes[index] += width - total
                break

        return sizes


def compartment(fields, sizes):
    x, y, lines = 0, 0, 0
    response = {}
    for x, (field, size) in enumerate(zip(fields, sizes)):
        y = 0
        field = str(field)
        while len(field) > size:
            tmp, field = field[:size], field[size:]
            response[(x, y)] = tmp
            y += 1
            lines = max(lines, y)
        field = '{:{width}}'.format(field, width=size)
        response[(x, y)] = '{:{width}}'.format(field, width=size)

    return response, lines
