# Day 01

## 受講者が実装する場所

- `day01/app.py`（基本はこのファイルを編集）

## 目的

- 開発環境のセットアップができる状態にする
- GitHubのPR提出フローに慣れる
- Pythonで小さなCLIを作り、例外/ログ/READMEの書き方を身につける

## ゴール（完了条件）

- READMEどおりに第三者が実行できる
- 入力不備で終了コード `2` になり、標準エラーに分かりやすいメッセージが出る

## 機能要件

### 機能要件

コマンド

- `python -m day01.app` で起動できること（モジュール名は固定）

必須オプション

- `--name`：表示したい名前（文字列、必須）

任意オプション

- `--repeat`：繰り返し回数（整数、デフォルト `1`、1〜10）
- `--format`：出力形式（`text` / `json`、デフォルト `text`）

出力

- `--format text` の場合：標準出力に、指定回数分のテキストを出す
- `--format json` の場合：標準出力にJSONを出す
  - 例：`{"name":"Taro","repeat":2,"outputs":["Hello, Taro","Hello, Taro"]}`

終了コード

- 正常終了：`0`
- 入力不備（未指定、範囲外など）：`2`

ログ

- 実行開始時に、`name` / `repeat` / `format` をINFOで出す
- 例外発生時はERRORで出す

### 受け入れ基準

- `--name` 未指定で終了コード `2`、標準エラーに分かりやすいメッセージが出る
- `--repeat 2` で2行（または2要素）出る
- `--format json` でJSONとしてパース可能な文字列が出る

## 実装タスク

- `day01/app.py` を編集し、機能要件を満たす
- 例外時は標準エラーへメッセージを出し、終了コードを要件どおりにする

## 実行方法

### セットアップ

```bash
# 仮想環境の作成と有効化
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 実行コマンド例

```bash
# 基本的な実行
python -m day01.app --name "Taro"

# 繰り返し回数を指定
python -m day01.app --name "Taro" --repeat 3

# JSON形式で出力
python -m day01.app --name "Taro" --repeat 2 --format json
```

### 期待する出力例

```
# --name "Taro" の場合
Hello, Taro

# --name "Taro" --repeat 2 --format json の場合
{"name": "Taro", "repeat": 2, "outputs": ["Hello, Taro", "Hello, Taro"]}
```

---

**以下は受講者が記入してください**

- 追加で確認した入力例：
--name に日本語や記号を指定して正常に出力されることを確認した。
--name に " を文字列として渡そうとしたがうまくできなかった。

- 発生したエラーと対処：
--repeat 11 を指定したところ、1～10の範囲外のためエラーになった。--repeat 10 に修正して正常に実行できることを確認した。

## 提出物

- `day01/app.py`
- `day01/README.md`

## セルフレビュー

- 正常系：`--name Taro` で期待どおりに表示される
- 異常系：`--name` 未指定でエラーになり、メッセージが分かりやすい
- 境界：`--name` に長い文字列や記号を入れても壊れない
- 再実行：同じ入力で複数回実行しても安定して同じ結果になる

## リサーチメモ（任意）

調べたURLや、理解した要点をメモしてください。

- Python仮想環境（venv等）
プロジェクトごとに専用の仮想環境を作成する必要がある。venvはPython標準の仮想環境作成モジュール。

- 依存管理（requirements/pyprojectの考え方）
Pythonプログラムを動かすには追加のライブラリが必要なことがあり、「このプログラムには何のライブラリが必要なのか」を管理するのが依存管理。
requirements：必要なライブラリ一覧
pyproject：プロジェクトの定義書

- CLIの引数処理（例：argparse等）
ターミナルからPythonプログラムに値を渡し、argparse などを使ってその引数を受け取り・整理・検証する。

- ログ（INFO/ERRORの使い分け）
INFOは通常の処理状況、ERRORはエラー発生時など、重要度に応じてログを使い分ける。

- GitHub：ブランチ作成→PR→修正push
本番ファイルではなく安全な場所で作業を行い、完了後レビュー依頼を送る。作業後や修正後はローカルからリモートに反映する。

## GitHub操作の練習
ブランチ作成、commit、push、PR作成の流れを確認した。