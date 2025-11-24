import os
from typing import List, Dict, Any

from openai import OpenAI

# Model for your project
OPENAI_MODEL = "gpt-5-mini"


def openai_client() -> OpenAI:
    """
    Create an OpenAI client using the OPENAI_API_KEY environment variable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Please set it in your environment."
        )
    return OpenAI(api_key=api_key)


def summarize_text(text: str, kind: str = "task") -> str:
    """
    Summarize the given text into a short actionable suggestion or title.

    kind is used only to tailor the system prompt (e.g., 'task', 'note', 'chat').
    """
    client = openai_client()

    system_prompt = (
        f"You help summarize a {kind}. "
        "Given the user's message, respond with a short, clear suggestion or summary "
        "in 1–2 sentences, suitable for a busy student."
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        reasoning_effort="minimal",
        max_completion_tokens=256,
    )

    content = response.choices[0].message.content
    return content.strip() if content else "(no response)"


def suggest_next_tasks(tasks: List[Dict[str, Any]]) -> str:
    """
    Given a list of task dicts, ask the model what the user should work on next.
    """
    client = openai_client()

    system_prompt = (
        "You are a task-prioritization assistant for a college student. "
        "Given their task list (with titles, due dates, and completion status), "
        "suggest what they should focus on next and why, in 2–4 sentences."
    )

    user_message = f"Here are my tasks (as JSON-like dicts):\n{tasks}"

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        reasoning_effort="minimal",
        max_completion_tokens=512,
    )

    content = response.choices[0].message.content
    return content.strip() if content else "(no response)"


def chat_loop() -> None:
    """
    Simple terminal REPL for chatting with the AI.

    Your CLI calls this when you run:
        python -m final_project.cli chat loop
    """
    print("Welcome to final_project chat. Type 'exit' to quit.")

    while True:
        try:
            msg = input("chat> ").strip()
        except EOFError:
            break

        if msg.lower() in {"exit", "quit"}:
            break
        if not msg:
            continue

        try:
            reply = summarize_text(msg, kind="chat")
            print("AI:", reply)
        except Exception as e:
            print("AI error:", e)
