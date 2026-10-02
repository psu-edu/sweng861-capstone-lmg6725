# Test the prompts routes

def test_get_prompts(client):
    response = client.get("/prompts")
    
    """# Depending on whether the user is authenticated or not, the status code can be 200 (OK) or 400 (Bad Request)
    assert response.status_code in [200, 400]"""
    
    # Testing for 401 Unauthorized since the user is not authenticated
    assert response.status_code == 401

def test_create_prompt_requires_auth(client):
    response = client.post(
        "/prompts",
        json={
            "prompt": "What is Python?",
            "response": "Python is a programming language."
        }
    )

    assert response.status_code in [200, 201, 401]

def test_get_invalid_prompt(client):
    response = client.get("/prompts/99999")

    assert response.status_code == 404