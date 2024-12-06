import unittest
from unittest.mock import patch, MagicMock
import requests
from app.main import get_long_url, create_short_url, redirect_page, main
from app.main import os as main_os


class TestStreamlitApp(unittest.TestCase):

    @patch("app.main.os.environ.get")
    def test_missing_api_env_var(self, mock_environ_get):
        mock_environ_get.return_value = None
        print(main_os.environ.get("API_ENDPOINT"))
        with patch("app.main.st.error") as mock_error:
            main()

            mock_error.assert_called_with(
                "missing .env file, please contact the developer or deploy your own backend!"
            )

    @patch("app.main.requests.get")
    def test_get_long_url_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"long_url": "https://example.com"}
        mock_get.return_value = mock_response

        result = get_long_url("abc123")
        self.assertEqual(result, "https://example.com")

    @patch("app.main.requests.get")
    def test_get_long_url_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("API error")

        with patch("app.main.st.error") as mock_error:
            result = get_long_url("abc123")
            self.assertIsNone(result)
            mock_error.assert_called_once_with("Error fetching long URL: API error")

    @patch("app.main.requests.post")
    def test_create_short_url_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"short_url": "abc123"}
        mock_post.return_value = mock_response

        result = create_short_url("https://example.com")
        self.assertEqual(result, "abc123")

    @patch("app.main.requests.post")
    def test_create_short_url_failure(self, mock_post):
        mock_post.side_effect = requests.RequestException("API error")

        with patch("app.main.st.error") as mock_error:
            result = create_short_url("https://example.com")
            self.assertIsNone(result)
            mock_error.assert_called_once_with("Error creating short URL: API error")

    @patch("app.main.st.markdown")
    @patch("app.main.st.page_link")
    def test_redirect_page(self, mock_page_link, mock_markdown):
        redirect_page("https://example.com")
        mock_markdown.assert_any_call(
            '\n        <meta http-equiv="refresh" content="0; url=https://example.com">\n    ',
            unsafe_allow_html=True,
        )
        mock_markdown.assert_any_call("If you are not redirected automatically, click below")

    @patch("app.main.st.query_params", {"go": "abc123"})
    @patch("app.main.get_long_url")
    @patch("app.main.redirect_page")
    @patch("app.main.st.text")  # Add this line
    def test_main_with_go_param(self, mock_st_text, mock_redirect_page, mock_get_long_url):
        mock_get_long_url.return_value = "https://example.com"
        main()
        mock_st_text.assert_called_with("Short path is abc123")
        mock_get_long_url.assert_called_once_with("abc123")
        mock_redirect_page.assert_called_once_with("https://example.com")

    @patch("app.main.st.query_params", {})
    @patch("app.main.st.text_input")
    @patch("app.main.create_short_url")
    def test_main_without_go_param(self, mock_create_short_url, mock_text_input):
        mock_text_input.return_value = "https://example.com"
        mock_create_short_url.return_value = "abc123"

        with patch("app.main.st.success") as mock_success:
            main()
            mock_success.assert_called_once_with(
                "Here's your new shiny short URL! "
                "[localhost:8501/?go=abc123](http://localhost:8501/?go=abc123)"
            )


if __name__ == "__main__":
    unittest.main()
