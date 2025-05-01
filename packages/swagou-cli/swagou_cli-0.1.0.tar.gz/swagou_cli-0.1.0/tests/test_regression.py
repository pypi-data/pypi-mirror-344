"""Regression tests for specific bugs that have been fixed."""

import pytest

from swagou.filter import extract_referenced_components


class TestSetChangedSizeRegression:
    """Tests for the "Set changed size during iteration" bug that was fixed."""

    def test_circular_references_no_iteration_error(self):
        """Test that circular references don't cause a "Set changed size during iteration" error."""
        # Create a components object with circular references
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
                        "comments": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Comment"},
                        },
                    },
                },
                "Comment": {
                    "type": "object",
                    "properties": {
                        "author": {"$ref": "#/components/schemas/User"},
                        "post": {"$ref": "#/components/schemas/Post"},
                    },
                },
            }
        }

        # Create a set of references with one initial reference
        references = {"components/schemas/User"}

        # This should not raise a "Set changed size during iteration" error
        filtered = extract_referenced_components(components, references)

        # Verify that all referenced components are included
        assert "schemas" in filtered
        assert "User" in filtered["schemas"]
        assert "Post" in filtered["schemas"]
        assert "Comment" in filtered["schemas"]

        # Verify that the references set contains all the references
        assert "components/schemas/User" in references
        assert "components/schemas/Post" in references
        assert "components/schemas/Comment" in references

    def test_deep_nested_references_no_iteration_error(self):
        """Test that deeply nested references don't cause a "Set changed size during iteration" error."""
        # Create a components object with deeply nested references
        components = {
            "schemas": {
                "Level1": {
                    "type": "object",
                    "properties": {
                        "level2": {"$ref": "#/components/schemas/Level2"},
                    },
                },
                "Level2": {
                    "type": "object",
                    "properties": {
                        "level3": {"$ref": "#/components/schemas/Level3"},
                    },
                },
                "Level3": {
                    "type": "object",
                    "properties": {
                        "level4": {"$ref": "#/components/schemas/Level4"},
                    },
                },
                "Level4": {
                    "type": "object",
                    "properties": {
                        "level5": {"$ref": "#/components/schemas/Level5"},
                    },
                },
                "Level5": {
                    "type": "object",
                    "properties": {
                        "circular": {"$ref": "#/components/schemas/Level1"},
                    },
                },
            }
        }

        # Create a set of references with one initial reference
        references = {"components/schemas/Level1"}

        # This should not raise a "Set changed size during iteration" error
        filtered = extract_referenced_components(components, references)

        # Verify that all referenced components are included
        assert "schemas" in filtered
        assert "Level1" in filtered["schemas"]
        assert "Level2" in filtered["schemas"]
        assert "Level3" in filtered["schemas"]
        assert "Level4" in filtered["schemas"]
        assert "Level5" in filtered["schemas"]

        # Verify that the references set contains all the references
        assert "components/schemas/Level1" in references
        assert "components/schemas/Level2" in references
        assert "components/schemas/Level3" in references
        assert "components/schemas/Level4" in references
        assert "components/schemas/Level5" in references
