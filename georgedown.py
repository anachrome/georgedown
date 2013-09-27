#!/usr/bin/python

import sys
import getopt
import re

def check_indent(str):
    for i,c in enumerate(str):
        if c != ' ':
            return i, str[i:]
    return (i, "") # if all spaces

def reindent(level, str):
    return " " * level + str

def help(self):
    print "Usage: " + self + " [options] file"
    print "  Options:"
    print "    -o file, --output file  send output to file.  default is stdout"
    print "    -h,      --help         print this help message"
    print "  if file is '-' " + self + " will read from stdin."

def load(self, argv):
    try:
        opts, args = getopt.getopt(argv, "o:h", ["output", "help"])
    except getopt.GetoptError as err:
        print err
        sys.exit(1)

    outfile = sys.stdout
    for opt, arg in opts:
        if opt in ("-o", "--output"):
            outfile = open(arg, "w")
        if opt in ("-h", "--help"):
            help(self)
            sys.exit(0)

    if len(args) < 1:
        print "More args!"
        sys.exit(1)
    elif len(args) > 1:
        print "No!  Too much arg!"
        sys.exit(1)
    else:
        if args[0] == "-":
            infile = sys.stdin
        else:
            try:
                infile = open(args[0], "r")
            except IOError:
                print "Not a real file. > <"
                sys.exit(2)

    return (infile, outfile)


def main():
    infile, outfile = load(sys.argv[0], sys.argv[1:])

    # main loop
    markdown = ""
    for line in infile:
        line = line[:-1] # strip newl

        # skip blanks, but keep the spacing
        if line == "":
            markdown += "\n"
            continue

        # handle indent
        (level, line) = check_indent(line)

        # headers
        # georgeheaders are denoted by a terminal colon.  replace this with
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

    outfile.write(markdown)

if __name__ == "__main__":
    main()
