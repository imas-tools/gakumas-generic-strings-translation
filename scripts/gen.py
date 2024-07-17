import os, json
from typing import List
from utils import (
    source_strings_dir,
    translation_dir,
    working_todo_dir,
    yield_source_string_from_translated_dir,
    yield_string,
    SPLIT_STRING_PREFIX,
)


def untranslated_strings_to_map(untranslated_strings: List[str]) -> dict:
    rtn = {}
    for s in untranslated_strings:
        rtn[s] = SPLIT_STRING_PREFIX if s.startswith(SPLIT_STRING_PREFIX) else ""
    return rtn


def gen_todo():
    translated_strings: List[str] = []
    for s, _ in yield_source_string_from_translated_dir(translation_dir):
        translated_strings.append(s)

    for root_path, _, file_names in os.walk(source_strings_dir):
        for file_name in file_names:
            if not file_name.endswith(".json"):
                continue
            file_path = os.path.join(root_path, file_name)
            rel_path = os.path.relpath(file_path, source_strings_dir)
            dest_path = os.path.join(working_todo_dir, rel_path)

            untranslated_strings = []
            for s, _ in yield_string(file_path):
                if s not in translated_strings:
                    untranslated_strings.append(s)

            if len(untranslated_strings) > 0:
                # save file in dest_path
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "w", encoding="utf-8") as f:
                    json.dump(untranslated_strings_to_map(untranslated_strings), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    gen_todo()
