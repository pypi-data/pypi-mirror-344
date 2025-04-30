
"""
Functions generator for OpenAPI endpoints.

This module provides functions to generate Python callables for all endpoints in an OpenAPI spec.
"""

from __future__ import annotations

import types
from pathlib import Path
from typing import List
from urllib.parse import urljoin

import requests

from .loader import load_spec, to_snake


def _build_function(
    base_url: str,
    path: str,
    method: str,
    query_params: List[str],
    path_params: List[str],
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

        url = urljoin(base, path.format(**{k: kwargs.pop(k) for k in path_params}))

        params = {k: kwargs.pop(k) for k in query_params if kwargs.get(k) is not None} or None
        body = kwargs.pop('body', None) if has_body else None

        response = requests.request(method, url, params=params, json=body, timeout=30)
        response.raise_for_status()
        return response.json()

    _endpoint_function.__name__ = func_name
    _endpoint_function.__doc__ = doc or ""
    return _endpoint_function


def generate_tools(
    spec_src: str | Path,
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

    # Iterate through paths
    for path, methods in spec['paths'].items():
        func_path = to_snake(path, "/api/v1")

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

            func = _build_function(
                base_url=base_url,
                path=path,
                method=method,
                query_params=query_params,
                path_params=path_params,
                func_name=func_name,
                doc=method_spec.get("description"),
                has_body=has_body,
            )

            setattr(namespace, func_name, func)

    return namespace
