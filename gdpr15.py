#!/usr/bin/python3

"""Automatically send a request according to article 15 GDPR."""

import argparse
import json
import subprocess
from string import Template

ESCAPE_CHARACTERS = ["\\", "&", "%", "$", "#", "_", "{", "}", "~", "^"]


def tex_escape(string: str) -> str:
    """Escape special LaTeX characters."""
    for escape_character in ESCAPE_CHARACTERS:
        string = string.replace(escape_character, "\\" + escape_character)
    return string


def clean_file_name(string: str) -> str:
    """Remove special characters from file names."""
    for escape_character in ESCAPE_CHARACTERS:
        string = string.replace(escape_character, "")
    return string.lower().replace(" ", "_")


def tex_escape_dict_values(dictionary: dict):
    """Remove special LaTeX characters from all values in dictionary."""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            tex_escape_dict_values(value)
        else:
            if isinstance(value, str):
                dictionary[key] = tex_escape(value)
    return dictionary


def run(file_name, language):
    """Print LaTeX letter of the request on the command line."""
    try:
        with open(file_name, mode="r", encoding="utf-8") as institution_file, open(
            "config.json", mode="r", encoding="utf-8"
        ) as requester_file:
            institution = tex_escape_dict_values(json.loads(institution_file.read()))
            requester = json.loads(requester_file.read())
    except IOError:
        print(f"Error: {file_name} or 'config.json' do(es) not exist.")
        raise
    data = institution["company"]
    data.update(requester)
    file_name = clean_file_name(institution["company"]["name"])
    with open(
        f"letter_{language}.template", mode="r", encoding="utf-8"
    ) as template_file, open(
        f"{file_name}.tex", mode="w", encoding="utf-8"
    ) as letter_file:
        template = Template(template_file.read())
        letter_file.write(template.substitute(data))
    subprocess.call(["lualatex", f"{file_name}.tex"])


def main():
    parser = argparse.ArgumentParser(
        description="Generate letters according to article 15 GDPR"
    )
    parser.add_argument(
        "-l", "--language", help="language of the data request", required=True
    )
    parser.add_argument(
        "-c",
        "--contacts",
        nargs="+",
        type=str,
        help="contacts files to create request letters",
        required=True,
    )
    arguments = parser.parse_args()
    for contact in arguments.contacts:
        run(contact, arguments.language)


if __name__ == "__main__":
    main()
