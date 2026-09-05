import os
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

event_path = os.environ.get("GITHUB_EVENT_PATH")
with open(event_path, "r") as f:
    event_data = json.load(f)

issue_title = event_data["issue"]["title"]
issue_body = event_data["issue"]["body"] or ""

# Claudeモデルの指定（Anthropic公式ライブラリ）
llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なプログラマーです。ユーザーのリクエストに基づいてPythonコードのみを出力してください。解説やMarkdownのコードブロック(```)は含めず、純粋なコードのみを返してください。"),
    ("user", "タイトル: {title}\n詳細: {body}")
])

chain = prompt | llm
res = chain.invoke({"title": issue_title, "body": issue_body}).content

# 返り値の処理
if isinstance(res, list):
    generated_code = "".join([str(item) for item in res])
else:
    generated_code = str(res)

generated_code = generated_code.replace("```python", "").replace("```", "").strip()

with open("generated_output.py", "w") as f:
    f.write(generated_code)

print("Claude AI coding completed.")