import os, json, warnings
from openai import OpenAI
from typing import cast, List, Dict
from utils import SPLIT_STRING_PREFIX, working_new_dir, working_todo_dir
from prompts import gen_system_prompt


def pretranslate_texts(texts: List[str]) -> Dict[str, str]:
    system_prompt = gen_system_prompt(str(texts))
    client = OpenAI(
        # api_key="",
        # base_url="",
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(texts)},
        ],
        response_format={"type": "json_object"},
    )
    translation_map = cast(Dict[str, str], json.loads(response.choices[0].message.content))  # type: ignore
    if not isinstance(translation_map, dict):
        raise ValueError("Translation map is not a dictionary")
    rtn = {}
    print(translation_map)
    for k, v in translation_map.items():
        if k not in texts:
            warnings.warn(f"Key {k} not in terms")
            continue
        if k.startswith(SPLIT_STRING_PREFIX) and not v.startswith(SPLIT_STRING_PREFIX):
            warnings.warn(
                f"Key {k} starts with {SPLIT_STRING_PREFIX} but value {v} does not"
            )
            continue
        rtn[k] = v
    return rtn


def get_next_batch(
    texts: List[str], max_batch_size: int, translated: Dict[str, str]
) -> List[str]:
    batch = []
    for text in texts:
        if text not in translated:
            batch.append(text)
            if len(batch) == max_batch_size:
                break
    print(
        f"Translated {len(translated)} texts, {len(texts) - len(translated)} texts left"
    )
    return batch


def pretranslate_all_texts(texts: List[str], max_batch_size=50) -> Dict[str, str]:
    result = {}
    while batch := get_next_batch(texts, max_batch_size, result):
        result.update(pretranslate_texts(batch))
    return result

def get_dest_filename(filename: str) -> str:
    splits = filename.split(".")
    splits[0] = f"{splits[0]}_translated"
    return ".".join(splits)

def pretranslate():
    for root_dir, _, files in os.walk(working_todo_dir):
        for file in files:
            relpath = os.path.relpath(
                os.path.join(root_dir, get_dest_filename(file)), working_todo_dir
            )
            destpath = os.path.join(working_new_dir, relpath)
            if file.endswith(".json"):
                with open(os.path.join(root_dir, file), "r", encoding="utf-8") as f:
                    texts = json.load(f)
                    print(f"Pretranslating {len(texts)} texts from {file} to {destpath}...")
                    translated = pretranslate_all_texts(texts)
                    with open(destpath, "w", encoding="utf-8") as f:
                        json.dump(translated, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    pretranslate()
