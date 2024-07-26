import os, json
from typing import Dict, List

# normalize each json file in the directory
# if the directory is in the order_exclude_dir, then do not sort the data
# otherwise, sort the data in ascending order

def normalize_strings(dir: str, order_exclude_dir: List[str]):
    for i in range(len(order_exclude_dir)):
        order_exclude_dir[i] = os.path.normpath(order_exclude_dir[i])

    for root_dir, _, files in os.walk(dir):

        for file in files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(root_dir, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = data.keys()
            with open(os.path.join(root_dir, file), "w", encoding="utf-8") as f:
                if os.path.normpath(root_dir) in order_exclude_dir:
                    json.dump(list(data), f, ensure_ascii=False, indent=4)
                else:
                    json.dump(sorted(data), f, ensure_ascii=False, indent=4)


def main():
    normalize_strings("./translated", [])

if __name__ == "__main__":
    main()
