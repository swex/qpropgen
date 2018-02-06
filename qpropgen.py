#!/usr/bin/env python3
import argparse
import os
import sys

import yaml

from jinja2 import Environment, PackageLoader


__appname__ = 'qpropgen'
__version__ = '0.1.0'
__license__ = 'Apache 2.0'

DESCRIPTION = """\
Generate QML property-based headers and implementation
"""

NO_CONST_REF_ARG_TYPES = {'int', 'bool', 'qreal'}

AUTOGENERATED_DISCLAIMER = 'This file has been generated with qpropgen, any' \
    ' changes made to it will be lost!'

HEADER_EXT = '.h'
IMPL_EXT = '.cpp'

VIRTUAL_IMPL = 'virtual'
PURE_IMPL = 'pure'

DEFAULTS = {
    'mutability': 'readwrite',
    'impl': 'plain',
    'access': 'private',
}


def get_filename_we(filepath):
    filename = os.path.basename(filepath)
    return os.path.splitext(filename)[0]


def need_constref(type_):
    return type_ not in NO_CONST_REF_ARG_TYPES and type_[-1] != '*'


class ClassDefinition:
    def __init__(self, filename, dct):
        self.filename_we = get_filename_we(filename)
        self.header = self.filename_we + HEADER_EXT
        self.class_name = dct['class']
        self.base_class_name = dct.get('baseClass', 'QObject')
        self.includes = dct.get('includes', [])

        self._read_defaults(dct)
        self.properties = [self._complete_property(x) for x in
                           dct['properties']]

    def generate_file(self, template, out_path):
        args = dict(
            autogenerated_disclaimer=AUTOGENERATED_DISCLAIMER,
            className=self.class_name,
            baseClassName=self.base_class_name,
            includes=self.includes,
            header=self.header,
            properties=self.properties,
        )

        with open(out_path, 'w') as f:
            f.write(template.render(**args))

    def _read_defaults(self, dct):
        self.defaults = dict(DEFAULTS)
        self.defaults.update(dct.get('defaults', {}))

    def _complete_property(self, property_dct):
        """Reads property_dct, merges it with defaults, compute other fields
        and return the new dictionary"""
        dct = dict(self.defaults)
        dct.update(property_dct)
        camelcase_name = dct['name'][0].upper() + dct['name'][1:]

        dct.setdefault('setterName', 'set' + camelcase_name)

        type_ = dct['type']
        if need_constref(type_):
            arg_type = 'const {}&'.format(type_)
        else:
            arg_type = type_
        dct.setdefault('argType', arg_type)

        dct.setdefault('varName', 'm' + camelcase_name)

        impl = dct['impl']
        if impl == VIRTUAL_IMPL:
            prefix, suffix = 'virtual', ''
        elif impl == PURE_IMPL:
            prefix, suffix = 'virtual', ' = 0'
        else:
            prefix, suffix = '', ''

        dct['declaration_prefix'] = prefix
        dct['declaration_suffix'] = suffix

        return dct


def main():
    parser = argparse.ArgumentParser()
    parser.description = DESCRIPTION

    parser.add_argument('-d', '--directory', dest='directory',
                        default='.',
                        help='generate files in DIR', metavar='DIR')

    parser.add_argument('class_definition')

    args = parser.parse_args()

    with open(args.class_definition, 'r') as f:
        definition = ClassDefinition(args.class_definition, yaml.load(f))

    env = Environment(loader=PackageLoader('qpropgen', 'templates'))

    for ext in HEADER_EXT, IMPL_EXT:
        out_path = os.path.join(args.directory, definition.filename_we + ext)
        template = env.get_template('template{}'.format(ext))
        definition.generate_file(template, out_path)

    return 0


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
