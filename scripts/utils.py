import os, json, warnings
from typing import Dict, List, cast, Tuple, Generator

SPLIT_STRING_PREFIX = "[split]"

source_strings_dir = "./gakumas-genric-source-strings/data"
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

        if isinstance(content, dict):
            for k, v in content.items():
                if k == v:
                    if v.startswith(SPLIT_STRING_PREFIX):
                        # warnings.warn(
                        #     "Key and value are the same and start with [split], this might be a mistake"
                        # )
                        raise ValueError(
                            "Key and value are the same and start with [split], this might be a mistake"
                        )
                    yield (cast(str, v), False)
                else:
                    if not isinstance(v, str) or not v.startswith(SPLIT_STRING_PREFIX):
                        raise ValueError(
                            f"Invalid split string: {v}, should start with {SPLIT_STRING_PREFIX}"
                        )
                    yield (cast(str, v), True)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, str):
                    yield (cast(str, item), (not item.startswith(SPLIT_STRING_PREFIX)))
                else:
                    raise ValueError("Invalid list item, should be a string")
        else:
            raise TypeError("Unsupported JSON content type")


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
