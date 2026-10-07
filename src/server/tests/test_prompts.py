# Test the prompts routes


def test_get_prompts_requires_auth(client):
    response = client.get("/prompts")
    assert response.status_code == 401

def test_create_prompt_requires_auth(client):
    response = client.post(
        "/prompts",
        json={
            "prompt": "What is Python?",
            "response": "Python is a programming language."
        }
    )
    assert response.status_code == 401

def test_get_invalid_prompt(client):
    response = client.get("/prompts/99999")

    # If this route is protected by authentication middleware, an
    # unauthenticated request should be rejected before lookup.
    assert response.status_code in [401, 404]
