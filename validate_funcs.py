import re

#------------------#
# Validation rules #
#----------------- #

def validate_name(username):
    # Validates usernames.
    # Only allow letters, hyphens and underscores. No spaces.
    return re.match("^[a-zA-Z0-9-_]{5,15}$", username)


def validate_question(question):
    # Validates question titles
    # Only allow printable characters and spaces but not mathematical operators. Up to 255 characters.
    # Allow the "-" sign as the only mathematical operator
    return re.match(r"^[^\/\+\<\>\*]{5,255}$", question)


def validate_question_text(question_text):
    # Validates question text
    # Only allow printable characters and spaces but not mathematical operators. Up to 1020 characters.
    # Allow the "-" sign as the only mathematical operator
    return re.match(r"^[^\/\+\<\>\*]{5,1020}$", question_text)


def validate_message(message):
    # Validates message text
    # Only allow printable characters and spaces but not mathematical operators. Up to 5000 characters.
    # Allow the "-" sign as the only mathematical operator
    return re.match(r"^[^\/\+\<\>\*]{5,5000}$", message)


def validate_fname(fname):
    # Validates first and last names.
    # Only allow letters and acceptable name symbols.
    return re.match("^[a-zA-Z\s\,\.\'\-]{2,26}$", fname)