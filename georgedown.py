#!/usr/bin/python

import sys
import re

def check_indent(str):
    for i,c in enumerate(str):
        if c != ' ':
            return i, str[i:]
    return (i, "") # if all spaces

def reindent(level, str):
    return " " * level + str

def main(argv):
    # file = open(sys.argv[0], 'w')
    file = sys.stdout

    # main loop
    markdown = ""
    for line in sys.stdin:
        line = line[:-1] # strip newl

        # skip blanks, but keep the spacing
        if line == "":
            markdown += "\n"
            continue

        # handle indent
        (level, line) = check_indent(line)

        # headers
        # georgeheaders are denoted by a terminal space.  replace this with
        # an initial octothorpe
        if line[-1] == ":":
            line = "#" + "#" * level + " " + line[0:-1]

        # bullets
        # georgebullets are indented two extra spaces.  these should be purged
        if line[0] == "-":
            line = reindent(level - 2, line)

        # italics
        # replace /word/ with *word*
        # points of note: only cases where each / is borded on exact
        line = re.sub(r"(^|[\s])/\b([^/]+)\b/([\s]|$)", r"\1*\2*\3", line)

        # autolink email
        line = re.sub(r"\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})\b",
                      r"[\1](mailto:\1)", line, 0, re.IGNORECASE)

        # links

        line += "\n" # reinsert newl
        markdown += line

    file.write(markdown)

if __name__ == "__main__":
    main(sys.argv[1:])
