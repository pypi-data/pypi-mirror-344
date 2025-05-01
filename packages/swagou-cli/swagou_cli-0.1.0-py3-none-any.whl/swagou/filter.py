"""Core functionality for filtering OpenAPI schemas."""

import fnmatch
from typing import Dict, List, Set, Union

import httpx
import yaml


def filter_openapi_schema(
    input_source: str,
    get_paths: List[str] = None,
    post_paths: List[str] = None,
    patch_paths: List[str] = None,
    delete_paths: List[str] = None,
    all_paths: List[str] = None,
    headers: List[str] = None,
    cookies: List[str] = None,
    tags: List[str] = None,
) -> str:
    """
    Filter an OpenAPI schema to include only specified paths and methods.

    Args:
        input_source: URL to the schema or path to a file
        get_paths: List of path patterns for GET endpoints
        post_paths: List of path patterns for POST endpoints
        patch_paths: List of path patterns for PATCH endpoints
        delete_paths: List of path patterns for DELETE endpoints
        all_paths: List of path patterns for all HTTP methods
        headers: List of HTTP headers to include in requests (format: 'Name: Value')
        cookies: List of cookies to include in requests (format: 'Name: Value')
        tags: List of tags to filter by

    Returns:
        Filtered OpenAPI schema as a YAML string
    """
    # Initialize empty lists if None
    get_paths = get_paths or []
    post_paths = post_paths or []
    patch_paths = patch_paths or []
    delete_paths = delete_paths or []
    all_paths = all_paths or []
    headers = headers or []
    cookies = cookies or []
    tags = tags or []

    # Load the schema
    schema = load_schema(input_source, headers, cookies)

    # Filter the schema
    filtered_schema = filter_schema(
        schema,
        get_paths,
        post_paths,
        patch_paths,
        delete_paths,
        all_paths,
        tags,
    )

    # Convert the filtered schema back to YAML
    return yaml.dump(filtered_schema, sort_keys=False)


def load_schema(input_source: str, headers: List[str] = None, cookies: List[str] = None) -> Dict:
    """
    Load an OpenAPI schema from a file or URL.

    Args:
        input_source: URL to the schema or path to a file
        headers: List of HTTP headers to include in requests (format: 'Name: Value')
        cookies: List of cookies to include in requests (format: 'Name: Value')

    Returns:
        OpenAPI schema as a dictionary
    """
    # Parse headers and cookies
    headers_dict = {}
    cookies_dict = {}

    if headers:
        for header in headers:
            if ":" in header:
                name, value = header.split(":", 1)
                headers_dict[name.strip()] = value.strip()

    if cookies:
        for cookie in cookies:
            if ":" in cookie:
                name, value = cookie.split(":", 1)
                cookies_dict[name.strip()] = value.strip()

    # Check if input_source is a URL
    if input_source.startswith(("http://", "https://")):
        # Fetch the schema from the URL
        response = httpx.get(input_source, headers=headers_dict, cookies=cookies_dict, follow_redirects=True)
        response.raise_for_status()
        content = response.text
    else:
        # Load the schema from a file
        with open(input_source, "r", encoding="utf-8") as f:
            content = f.read()

    # Parse the YAML content
    return yaml.safe_load(content)


def filter_schema(
    schema: Dict,
    get_paths: List[str],
    post_paths: List[str],
    patch_paths: List[str],
    delete_paths: List[str],
    all_paths: List[str],
    tags: List[str],
) -> Dict:
    """
    Filter an OpenAPI schema to include only specified paths and methods.

    Args:
        schema: OpenAPI schema as a dictionary
        get_paths: List of path patterns for GET endpoints
        post_paths: List of path patterns for POST endpoints
        patch_paths: List of path patterns for PATCH endpoints
        delete_paths: List of path patterns for DELETE endpoints
        all_paths: List of path patterns for all HTTP methods
        tags: List of tags to filter by

    Returns:
        Filtered OpenAPI schema as a dictionary
    """
    # Create a copy of the schema to avoid modifying the original
    filtered_schema = {
        "openapi": schema.get("openapi", "3.0.0"),
        "info": schema.get("info", {"title": "Filtered API", "version": "1.0.0"}),
        "paths": {},
    }

    # Add servers if present
    if "servers" in schema:
        filtered_schema["servers"] = schema["servers"]

    # Create a mapping of HTTP methods to path patterns
    method_patterns = {
        "get": get_paths,
        "post": post_paths,
        "patch": patch_paths,
        "delete": delete_paths,
    }

    # Keep track of components that are referenced
    referenced_components = set()

    # Filter paths
    paths = schema.get("paths", {})
    for path, path_item in paths.items():
        # Check if path matches any pattern for any method
        path_matched = False
        filtered_path_item = {}

        # Check if path matches any pattern in all_paths
        for pattern in all_paths:
            if fnmatch.fnmatch(path, pattern):
                # Include all methods for this path
                filtered_path_item = path_item.copy()
                path_matched = True
                break

        # Check specific methods if path wasn't matched by all_paths
        if not path_matched:
            for method, patterns in method_patterns.items():
                if method in path_item and any(fnmatch.fnmatch(path, pattern) for pattern in patterns):
                    # Include this method for this path
                    filtered_path_item[method] = path_item[method]
                    path_matched = True

        # Filter by tags if specified
        if tags and path_matched:
            for method, operation in list(filtered_path_item.items()):
                if method not in ["get", "post", "patch", "delete"]:
                    continue

                operation_tags = operation.get("tags", [])
                if not any(tag in operation_tags for tag in tags):
                    # Remove operations that don't match any of the specified tags
                    del filtered_path_item[method]

        # Add the filtered path item to the filtered schema if it has any operations
        if filtered_path_item:
            filtered_schema["paths"][path] = filtered_path_item

            # Collect referenced components
            collect_references(filtered_path_item, referenced_components)

    # Add referenced components
    if referenced_components and "components" in schema:
        filtered_schema["components"] = extract_referenced_components(schema["components"], referenced_components)

    return filtered_schema


def collect_references(obj: Union[Dict, List], references: Set[str]) -> None:
    """
    Recursively collect all $ref values from an object.

    Args:
        obj: Object to search for references
        references: Set to collect references in
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref" and isinstance(value, str) and value.startswith("#/components/"):
                # Extract the reference path (e.g., "#/components/schemas/User" -> "components/schemas/User")
                ref_path = value[2:]  # Remove the "#/"
                references.add(ref_path)
            else:
                collect_references(value, references)
    elif isinstance(obj, list):
        for item in obj:
            collect_references(item, references)


def extract_referenced_components(components: Dict, references: Set[str]) -> Dict:
    """
    Extract referenced components from the components object.

    Args:
        components: Components object from the OpenAPI schema
        references: Set of references to extract

    Returns:
        Dictionary containing only the referenced components
    """
    filtered_components = {}

    # Create a copy of the references set to iterate over
    # This prevents the "Set changed size during iteration" error
    refs_to_process = list(references.copy())
    processed_refs = set()

    # Process each reference
    while refs_to_process:
        ref = refs_to_process.pop(0)

        # Skip if we've already processed this reference
        if ref in processed_refs:
            continue

        processed_refs.add(ref)

        # Skip the "components/" prefix
        if ref.startswith("components/"):
            ref = ref[len("components/") :]

        # Split the reference path (e.g., "schemas/User" -> ["schemas", "User"])
        parts = ref.split("/")
        if len(parts) >= 2:
            component_type = parts[0]  # e.g., "schemas"
            component_name = parts[1]  # e.g., "User"

            # Ensure the component type exists in the filtered components
            if component_type not in filtered_components:
                filtered_components[component_type] = {}

            # Add the component if it exists in the original components
            if component_type in components and component_name in components[component_type]:
                filtered_components[component_type][component_name] = components[component_type][component_name]

                # Recursively collect references from this component
                # Store the current size of references
                current_size = len(references)
                collect_references(components[component_type][component_name], references)

                # Add any new references to our processing list
                new_refs = list(references - processed_refs)
                refs_to_process.extend(new_refs)

    return filtered_components
