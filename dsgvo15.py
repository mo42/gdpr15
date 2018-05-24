#!/usr/bin/python

'''Automatically send a request according to article 15 GDPR.'''

import json
import subprocess
import sys

class Institution(object):
    '''This class represents the institution to which the request ist sent.'''
    def __init__(self, institution_json):
        self.institution = json.load(institution_json)
        self.name = self.institution['company']['name']
        self.street = self.institution['company']['street']
        self.zip = self.institution['company']['pcode']
        self.city = self.institution['company']['city']
        self.mail = self.institution['company']['email']


class Requester(object):
    '''This class represents the requester.'''
    def __init__(self, requester_json):
        self.requester = json.load(requester_json)
        self.name = self.requester['name']
        self.street = self.requester['street']
        self.city = self.requester['city']
        self.zip = self.requester['zip']
        self.birth_date = self.requester['birth_date']

class Letter(object):
    '''This class represents the letter for requesting your own information
    according to article 15 GDPR.'''
    def __init__(self, institution_json, requester_json):
        self.institution = Institution(institution_json)
        self.requester = Requester(requester_json)
        text = open('dsgvo15.txt', 'r')
        self.text = text.read()

    def to_tex(self):
        '''Create a LaTeX scrlttr2 request.'''
        string = r'\documentclass[fontsize=12pt,a4paper]{scrlttr2}' + '\n' \
            + '\\usepackage[utf8]{inputenc}\n' \
            + '\\usepackage[ngerman]{babel}\n' \
            + r'\setlength{\parindent}{0pt}' + '\n' \
            + r'\setlength{\parskip}{.36cm plus0.09cm minus0.09cm}' + '\n\n' \
            + r'\begin{document}' + '\n' + r'\begin{letter}{%' + '\n' \
            + self.institution.name + r'\\' + '\n' \
            + self.institution.street + r'\\' + '\n' \
            + self.institution.zip + ' ' + self.institution.city + r'\\' \
            + '\n' + '}\n\n' \
            + r'\setkomavar{fromname}{' + self.requester.name + '}\n' \
            + r'\setkomavar{fromaddress}{%' + '\n' \
            + self.requester.street + r'\\' + '\n' \
            + self.requester.zip + ' ' + self.requester.city + '\n' \
            + '}\n\n' \
            + r'\setkomavar{place}{' + self.requester.name + '}\n' \
            + r'\setkomavar{place}{' + self.requester.city + '}\n\n' \
            + r'\setkomavar{date}{\today}' + '\n\n' \
            + r'\setkomavar{subject}{Selbstauskunft nach Art. 15 DSGVO}' + '\n\n' \
            + r'\opening{Sehr geehrte Damen und Herren,}' + '\n\n' \
            + self.text + '\n' \
            + r'Mein Name: \textbf{' + self.requester.name + r'}\\' + '\n' \
            + r'Mein Geburtsdatum: \textbf{' + self.requester.birth_date + '}\n' \
            + '\n' \
            + r'Meine gegenwärtige Anschrift:' + '\n' \
            + r'\textbf{' + self.requester.street + ', ' \
                + self.requester.zip + ' ' + self.requester.city + '}\n' \
            + '\n' \
            + r'\renewcommand*{\raggedsignature}{\raggedright}' + '\n' \
            + r'\raggedsignature' + '\n' \
            + r'\closing{Freundliche Grüße}' + '\n' \
            + r'\end{letter}' + '\n' \
            + r'\end{document}' + '\n'
        return string

    def to_pdf(self, file_name='letter.tex'):
        '''Create a request in the PDF format. This requires pdflatex to be
        installed.'''
        file = open(file_name, 'w')
        file.write(self.to_tex())
        file.close()
        subprocess.call(['pdflatex', file_name])
        #file_name = file_name.split('.')
        #file_name[-1] = 'pdf'
        #self.file = '.'.join(file_name)


def main(argv):
    '''Print LaTeX letter of the request on the command line.'''
    try:
        institution = open(argv[1], 'r')
        requester = open('config.json', 'r')
    except IOError:
        print('Error: ' + argv[1] + ' or \'config.json\' do(es) not exist.')
        raise
    letter = Letter(institution, requester)
    letter.to_pdf()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: bdsg34.py institution.json')
        sys.exit(2)
    else:
        main(sys.argv)
