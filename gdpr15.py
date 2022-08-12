#!/usr/bin/python3

'''Automatically send a request according to article 15 GDPR.'''

import json
import subprocess
import sys
from string import Template

ESCAPE_CHARACTERS = ['\\', '&', '%', '$', '#', '_', '{', '}', '~', '^']

def tex_escape(string):
    for escape_character in ESCAPE_CHARACTERS:
        string = string.replace(escape_character, f'\{escape_character}')
    return string

def clean_file_name(string):
    for escape_character in ESCAPE_CHARACTERS:
        string = string.replace(escape_character, '')
    return string.lower().replace(' ', '_')

def tex_escape_dict_values(d):
    for k, v in d.items():
        if isinstance(v, dict):
            tex_escape_dict_values(v)
        else:
            if isinstance(v, str):
                d[k] = tex_escape(v)
    return d

def main(file_name):
    '''Print LaTeX letter of the request on the command line.'''
    try:
        with open(file_name, mode='r', encoding='utf-8') as institution_file, \
            open('config.json', mode='r', encoding='utf-8') as requester_file:
            institution = tex_escape_dict_values(
                json.loads(institution_file.read())
            )
            requester = json.loads(requester_file.read())
    except IOError:
        print(f'Error: {file_name} or \'config.json\' do(es) not exist.')
        raise
    data = institution['company']
    data.update(requester)
    file_name = clean_file_name(institution['company']['name'])
    with open('letter.template', mode='r', encoding='utf-8') as template_file, \
        open(f'{file_name}.tex', mode='w', encoding='utf-8') as letter_file:
        template = Template(template_file.read())
        letter_file.write(template.substitute(data))
    subprocess.call(['lualatex', f'{file_name}.tex'])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} institution.json')
        sys.exit(2)
    else:
        for file_name in sys.argv[1:]:
            main(file_name)
