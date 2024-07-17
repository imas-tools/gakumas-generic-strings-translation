import json

dest_lang = "simplified Chinese"
example_input = [
    "AP不足",
    "AP全回復",
    "AP回復",
    "AP回復アイテム",
    "[split]アイドル選択",
    "[split]サポート選択",
    "[split]メモリー選択",
    "[split]開始確認",
]
example_output = {
    "AP不足": "AP不足",
    "AP全回復": "AP全恢复",
    "AP回復": "AP恢复",
    "AP回復アイテム": "AP恢复道具",
    "[split]アイドル選択": "[split]偶像选择",
    "[split]サポート選択": "[split]支援选择",
    "[split]メモリー選択": "[split]回忆选择",
    "[split]開始確認": "[split]开始确认",
}

base_system_prompt =  f"""You are working for a localization service company that translates game texts from Japanese to {dest_lang}.

Requirements:
1. You will be given a json array containing the game texts in Japanese. 
2. Each text may start with an identifier [split] marking that this text is a part of a longer text. And if the text starts with the identifier, the corresponding translation shall contain the identifier too
3. You should return the translation in json map array with scheme: {{ [original text]: [translation] }}"""

term_table_path = "./etc/terms.json"
with open(term_table_path, "r", encoding="utf-8") as f:
    term_table = json.load(f)

def gen_term_slice_from_term_table(user_prompt: str):
    term_table_slice = {}
    for term in term_table:
        if term in user_prompt:
            term_table_slice[term] = term_table[term]
    return term_table_slice

def gen_system_prompt(user_prompt: str):
    term_slice = gen_term_slice_from_term_table(user_prompt)
    term_slice_prompt_snippets = f"""4. You may use the following terms for translation: {term_slice}""" if term_slice else ""
    return base_system_prompt + term_slice_prompt_snippets + f"""
Example Input:
{example_input}

Example Output:
{example_output}
"""
