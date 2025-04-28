from unittest.mock import patch
from sas_dict.cli import fetch_word_data, main

# Mock data for testing
mock_word_data = [
    {
        "meanings": [
            {
                "partOfSpeech": "noun",
                "definitions": [{"definition": "A mock definition for testing."}],
            }
        ]
    }
]


@patch("sas_dict.cli.fetch_word_data")
def test_fetch_word_data(mock_fetch):
    # Mock the fetch_word_data function
    mock_fetch.return_value = mock_word_data

    # Simulate command-line arguments
    with patch("sys.argv", ["cli.py", "test"]):
        main()

    # Call the function and verify the result
    result = fetch_word_data("test")
    assert result != mock_word_data
    mock_fetch.assert_called_once_with("test")


@patch("sas_dict.cli.fetch_word_data")
@patch("builtins.print")
def test_main_with_valid_word(mock_print, mock_fetch):
    # Mock the fetch_word_data function
    mock_fetch.return_value = mock_word_data

    # Simulate command-line arguments
    with patch("sys.argv", ["cli.py", "test"]):
        main()

    # Verify that the correct output was printed
    mock_print.assert_any_call("Definitions for 'test':")
    mock_print.assert_any_call("\nnoun:")
    mock_print.assert_any_call("- A mock definition for testing.")


@patch("sas_dict.cli.fetch_word_data")
@patch("builtins.print")
def test_main_with_invalid_word(mock_print, mock_fetch):
    # Mock the fetch_word_data function to return None
    mock_fetch.return_value = None

    # Simulate command-line arguments
    with patch("sys.argv", ["cli.py", "invalid"]):
        main()

    # Verify that the correct error message was printed
    mock_print.assert_called_once_with("Could not retrieve definition for 'invalid'.")
