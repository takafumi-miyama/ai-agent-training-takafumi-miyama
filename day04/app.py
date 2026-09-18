from __future__ import annotations
 
import argparse
import logging
import os
import sys
from typing import List
 
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.tools import tool
 
 
def build_parser() -> argparse.ArgumentParser:
    """Day04のCLI引数を定義します（ユーザー入力テキスト）。"""
    p = argparse.ArgumentParser(prog="day04")
    p.add_argument("--text", required=True)
    return p
 
 
def _validate_args(args: argparse.Namespace) -> None:
    """引数の簡易バリデーションを行います（入力不備は exit code=2）。"""
    if not args.text:
        raise ValueError("--text is required")
 
@tool
def add(a: int, b: int) -> int:
    """2つの整数を足します。"""
    logging.info("Tool called: add(a=%s, b=%s)", a, b)
    return a + b
 
def run_chain(text: str) -> str:
    """LangChain + Tool calling を使って回答（文字列）を返します。
 
    この関数を実装すると、`python -m day04.app --text ...` が動くようになります。
 
    要件（READMEの受け入れ基準）：
    - `today` または `add` のツールを1つ実装し、LLMから1回以上呼び出す
    - ツール引数のバリデーションを入れる（不正なら実行しない）
    - ツール失敗時は安全に失敗する（例外でOK。mainがexit code=1にする）
 
    ヒント：
    - まずはツールをPython関数として作り、ログで「呼ばれた」ことを確認
    - 次にLLM側のプロンプトで「必要ならツールを使う」よう誘導
    """
    load_dotenv()
 
    region = os.getenv("AWS_REGION")
    model_id = os.getenv("BEDROCK_MODEL_ID")
 
    if not region:
        raise ValueError("AWS_REGION is required")
 
    if not model_id:
        raise ValueError("BEDROCK_MODEL_ID is required")
 
    llm = ChatBedrock(
        model_id=model_id,
        region_name=region,
    )
 
    llm_with_tools = llm.bind_tools([add])
 
    prompt = f"""
あなたは計算を手伝うアシスタントです。
 
足し算が必要な場合は、必ずaddツールを使用してください。
 
ユーザーの質問:
{text}
"""
 
    response = llm_with_tools.invoke(prompt)
 
    if not response.tool_calls:
        return response.content
 
    tool_call = response.tool_calls[0]
 
    if tool_call["name"] != "add":
        raise ValueError(f"Unexpected tool: {tool_call['name']}")
 
    result = add.invoke(tool_call["args"])
 
    final_response = llm.invoke(
        [
            ("user", prompt),
            response,
            {
                "role": "tool",
                "content": str(result),
                "tool_call_id": tool_call["id"],
            },
        ]
    )
 
    return final_response.content
 
 
def main(argv: List[str] | None = None) -> int:
    """CLIのエントリポイントです。
 
    受講者は `run_chain()` の実装に集中し、ここは原則編集しません。
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
        out = run_chain(args.text)
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