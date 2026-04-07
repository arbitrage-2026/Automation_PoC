import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_root_cause(data):
    prompt = f"""
    Analyze telemetry:
    {data}

    Return JSON:
    root_cause, confidence, action
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response["choices"][0]["message"]["content"]

    # Simple fallback mapping
    if data["cpu"] > 85:
        return {"root_cause": "High CPU", "confidence": 90, "action": "FixCPU"}
    if data["disk"] < 10:
        return {"root_cause": "Low Disk", "confidence": 95, "action": "FixDisk"}

    return {"root_cause": "Unknown", "confidence": 50, "action": "None"}