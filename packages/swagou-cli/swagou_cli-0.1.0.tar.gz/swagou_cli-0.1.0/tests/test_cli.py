"""Unit tests for the CLI module."""

import os
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from swagou.cli import app


# Setup the CLI runner
runner = CliRunner()


class TestCliFilter:
    """Tests for the filter command in the CLI."""

    @patch("swagou.cli.filter_openapi_schema")
    def test_filter_command_basic(self, mock_filter):
        """Test the basic filter command."""
        # Mock the filter_openapi_schema function to return a simple string
        mock_filter.return_value = "filtered schema"

        # Run the command
        result = runner.invoke(app, ["--input", "test.yaml", "--get", "/api/posts/"])

        # Check that the command ran successfully
        assert result.exit_code == 0

        # Check that filter_openapi_schema was called with the correct arguments
        mock_filter.assert_called_once_with(
            input_source="test.yaml",
            get_paths=["/api/posts/"],
            post_paths=[],
            patch_paths=[],
            delete_paths=[],
            all_paths=[],
            headers=None,
            cookies=None,
            tags=None,
        )

        # Check that the output is correct
        assert "filtered schema" in result.stdout

    @patch("swagou.cli.filter_openapi_schema")
    def test_filter_command_with_output_file(self, mock_filter):
        """Test the filter command with an output file."""
        # Mock the filter_openapi_schema function to return a simple string
        mock_filter.return_value = "filtered schema"

        # Create a temporary file path
        output_file = "test_output.yaml"

        try:
            # Run the command
            result = runner.invoke(
                app,
                [
                    "--input",
                    "test.yaml",
                    "--get",
                    "/api/posts/",
                    "--output",
                    output_file,
                ],
            )

            # Check that the command ran successfully
            assert result.exit_code == 0

            # Check that filter_openapi_schema was called with the correct arguments
            mock_filter.assert_called_once_with(
                input_source="test.yaml",
                get_paths=["/api/posts/"],
                post_paths=[],
                patch_paths=[],
                delete_paths=[],
                all_paths=[],
                headers=None,
                cookies=None,
                tags=None,
            )

            # Check that the output message is correct
            assert f"Filtered schema written to {output_file}" in result.stdout

            # Check that the file was created (mock doesn't actually create it)
            # In a real test, we would check the file content
        finally:
            # Clean up (in case the file was actually created)
            if os.path.exists(output_file):
                os.remove(output_file)

    @patch("swagou.cli.filter_openapi_schema")
    def test_filter_command_with_multiple_paths(self, mock_filter):
        """Test the filter command with multiple paths."""
        # Mock the filter_openapi_schema function to return a simple string
        mock_filter.return_value = "filtered schema"

        # Run the command with multiple paths
        result = runner.invoke(
            app,
            [
                "--input",
                "test.yaml",
                "--get",
                "/api/posts/",
                "--get",
                "/api/users/",
                "--post",
                "/api/comments/",
                "--all",
                "/api/auth/*",
            ],
        )

        # Check that the command ran successfully
        assert result.exit_code == 0

        # Check that filter_openapi_schema was called with the correct arguments
        mock_filter.assert_called_once_with(
            input_source="test.yaml",
            get_paths=["/api/posts/", "/api/users/"],
            post_paths=["/api/comments/"],
            patch_paths=[],
            delete_paths=[],
            all_paths=["/api/auth/*"],
            headers=None,
            cookies=None,
            tags=None,
        )

    @patch("swagou.cli.filter_openapi_schema")
    def test_filter_command_with_headers_and_cookies(self, mock_filter):
        """Test the filter command with headers and cookies."""
        # Mock the filter_openapi_schema function to return a simple string
        mock_filter.return_value = "filtered schema"

        # Run the command with headers and cookies
        result = runner.invoke(
            app,
            [
                "--input",
                "https://example.com/api/schema",
                "--get",
                "/api/posts/",
                "--header",
                "Authorization: Bearer token",
                "--cookie",
                "sessionid: abc123",
            ],
        )

        # Check that the command ran successfully
        assert result.exit_code == 0

        # Check that filter_openapi_schema was called with the correct arguments
        mock_filter.assert_called_once_with(
            input_source="https://example.com/api/schema",
            get_paths=["/api/posts/"],
            post_paths=[],
            patch_paths=[],
            delete_paths=[],
            all_paths=[],
            headers=["Authorization: Bearer token"],
            cookies=["sessionid: abc123"],
            tags=None,
        )

    @patch("swagou.cli.filter_openapi_schema")
    def test_filter_command_with_tags(self, mock_filter):
        """Test the filter command with tags."""
        # Mock the filter_openapi_schema function to return a simple string
        mock_filter.return_value = "filtered schema"

        # Run the command with tags
        result = runner.invoke(
            app,
            [
                "--input",
                "test.yaml",
                "--get",
                "/api/posts/",
                "--tags",
                "posts",
                "--tags",
                "users",
            ],
        )

        # Check that the command ran successfully
        assert result.exit_code == 0

        # Check that filter_openapi_schema was called with the correct arguments
        mock_filter.assert_called_once_with(
            input_source="test.yaml",
            get_paths=["/api/posts/"],
            post_paths=[],
            patch_paths=[],
            delete_paths=[],
            all_paths=[],
            headers=None,
            cookies=None,
            tags=["posts", "users"],
        )

    @patch("swagou.cli.filter_openapi_schema")
    def test_filter_command_error_handling(self, mock_filter):
        """Test error handling in the filter command."""
        # Mock the filter_openapi_schema function to raise an exception
        mock_filter.side_effect = Exception("Test error")

        # Run the command
        result = runner.invoke(app, ["--input", "test.yaml", "--get", "/api/posts/"])

        # Check that the command failed
        assert result.exit_code == 1

        # Check that the error message is displayed
        assert "Error: Test error" in result.stdout
