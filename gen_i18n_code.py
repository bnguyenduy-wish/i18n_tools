from curses.ascii import isascii
import re
import os
import sys

SPLITTER = "|"


def main(input_file_name):
    i18n_dict = {}

    with open(input_file_name, "r") as file:
        line_count = 0
        while True:
            line = file.readline()
            if not line:
                break

            line_count += 1

            if SPLITTER not in line:
                continue

            key, value = extract_key_value(line)
            i18n_dict[key] = transform_to_i18n_call(value)

    output_file_name = os.path.splitext(input_file_name)[0] + ".py"
    write_i18n_python_file(output_file_name, i18n_dict)
    print("generated python file: ", output_file_name)


def write_i18n_python_file(output_file_name, i18n_dict):
    with open(output_file_name, "w") as file:
        file.writelines(["from sweeper.i18n import i18n, ci18n\n\n", "i18n_dict = {\n"])

        for key, value in i18n_dict.items():
            file.writelines(["    '{}': {},\n".format(key, value)])

        file.writelines(["}\n", "\n"])


def extract_key_value(text):
    subs = text.split(SPLITTER, 1)
    return subs[0].strip(), subs[1].strip()


def transform_to_i18n_call(text):
    groups = re.findall("(\[\[\s*[a-z0-9_]+\s*\]\])", text)

    if not groups:
        return 'lambda: i18n(u"' + escape_string(text) + '")'

    i18n_lambda = ""
    var_names = [g.replace("[", "").replace("]", "").strip() for g in groups]
    i18n_string = text
    for i, (var_name, g) in enumerate(zip(var_names, groups)):
        i18n_string = i18n_string.replace(g, "{%" + str(i + 1) + "=" + var_name + "}")

    i18n_string = escape_string(i18n_string)
    i18n_lambda = (
        "lambda "
        + ", ".join(var_names)
        + ': i18n(u"'
        + i18n_string
        + '", '
        + ", ".join(var_names)
        + ")"
    )

    return i18n_lambda


def escape_string(text):
    return replace_not_ascii_chars(text.replace('"', '\\"'))


def replace_not_ascii_chars(text):
    output = ""
    for c in text:
        if c.isascii():
            output += c
        else:
            output += c.encode("unicode-escape").decode()

    return output


if __name__ == "__main__":

    for a in sys.argv[1:]:
        main(a)
