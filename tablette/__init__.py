"""
    tablette
    ~~~~~~~~

"""

__all__ = ['Printer', 'Tablette']

import logging
from blinker import Namespace
from six import callable, string_types
from termcolor import colored
from .utils import terminal_size

logger = logging.getLogger(__name__)
signal = Namespace().signal
resized = signal('resized', doc="Emited when size of table has changed.")
pre_format = signal('pre-format', doc="Emited before line formatting.")

def check_size(instance, fields):
    maximum = instance.maximum
    a = [len('{}'.format(field)) for field in fields]
    b = [max(*sizes) for sizes in zip(a, instance.sizes)]
    if b != instance.sizes:
        resized.send(instance, previous=b, current=instance.sizes)
        instance.sizes = b


class Tablette(object):

    def __init__(self, columns, data=None):
        super(Tablette, self).__init__()
        self.data = data or []

        self.names = []
        self.sizes = []
        self.terms = []
        self.templates = []

        for column in columns:
            self.add_column(column)

        self._row_len = 0
        self.maximum = terminal_size()[0]

    def add_column(self, column):
        if isinstance(column, dict):
            name = column.get('name', '')
            template = column.get('template', '{:{width}}')
            term = column.get('term', None)
            if 'width' in column:
                width = column['width']
            elif 'name' in column:
                width = len(column['name'])
            else:
                width = 1
        else:
            name = column
            template = '{:{width}}'
            term = None
            width = len('{}'.format(name))

        self.names.append(name)
        self.terms.append(term)
        self.sizes.append(width)
        self.templates.append(template)

    @property
    def header(self):
        check_size(self, self.names)
        rendered = []
        for value, width in zip(self.names, self.sizes):
            response = '{:{width}}'.format(value, width=width)
            rendered.append(response)
        response = '| ' + ' | '.join(rendered) + ' |'
        self._row_len = max(self._row_len, len(response))
        return response

    @property
    def separator(self):
        return '+' + '+'.join(
            '-' * width + '--' for width in self.sizes
        ) + '+'

    def __iter__(self):
        for values in self.data:
            pre_format.send(self, row=values)
            response = self.format(values)
            curr_len = len(response)
            if curr_len != self._row_len:
                check_size(self, values)
                self._row_len = curr_len
            yield response

    def format(self, line):
        rendered = []
        for value, width, template, term in zip(line, self.sizes,
                                                      self.templates,
                                                      self.terms):
            response = template.format(value, width=width)
            if term:
                if callable(term):
                    term = term(value)
                if isinstance(term, list):
                    response = colored(response, *term)
                if isinstance(term, dict):
                    response = colored(response, **term)
                if isinstance(term, string_types):
                    response = colored(response, term)
            rendered.append(response)
        return '| ' + ' | '.join(rendered) + ' |'

    def printer(self, split=None):
        return Printer(self, split)


class Printer(object):
    def __init__(self, tablette, split=None):
        super(Printer, self).__init__()
        self.tablette = tablette
        self.split = split

    def __iter__(self):

        def block():
            self.tablette.maximum = terminal_size()[0]
            yield self.tablette.separator
            yield self.tablette.header
            yield self.tablette.separator

        rows = iter(self.tablette)
        pos = 0
        for row in rows:
            if pos == 0 or self.split and pos % self.split == 0:
                for line in block():
                    yield line
            yield row
            pos += 1

        yield self.tablette.separator
