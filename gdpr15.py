#!/usr/bin/python3

'''Automatically send a request according to article 15 GDPR.'''

import json
import subprocess
import sys
from string import Template

def main(argv):
    '''Print LaTeX letter of the request on the command line.'''
    try:
        institution = json.loads(open(argv[1], 'r').read())
        requester = json.loads(open('config.json', 'r').read())
    except IOError:
        print(f'Error: {argv[1]} or \'config.json\' do(es) not exist.')
        raise
    data = institution['company']
    data.update(requester)
    template = Template(open('letter.template', 'r').read())
    with open('letter.tex', 'w') as letter:
        letter.write(template.substitute(data))
        letter.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {argv[0]} institution.json')
        sys.exit(2)
    else:
        main(sys.argv)
