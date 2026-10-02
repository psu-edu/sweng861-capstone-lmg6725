from services.drift_client import ask_drift


def test_ask_drift_returns_json(mocker):

    mock_response = mocker.Mock()

    mock_response.json.return_value = {
        "choices": [{"message": "test"}]
    }

    mock_response.raise_for_status.return_value = None

    mocker.patch(
        "services.drift_client.requests.post",
        return_value=mock_response
    )

    result = ask_drift(
        "hello",
        "apikey"
    )

    assert "choices" in result

def test_ask_drift_calls_requests_post(mocker):

    mock_post = mocker.patch(
        "services.drift_client.requests.post"
    )

    mock_post.return_value.raise_for_status.return_value = None
    mock_post.return_value.json.return_value = {}

    ask_drift(
        "prompt",
        "key"
    )

    mock_post.assert_called_once()