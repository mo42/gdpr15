# gdpr15

This tool automatically generates requests according to article 15 GDPR.

## Dependencies

For it to run, Python and LaTeX is required.
## Features
  - German (de) and English (en) language
  - Generates automatically request letters in LaTeX and PDF format
  - The companies and authorities of
    [selbstauskunft.net](https://selbstauskunft.net/) can be used.

## Quick Start
1. Create a file for a data controller in ```contacts/``` you want your
   information from.
   * There is an example file
   * Alternatively, you can use the files from
     [selbstauskunft.net](https://selbstauskunft.net/)
2. Put your personal information in ```config.json```.
3. Run ```./gdpr15.py --language=en --contacts contacts/sample.json```.
