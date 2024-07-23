# Translation project for gakumas generic strings translation

## Introduction

- translated files (json map) are placed in `translated` folder, with corresponding file name as `gakumas-generic-source-strings/data`
  - if the original folder changes structure, so will the strings in corresponding files in `translated`
- can generate untranslated strings in `working/todo`
- can apply translated strings in `new` to `translated`, regardless of folder structure in `new` folder
- can pretranslate files (jp-> dest lang, default to zh) in `todo` folder and save in `working/new` folder with `-pretranslated` identifier
  - should respect terms (dynamically renders terms in `terms.json` to prompts)

Should treat strings in `.split.json` and `.json` slightly differently

## Commands

- `make update`: update files contents in `translated` folder
- `make apply`: apply files in working
- `make gen-todo`: gen untranslated strings
- `make check`: check if files in `translated` is valid
- `make arrange`: arrange files in `translated` according to strings belongings in `gakumas-generic-source-strings/data`
- `make pretranslate`: pretranslate files in `working/todo` and save in `working/new`

## Example

files in `gakumas-generic-source-strings/data`: `default.json`, `default.split.json`
format are json arrays

```
// gakumas-generic-source-strings/data/default.json
["AP不足","AP全回復","AP回復","AP回復アイテム"]
// gakumas-generic-source-strings/data/default.split.json
["[__split__]アイドル選択","[__split__]サポート選択","[__split__]メモリー選択","[__split__]開始確認"]
```

Supposing `translated` folder contains

```
// /translated/default.json
{"AP不足":"AP不足"}
// gakumas-generic-source-strings/data/default.split.json
{"[__split__]アイドル選択":"[__split__]偶像选择"}
```

### make gen-todo

files are generated in `working/todo`

```
// working/todo/default.json
{"AP全回復":"","AP回復":"","AP回復アイテム":""}
// working/todo/default.split.json
{"[__split__]サポート選択":[__split__],"[__split__]メモリー選択":"[__split__]","[__split__]開始確認":"[__split__]"}
```

### make pretranslate

Will translate files in `working/todo` and save in `working/new`

```
// working/new/default-pretranslated.json
{"AP全回復":"AP全回复","AP回復":"AP回复","AP回復アイテム":"AP回复道具"}
// working/new/default.split.json
{"[__split__]サポート選択":"[__split__]支援选择"","[__split__]メモリー選択":"[__split__]回忆选择","[__split__]開始確認":"[__split__]开始确认"}
```

### make apply

Will apply the files in `working/new` to `translated`

```
// translated/default.json
{"AP不足":"AP不足","AP全回復":"AP全回复","AP回復":"AP回复","AP回復アイテム":"AP回复道具"}
// working/default.split.json
{"[__split__]アイドル選択":"[__split__]偶像选择","[__split__]サポート選択":"[__split__]支援选择"","[__split__]メモリー選択":"[__split__]回忆选择","[__split__]開始確認":"[__split__]开始确认"}
```

### make arrange

arrange strings in `translated` folder according to `gakumas-generic-source-strings/data`

Supposing `gakumas-generic-source-strings/data` is now changed to:

```
// gakumas-generic-source-strings/data/default.json
["AP全回復","AP回復","AP回復アイテム"]
// gakumas-generic-source-strings/data/default-1.json
["AP不足"]
// gakumas-generic-source-strings/data/default.split.json
["[__split__]サポート選択","[__split__]メモリー選択","[__split__]開始確認"]
// gakumas-generic-source-strings/data/default-1.split.json
["[__split__]アイドル選択"]
```

After running `make arrange`

The files in translated should follow its pattern and change to

```
// translated/default.json
{"AP全回復":"AP全回复","AP回復":"AP回复","AP回復アイテム":"AP回复道具"}
// translated/default-1.json
{"AP不足":"AP不足"}
// translated/default.split.json
{"[__split__]サポート選択":"[__split__]支援选择","[__split__]メモリー選択":"[__split__]回忆选择","[__split__]開始確認":"[__split__]开始确认"}
// translated/default-1.split.json
{"[__split__]アイドル選択":"[__split__]偶像选择"}
```

## TODO

- [ ] support `terms.json`
- [ ] backup `translated` before applying
