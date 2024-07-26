import os, json, warnings, re
from typing import Dict, List, cast, Tuple, Generator

SPLIT_STRING_PREFIX = "[__split__]"

source_strings_dir = "./gakumas-generic-source-strings/data"
translation_dir = "./translated"
working_new_dir = "./working/new"
working_todo_dir = "./working/todo"


# yield (string, is_split)
def yield_string(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")

        for k in content:
            yield (cast(str, k), (cast(str, k).startswith(SPLIT_STRING_PREFIX)))


def yield_string_from_dir(dir_path: str) -> Generator[Tuple[str, bool], None, None]:
    for root_path, _, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(".json"):
                continue
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                yield from yield_string(file_path)


def yield_source_string_from_translated_dir(dir_path: str) -> Generator[Tuple[str, bool], None, None]:
    for root_path, _, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(".json"):
                continue
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    content = json.load(file)
                    if not isinstance(content, dict):
                        raise ValueError("Invalid JSON content")
                    for k in content:
                        yield k, k.startswith(SPLIT_STRING_PREFIX)


def get_kvs_for_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_kvs_for_dir(dir_path: str):
    kvs = {}
    for root_path, _, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(".json"):
                continue
            file_path = os.path.join(root_path, file)
            kv_for_file = get_kvs_for_file(file_path)
            kvs.update(kv_for_file)
    return kvs


def find_english_phrases(text):
    # 正则表达式匹配包含空格的连续英文字母
    pattern = r"[A-Za-z]+(?:\s+[A-Za-z\-]+)*"
    matches = re.findall(pattern, text)
    return matches
