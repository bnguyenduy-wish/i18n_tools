import re
import os
import sys

SPLITTER = "|"


def main(input_file_name):
    i18n_data = []

    with open(input_file_name, "r") as file:
        line_count = 0
        while True:
            line = file.readline()
            if not line:
                break

            line_count += 1

            if SPLITTER not in line:
                continue

            data = extract_key_value(line)
            i18n_data.append(
                (
                    data["key"],
                    transform_to_i18n_call(data["content"], data.get("context")),
                )
            )

    output_file_name = os.path.splitext(input_file_name)[0] + ".py"
    write_i18n_python_file(output_file_name, i18n_data)
    print("generated python file: ", output_file_name)


def write_i18n_python_file(output_file_name, i18n_data):
    with open(output_file_name, "w") as file:
        file.writelines(["from sweeper.i18n import i18n, ci18n\n\n", "i18n_dict = {\n"])

        for key, value in i18n_data:
            file.writelines(["    '{}': {},\n".format(key, value)])

        file.writelines(["}\n", "\n"])


def extract_key_value(text):
    # test text with context template, example "key | context: context should be here | content is here "
    groups = re.findall(".+\|\s*(context\s*:).+\|.+", text)
    if groups:
        subs = text.split(SPLITTER, 2)
        data = {
            "key": subs[0].strip(),
            "context": subs[1].replace(groups[0], "").strip(),
            "content": subs[2].strip(),
        }
    else:
        subs = text.split(SPLITTER, 1)
        data = {"key": subs[0].strip(), "content": subs[1].strip()}

    data["key"] = to_snake_case(data["key"])

    return data


def transform_to_i18n_call(text, context=None):
    groups = re.findall("(\[\[\s*[\w\s_\-]+\s*\]\])", text)

    i18n_call = "i18n("
    if context:
        i18n_call = 'ci18n("' + context + '", '

    if not groups:
        return "lambda: " + i18n_call + 'u"' + escape_string(text) + '")'

    i18n_lambda = ""
    var_names = []
    i18n_string = text
    for i, g in enumerate(groups):
        var_name = g.replace("[", "").replace("]", "").strip()
        var_name = to_snake_case(var_name)
        var_names.append(var_name)
        i18n_string = i18n_string.replace(g, "{%" + str(i + 1) + "=" + var_name + "}")

    i18n_string = escape_string(i18n_string)
    i18n_lambda = (
        "lambda "
        + ", ".join(var_names)
        + ": "
        + i18n_call
        + 'u"'
        + i18n_string
        + '", '
        + ", ".join(var_names)
        + ")"
    )

    return i18n_lambda


def escape_string(text):
    return to_unicode_escape(text).replace('"', '\\"')


def to_unicode_escape(text):
    if sys.version_info.major == 2:
        return text.decode("utf-8").encode("unicode-escape")

    return text.encode("unicode-escape").decode()


def to_snake_case(text):
    text = re.sub("\W", " ", text)
    subs = [sub.strip().lower() for sub in text.split(" ")]
    return "_".join([sub for sub in subs if sub])


if __name__ == "__main__":

    for a in sys.argv[1:]:
        main(a)
