#!/usr/bin/python3

'''Automatically send a request according to article 15 GDPR.'''

import json
import subprocess
import sys
from string import Template

def main(argv):
    '''Print LaTeX letter of the request on the command line.'''
    try:
        with open(argv[1], mode='r', encoding='utf-8') as institution_file, \
            open('config.json', mode='r', encoding='utf-8') as requester_file:
            institution = json.loads(institution_file.read())
            requester = json.loads(requester_file.read())
    except IOError:
        print(f'Error: {argv[1]} or \'config.json\' do(es) not exist.')
        raise
    data = institution['company']
    data.update(requester)
    with open('letter.template', mode='r', encoding='utf-8') as template_file, \
        open('letter.tex', mode='w', encoding='utf-8') as letter_file:
        template = Template(template_file.read())
        letter_file.write(template.substitute(data))
    subprocess.call(['lualatex', 'letter.tex'])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} institution.json')
        sys.exit(2)
    else:
        main(sys.argv)
