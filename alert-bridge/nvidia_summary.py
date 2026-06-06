"""
NVIDIA NIM summary placeholder.

Keep this read-only at first:
- summarize alert
- suggest likely causes
- suggest safe next checks
- never auto-run shell commands
"""

import os
from openai import OpenAI


def generate_incident_summary(raw_alert: str, service_name: str) -> str:
    api_key = os.getenv("NVIDIA_API_KEY")
    model = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")

    if not api_key:
        return "NVIDIA_API_KEY not set. AI summary skipped."

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )

    prompt = f"""
You are an IT incident analyst for a small homelab.

Service: {service_name}

Alert:
{raw_alert}

Return:
1. Summary
2. Likely causes
3. Safe next checks
4. What not to touch yet
5. Suggested KB article

Do not recommend destructive commands.
Do not tell the user to expose admin services publicly.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a cautious IT incident analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
