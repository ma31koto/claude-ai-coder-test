import os
import json
import anthropic

# イベントデータの読み込み
event_path = os.environ.get("GITHUB_EVENT_PATH")
with open(event_path, "r") as f:
    event_data = json.load(f)

# Claude公式クライアントの初期化
client = anthropic.Anthropic()

# 最新のHaikuモデルに変更
response = client.messages.create(
    model="claude-3-5-haiku-latest",
    max_tokens=1000,
    system="あなたは優秀なプログラマーです。ユーザーのリクエストに基づいてPythonコードのみを出力してください。解説やMarkdownのコードブロック(```)は含めず、純粋なコードのみを返してください。",
    messages=[
        {"role": "user", "content": f"タイトル: {event_data['issue']['title']}\n詳細: {event_data['issue']['body'] or ''}"}
    ]
)

# 生成されたコードの保存
generated_code = response.content[0].text.replace("```python", "").replace("```", "").strip()
with open("generated_output.py", "w") as f:
    f.write(generated_code)

print("Claude AI coding completed.")