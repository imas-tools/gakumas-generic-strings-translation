import os, json
from utils import get_kvs_for_dir, translation_dir, source_strings_dir, yield_string


def arrange():
    all_kvs = get_kvs_for_dir(translation_dir)
    # filename -> {key -> value}
    kvs_to_update: dict[str, dict[str, str]] = {}

    # update
    # init empty kvs_to_update filename
    for root_path, _, files in os.walk(translation_dir):
        for file in files:
            if not file.endswith(".json"):
                continue
            file_path = os.path.join(root_path, file)
            kvs_to_update[file_path] = {}
            
    # arrange kvs
    for root_path, _, files in os.walk(source_strings_dir):
        for file in files:
            if not file.endswith(".json"):
                continue
            file_path = os.path.join(root_path, file)
            rel_path = os.path.relpath(file_path, source_strings_dir)
            dest_file_path = os.path.join(translation_dir, rel_path)
            kvs_to_update.setdefault(dest_file_path, {})
                
            for string, _ in yield_string(file_path):
                if string not in all_kvs:
                    continue
                kvs_to_update[dest_file_path][string] = all_kvs[string]
    
    # write kvs
    for filename, kvs in kvs_to_update.items():
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(kvs, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    arrange()