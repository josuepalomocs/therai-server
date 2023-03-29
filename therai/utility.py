from django.utils import html


def clean_html_string(input_string):
    # Replace newlines and tabs with spaces
    input_string = input_string.replace('\n', ' ').replace('\t', ' ')

    # Replace escaped ampersands with their unescaped equivalent
    input_string = input_string.replace('&amp;', '&')

    # Escape HTML special characters
    input_string = html.escape(input_string)

    # Remove unnecessary whitespace
    input_string = ' '.join(input_string.split())

    return input_string

