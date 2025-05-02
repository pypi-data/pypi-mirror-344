"""
Functions generator for OpenAPI endpoints.

This module provides functions to generate Python callables for all endpoints in an OpenAPI spec.
"""

from __future__ import annotations

import types
from pathlib import Path
from typing import List, Dict, Any, Union
from urllib.parse import urljoin

from pydantic import BaseModel, Field, create_model
import requests

from .loader import load_spec, to_snake

def _openapi_to_python_type(openapi_types: List[str]) -> str:
    """
    Maps OpenAPI types to Python type annotations.

    Given a list of OpenAPI types, returns a string representing the corresponding Python type annotation.
    If no types are provided, the function returns 'Any'.
    For each type in the list, the function maps it to a Python type annotation using the following mapping:
    - string: str
    - integer: int
    - number: float
    - boolean: bool
    - array: List[Any]
    - object: Dict[str, Any]
    - null: None
    If the OpenAPI type is not found in the mapping, the function returns 'Any'.
    The function then removes duplicates from the list of Python types while preserving order.
    If the resulting list is empty, the function returns 'Any'.
    If the list contains only one type, the function returns that type.
    Otherwise, the function returns a Union type containing all the types in the list.
    """
    # If no types provided, fallback to Any
    if not openapi_types:
        return "Any"
    # Map OpenAPI types to Python type annotations
    type_map = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "List[Any]",
        "object": "Dict[str, Any]",
        "null": "None",
    }
    python_types = []
    for t in openapi_types:
        python_types.append(type_map.get(t, "Any"))
    # Remove duplicates while preserving order
    unique_types = []
    for t in python_types:
        if t not in unique_types:
            unique_types.append(t)
    # If mapping produced no types, fallback to Any
    if not unique_types:
        return "Any"

    if len(unique_types) == 1:
        return unique_types[0]

    return f"Union[{', '.join(unique_types)}]"


def _generate_components(spec: Dict[str, Any]) -> Dict[str, type[BaseModel]]:
    """
    Generates Pydantic models from OpenAPI schema components.

    This function iterates over the 'components' section of an OpenAPI specification,
    extracting schema definitions and generating Pydantic models for each schema using
    the `pydantic.create_model` function. Each model corresponds to an OpenAPI schema
    and includes fields with types, descriptions, and required status derived from the
    schema's properties.

    Args:
        spec (Dict[str, Any]): The OpenAPI specification containing component schemas.

    Returns:
        Dict[str, Any]: A dictionary mapping each component name to its corresponding
        Pydantic model class.
    """
    component_classes = {}
    components = {}

    for key in spec['components']['schemas'].keys():
        component = spec['components']['schemas'][key]
        properties = component['properties']
        required = component['required'] if 'required' in component else []

        fields = []

        for prop_key, prop_value in properties.items():

            prop_description = prop_value['description'] if 'description' in prop_value else "-"
            prop_types = []

            if 'type' in prop_value:
                prop_types.append(prop_value['type'])

            if 'anyOf' in prop_value:
                any_of = prop_value['anyOf']
                for any_of_item in any_of:
                    prop_types.append(any_of_item['type'])

            field = {
                "name": prop_key,
                "type": _openapi_to_python_type(prop_types),
                "description": prop_description,
                "required": prop_key in required,
            }
            fields.append(field)

        components[key] = fields

    for component_name, fields in components.items():
        class_fields = {}

        for field in fields:
            if field["required"]:
                default = ...
            else:
                default = None
            class_fields[field['name']] = (field['type'], Field(default=default, description=field['description']))

        model = create_model(
            component_name,
            __base__=BaseModel,
            **class_fields
        )
        model.model_rebuild()
        component_classes[component_name] = model

    return component_classes


def _build_function(
    base_url: str,
    path: str,
    method: str,
    query_params: List[str],
    path_params: List[str],
    body_model: type[BaseModel],
    func_name: str,
    doc: str,
    has_body: bool,
):
    """
    Build a Python function for a given OpenAPI endpoint.

    Parameters:
        base_url (str): The base URL of the API.
        path (str): Endpoint path template, possibly containing path parameters.
        method (str): HTTP method for the request (e.g., 'GET', 'POST').
        query_params (List[str]): Names of allowed query parameters.
        path_params (List[str]): Names of required path parameters.
        body_model (type[BaseModel]): Pydantic model for the request body.
        func_name (str): Name to assign to the generated function.
        doc (str): Description to set as the function's docstring.
        has_body (bool): Whether the endpoint accepts a JSON body.

    Returns:
        function: A callable that performs the HTTP request and returns parsed JSON.
    """

    def _endpoint_function(*, base_url: str = base_url, **kwargs):
        """
        A function built for an OpenAPI endpoint.

        The function takes arbitrary keyword arguments, and passes on any matching
        query parameters or path parameters to the request. If a body parameter is
        present and the endpoint allows a body, the body is passed as JSON.

        The function returns the response JSON, after raising an exception if the
        request was not successful.
        """

        base = base_url
        if not base.endswith("/"):
            base += "/"

        for arg in kwargs:
            print(arg)
        
        url = urljoin(base, path.format(**{k: kwargs.pop(k) for k in path_params}))


        params = {k: kwargs.pop(k) for k in query_params if kwargs.get(k) is not None} or None
        body = kwargs.pop('body', None) if has_body else None

        if body_model:
            body_fields = body_model.model_fields
        else:
            body_fields = {}


        response = requests.request(method, url, params=params, json=body, timeout=30)
        response.raise_for_status()
        return response.json()

    _endpoint_function.__name__ = func_name
    _endpoint_function.__doc__ = doc or ""
    return _endpoint_function


def generate_tools(
    spec_src: str | Path,
    removeprefix: str | None = None,
) -> types.SimpleNamespace:
    """
    Generate a namespace of Python callables for all endpoints in an OpenAPI spec.

    This function loads the OpenAPI specification, iterates over each path and method,
    and uses `_build_function` to create a corresponding Python function that handles
    path, query, and body parameters, then aggregates them into a SimpleNamespace.

    Parameters:
        spec_src (str | Path): Path or URL to the OpenAPI JSON specification.

    Returns:
        types.SimpleNamespace: Namespace containing one function per endpoint,
            named `<method>_<snake_case_path>`.
    """

    namespace = types.SimpleNamespace()
    spec = load_spec(spec_src)
    base_url = str(spec_src).removesuffix("/openapi.json")
    components = _generate_components(spec)

    # Iterate through paths
    for path, methods in spec['paths'].items():
        func_path = to_snake(path, removeprefix) if removeprefix else to_snake(path)

        # Iterate through methods in each path
        for method, method_spec in methods.items():
            method_name = method.lower()
            method_signature = method.lower()
            if method_name == 'post':
                method_signature = 'create'
            elif method_name == 'put':
                method_signature = 'update'

            func_name = f"{method_signature}_{func_path}"

            path_params: List[str] = []
            query_params: List[str] = []
            body_model = None
            py_args: List[str] = []

            # Define path and query params
            for param in method_spec.get('parameters', []):
                name, location, required = param['name'], param['in'], param['required']

                if location == 'path':
                    path_params.append(name)
                elif location == 'query':
                    query_params.append(name)

                py_args.append(name if required else f"{name}=None")

            has_body = (method_name in ['post', 'put']) and ('requestBody' in method_spec)

            # Request body
            if has_body:
                py_args.append('body')
                ref = method_spec['requestBody']['content']['application/json']['schema']['$ref']
                ref_name = ref.removeprefix("#/components/schemas/")
                body_model = components[ref_name]

            func = _build_function(
                base_url=base_url,
                path=path,
                method=method,
                query_params=query_params,
                path_params=path_params,
                body_model=body_model,
                func_name=func_name,
                doc=method_spec.get("description"),
                has_body=has_body,
            )

            setattr(namespace, func_name, func)

    return namespace
