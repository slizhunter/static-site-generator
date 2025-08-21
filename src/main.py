from generate_pages import (
    prepare_directory,
    copy_directory,
    generate_pages_recursive
)

def main():
    prepare_directory("public")
    copy_directory("static", "public")
    generate_pages_recursive("content/", "template.html", "public/")

main()