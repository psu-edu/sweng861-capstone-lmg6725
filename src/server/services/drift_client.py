import requests
import os

DRIFT_URL = "http://ec2-13-59-66-30.us-east-2.compute.amazonaws.com:8091/v1/chat/completions"

def ask_drift(prompt, api_key):
    print("calling drift")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "drift",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        DRIFT_URL,
        json=payload,
        headers=headers
    )
    # Check if the response was successful
    response.raise_for_status()
    return response.json()