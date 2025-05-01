"""Unit tests for the filter module."""

import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest
import yaml

from swagou.filter import (
    filter_openapi_schema,
    load_schema,
    filter_schema,
    collect_references,
    extract_referenced_components,
)


# Test data
SAMPLE_SCHEMA = {
    "openapi": "3.0.0",
    "info": {"title": "Test API", "version": "1.0.0"},
    "paths": {
        "/api/posts/": {
            "get": {
                "summary": "List all posts",
                "tags": ["posts"],
                "responses": {
                    "200": {
                        "description": "A list of posts",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Post"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "summary": "Create a new post",
                "tags": ["posts"],
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PostCreate"}}},
                },
                "responses": {
                    "201": {
                        "description": "Post created successfully",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Post"}}},
                    }
                },
            },
        },
        "/api/users/": {
            "get": {
                "summary": "List all users",
                "tags": ["users"],
                "responses": {
                    "200": {
                        "description": "A list of users",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"},
                                }
                            }
                        },
                    }
                },
            },
        },
    },
    "components": {
        "schemas": {
            "Post": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "author": {"$ref": "#/components/schemas/User"},
                },
                "required": ["id", "title", "content", "author"],
            },
            "PostCreate": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["title", "content"],
            },
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                },
                "required": ["id", "username", "email"],
            },
        }
    },
}


class TestLoadSchema:
    """Tests for the load_schema function."""

    def test_load_schema_from_file(self):
        """Test loading a schema from a file."""
        # Create a temporary file with the sample schema
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            yaml.dump(SAMPLE_SCHEMA, temp_file)
            temp_file_path = temp_file.name

        try:
            # Load the schema from the file
            schema = load_schema(temp_file_path)

            # Check that the schema was loaded correctly
            assert schema["openapi"] == "3.0.0"
            assert schema["info"]["title"] == "Test API"
            assert "/api/posts/" in schema["paths"]
            assert "/api/users/" in schema["paths"]
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    @patch("httpx.get")
    def test_load_schema_from_url(self, mock_get):
        """Test loading a schema from a URL."""
        # Mock the response from httpx.get
        mock_response = MagicMock()
        mock_response.text = yaml.dump(SAMPLE_SCHEMA)
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Load the schema from a URL
        schema = load_schema("https://example.com/api/schema")

        # Check that the schema was loaded correctly
        assert schema["openapi"] == "3.0.0"
        assert schema["info"]["title"] == "Test API"
        assert "/api/posts/" in schema["paths"]
        assert "/api/users/" in schema["paths"]

        # Check that httpx.get was called with the correct arguments
        mock_get.assert_called_once_with(
            "https://example.com/api/schema",
            headers={},
            cookies={},
            follow_redirects=True,
        )

    @patch("httpx.get")
    def test_load_schema_with_headers_and_cookies(self, mock_get):
        """Test loading a schema with headers and cookies."""
        # Mock the response from httpx.get
        mock_response = MagicMock()
        mock_response.text = yaml.dump(SAMPLE_SCHEMA)
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Load the schema from a URL with headers and cookies
        schema = load_schema(
            "https://example.com/api/schema",
            headers=["Authorization: Bearer token"],
            cookies=["sessionid: abc123"],
        )

        # Check that httpx.get was called with the correct arguments
        mock_get.assert_called_once_with(
            "https://example.com/api/schema",
            headers={"Authorization": "Bearer token"},
            cookies={"sessionid": "abc123"},
            follow_redirects=True,
        )


class TestFilterSchema:
    """Tests for the filter_schema function."""

    def test_filter_by_get_path(self):
        """Test filtering by GET path."""
        filtered = filter_schema(
            SAMPLE_SCHEMA,
            get_paths=["/api/posts/"],
            post_paths=[],
            patch_paths=[],
            delete_paths=[],
            all_paths=[],
            tags=[],
        )

        # Check that only the GET method for /api/posts/ is included
        assert "/api/posts/" in filtered["paths"]
        assert "get" in filtered["paths"]["/api/posts/"]
        assert "post" not in filtered["paths"]["/api/posts/"]
        assert "/api/users/" not in filtered["paths"]

        # Check that referenced components are included
        assert "schemas" in filtered["components"]
        assert "Post" in filtered["components"]["schemas"]
        assert "User" in filtered["components"]["schemas"]  # Referenced by Post

    def test_filter_by_post_path(self):
        """Test filtering by POST path."""
        filtered = filter_schema(
            SAMPLE_SCHEMA,
            get_paths=[],
            post_paths=["/api/posts/"],
            patch_paths=[],
            delete_paths=[],
            all_paths=[],
            tags=[],
        )

        # Check that only the POST method for /api/posts/ is included
        assert "/api/posts/" in filtered["paths"]
        assert "post" in filtered["paths"]["/api/posts/"]
        assert "get" not in filtered["paths"]["/api/posts/"]
        assert "/api/users/" not in filtered["paths"]

        # Check that referenced components are included
        assert "schemas" in filtered["components"]
        assert "Post" in filtered["components"]["schemas"]
        assert "PostCreate" in filtered["components"]["schemas"]
        assert "User" in filtered["components"]["schemas"]  # Referenced by Post

    def test_filter_by_all_paths(self):
        """Test filtering by all paths."""
        filtered = filter_schema(
            SAMPLE_SCHEMA,
            get_paths=[],
            post_paths=[],
            patch_paths=[],
            delete_paths=[],
            all_paths=["/api/users/"],
            tags=[],
        )

        # Check that all methods for /api/users/ are included
        assert "/api/users/" in filtered["paths"]
        assert "get" in filtered["paths"]["/api/users/"]
        assert "/api/posts/" not in filtered["paths"]

        # Check that referenced components are included
        assert "schemas" in filtered["components"]
        assert "User" in filtered["components"]["schemas"]

    def test_filter_by_tags(self):
        """Test filtering by tags."""
        filtered = filter_schema(
            SAMPLE_SCHEMA,
            get_paths=["/api/posts/", "/api/users/"],
            post_paths=[],
            patch_paths=[],
            delete_paths=[],
            all_paths=[],
            tags=["users"],
        )

        # Check that only endpoints with the "users" tag are included
        assert "/api/users/" in filtered["paths"]
        assert "get" in filtered["paths"]["/api/users/"]
        assert "/api/posts/" not in filtered["paths"]

        # Check that referenced components are included
        assert "schemas" in filtered["components"]
        assert "User" in filtered["components"]["schemas"]

    def test_filter_with_wildcard(self):
        """Test filtering with wildcard patterns."""
        filtered = filter_schema(
            SAMPLE_SCHEMA,
            get_paths=["/api/*/"],
            post_paths=[],
            patch_paths=[],
            delete_paths=[],
            all_paths=[],
            tags=[],
        )

        # Check that GET methods for all matching paths are included
        assert "/api/posts/" in filtered["paths"]
        assert "get" in filtered["paths"]["/api/posts/"]
        assert "post" not in filtered["paths"]["/api/posts/"]
        assert "/api/users/" in filtered["paths"]
        assert "get" in filtered["paths"]["/api/users/"]


class TestCollectReferences:
    """Tests for the collect_references function."""

    def test_collect_direct_references(self):
        """Test collecting direct references."""
        obj = {"$ref": "#/components/schemas/User"}
        references = set()

        collect_references(obj, references)

        assert "components/schemas/User" in references

    def test_collect_nested_references(self):
        """Test collecting nested references."""
        obj = {
            "schema": {
                "type": "object",
                "properties": {
                    "user": {"$ref": "#/components/schemas/User"},
                    "post": {"$ref": "#/components/schemas/Post"},
                },
            }
        }
        references = set()

        collect_references(obj, references)

        assert "components/schemas/User" in references
        assert "components/schemas/Post" in references

    def test_collect_references_in_array(self):
        """Test collecting references in an array."""
        obj = {
            "items": [
                {"$ref": "#/components/schemas/User"},
                {"$ref": "#/components/schemas/Post"},
            ]
        }
        references = set()

        collect_references(obj, references)

        assert "components/schemas/User" in references
        assert "components/schemas/Post" in references


class TestExtractReferencedComponents:
    """Tests for the extract_referenced_components function."""

    def test_extract_simple_references(self):
        """Test extracting simple references."""
        components = {
            "schemas": {
                "User": {"type": "object"},
                "Post": {"type": "object"},
                "Comment": {"type": "object"},
            }
        }
        references = {"components/schemas/User", "components/schemas/Post"}

        filtered = extract_referenced_components(components, references)

        assert "schemas" in filtered
        assert "User" in filtered["schemas"]
        assert "Post" in filtered["schemas"]
        assert "Comment" not in filtered["schemas"]

    def test_extract_nested_references(self):
        """Test extracting nested references."""
        components = {
            "schemas": {
                "User": {"type": "object"},
                "Post": {
                    "type": "object",
                    "properties": {
                        "author": {"$ref": "#/components/schemas/User"},
                        "comments": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Comment"},
                        },
                    },
                },
                "Comment": {"type": "object"},
            }
        }
        references = {"components/schemas/Post"}

        filtered = extract_referenced_components(components, references)

        # Should include Post and all referenced schemas (User and Comment)
        assert "schemas" in filtered
        assert "Post" in filtered["schemas"]
        assert "User" in filtered["schemas"]
        assert "Comment" in filtered["schemas"]

    def test_extract_circular_references(self):
        """Test extracting circular references."""
        components = {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "posts": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Post"},
                        }
                    },
                },
                "Post": {
                    "type": "object",
                    "properties": {
                        "author": {"$ref": "#/components/schemas/User"},
                    },
                },
            }
        }
        references = {"components/schemas/User"}

        filtered = extract_referenced_components(components, references)

        # Should handle circular references without infinite recursion
        assert "schemas" in filtered
        assert "User" in filtered["schemas"]
        assert "Post" in filtered["schemas"]


class TestFilterOpenApiSchema:
    """Tests for the filter_openapi_schema function."""

    @patch("swagou.filter.load_schema")
    @patch("swagou.filter.filter_schema")
    def test_filter_openapi_schema(self, mock_filter_schema, mock_load_schema):
        """Test the filter_openapi_schema function."""
        # Mock the load_schema and filter_schema functions
        mock_load_schema.return_value = SAMPLE_SCHEMA
        mock_filter_schema.return_value = {"filtered": True}

        # Call the function
        result = filter_openapi_schema(
            input_source="test.yaml",
            get_paths=["/api/posts/"],
            headers=["Authorization: Bearer token"],
        )

        # Check that the functions were called with the correct arguments
        mock_load_schema.assert_called_once_with("test.yaml", ["Authorization: Bearer token"], [])
        mock_filter_schema.assert_called_once_with(SAMPLE_SCHEMA, ["/api/posts/"], [], [], [], [], [])

        # Check that the result is the YAML representation of the filtered schema
        assert isinstance(result, str)
        assert yaml.safe_load(result) == {"filtered": True}
