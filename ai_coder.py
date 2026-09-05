import os
import json
import anthropic

event_path = os.environ.get("GITHUB_EVENT_PATH")
with open(event_path, "r") as f:
    event_data = json.load(f)

client = anthropic.Anthropic()

# 画面に表示されている最新モデルを指定
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    system="あなたは優秀なプログラマーです。ユーザーのリクエストに基づいてPythonコードのみを出力してください。解説やMarkdownのコードブロック(```)は含めず、純粋なコードのみを返してください。",
    messages=[
        {"role": "user", "content": f"タイトル: {event_data['issue']['title']}\n詳細: {event_data['issue']['body'] or ''}"}
    ]
)

generated_code = response.content[0].text.replace("```python", "").replace("```", "").strip()
with open("generated_output.py", "w") as f:
    f.write(generated_code)

print("Claude AI coding completed.")