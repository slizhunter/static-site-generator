import sys

from generate_pages import (
    prepare_directory,
    copy_directory,
    generate_pages_recursive
)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    prepare_directory("docs")
    copy_directory("static", "docs")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

main()