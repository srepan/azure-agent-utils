#!/usr/bin/env python3
"""List Azure AI Foundry agents for a project endpoint."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable
from urllib import error, parse, request


DEFAULT_API_VERSION = "2024-05-01-preview"


def _normalize_endpoint(endpoint: str) -> str:
    return endpoint.rstrip("/")


def fetch_agents(endpoint: str, token: str, api_version: str = DEFAULT_API_VERSION) -> list[dict[str, Any]]:
    normalized_endpoint = _normalize_endpoint(endpoint)
    query = parse.urlencode({"api-version": api_version})
    url = f"{normalized_endpoint}/agents?{query}"

    req = request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )

    with request.urlopen(req) as response:  # nosec: B310 - URL comes from explicit CLI input
        payload = json.load(response)

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return data

    raise ValueError("Unexpected response format while listing agents")


def _display_rows(agents: Iterable[dict[str, Any]]) -> None:
    print("id\tname\tmodel")
    for agent in agents:
        print(
            f"{agent.get('id', '')}\t"
            f"{agent.get('name', '')}\t"
            f"{agent.get('model', '')}"
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List agents in an Azure AI Foundry project")
    parser.add_argument("--endpoint", required=True, help="Project endpoint, e.g. https://<resource>.services.ai.azure.com/api/projects/<project>")
    parser.add_argument("--token", required=True, help="Access credential for the project endpoint")
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION, help=f"API version to use (default: {DEFAULT_API_VERSION})")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        agents = fetch_agents(args.endpoint, args.token, args.api_version)
    except error.HTTPError as exc:
        print(f"Failed to list agents (HTTP {exc.code}): {exc.reason}", file=sys.stderr)
        return 1
    except error.URLError as exc:
        print(f"Failed to connect to endpoint: {exc.reason}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    _display_rows(agents)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
