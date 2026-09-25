from __future__ import annotations
 
import argparse
import logging
import re
import sys
from pathlib import Path
from typing import List
 
 
def build_parser() -> argparse.ArgumentParser:
    """Day05のCLI引数を定義します（質問文）。"""
    p = argparse.ArgumentParser(prog="day05")
    p.add_argument("--question", required=True)
    return p
 
 
def _validate_args(args: argparse.Namespace) -> None:
    """引数の簡易バリデーションを行います（入力不備は exit code=2）。"""
    if not args.question:
        raise ValueError("--question is required")
 
 
def answer_with_rag(question: str) -> str:
    """RAGで質問に回答し、指定フォーマットのテキストを返します。
 
    この関数を実装すると、`python -m day05.app --question ...` が動くようになります。
 
    要件（READMEの出力フォーマット）：
    - 標準出力に次の形で出すための文字列を返す
      1) `Answer:` 行
      2) `Sources:` 行
      3) `- <URL or ファイル名> (excerpt: "...")` を最低1件（ヒットなしなら `- (none)`）
 
    実装ガイド：
    - `day05/data/` 配下の `.txt` を読み込み、検索対象とする
    - 最初は単純なキーワード検索でもOK（高品質でなくてよい）
    - ヒットがない場合の挙動を必ず実装する
    """
    data_dir = Path(__file__).resolve().parent / "data"
    documents = sorted(data_dir.glob("*.txt"))
    if not documents:
        raise FileNotFoundError(f"No .txt documents found in {data_dir}")
 
    def terms(text: str) -> set[str]:
        # Japanese text usually has no spaces, so compare overlapping character
        # bigrams as well as ordinary words. Ignore whitespace and punctuation.
        normalized = re.sub(r"[^\wぁ-んァ-ヶ一-龠ー]+", " ", text.lower())
        result: set[str] = set()
        for part in normalized.split():
            if re.fullmatch(r"[ぁ-んァ-ヶ一-龠ー]+", part):
                if len(part) == 1:
                    result.add(part)
                else:
                    result.update(part[i : i + 2] for i in range(len(part) - 1))
            else:
                result.add(part)
        return result
 
    question_terms = terms(question)
    matches: list[tuple[int, str, str]] = []
    for path in documents:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        # Each non-empty line is a small retrieval chunk with its own citation.
        for line in content.splitlines():
            chunk = line.strip()
            if not chunk or chunk.startswith("#") or chunk.startswith("Source:") or chunk.startswith("License:"):
                continue
            score = len(question_terms & terms(chunk))
            if score:
                matches.append((score, path.name, chunk))
 
    if not matches:
        return "Answer: 該当する根拠が見つかりませんでした。質問を言い換えるか、別の資料を追加してください。\nSources:\n- (none)"
 
    matches.sort(key=lambda item: (-item[0], item[1], item[2]))
    selected = matches[:3]
    answer = " ".join(chunk for _, _, chunk in selected)
    sources = "\n".join(
        f'- {filename} (excerpt: "{excerpt.replace(chr(34), chr(39))}")'
        for _, filename, excerpt in selected
    )
    return f"Answer: {answer}\nSources:\n{sources}"
 
 
def main(argv: List[str] | None = None) -> int:
    """CLIのエントリポイントです。
 
    受講者は `answer_with_rag()` を実装します。
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)
 
    try:
        _validate_args(args)
    except Exception as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 2
 
    try:
        out = answer_with_rag(args.question)
        print(out)
        return 0
    except NotImplementedError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 1
    except Exception as e:
        logging.error("%s", e)
        print(str(e), file=sys.stderr)
        return 1
 
 
if __name__ == "__main__":
    raise SystemExit(main())