import os
from openai import OpenAI

MODEL = "gpt-5-mini"

def main() -> None:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG_ID"),
    )

    paragraphs = [
        "Write a detailed research paper discussing the economic impact of electric vehicles on the global oil industry. Include data analysis, charts, and forecasts for the next decade.",
        "Develop a new marketing strategy for a local coffee shop that focuses on social media outreach, loyalty programs, and community engagement events to increase foot traffic."
    ]

    print("Summarizing tasks...\n")

    for i, text in enumerate(paragraphs, start=1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You summarize tasks into short phrases."},
                {"role": "user", "content": f"Summarize this task as a short phrase: {text}"},
            ],
        )
        summary = response.choices[0].message.content.strip()
        print(f"Task {i} summary: {summary}")

if __name__ == "__main__":
    main()
