import io
import json
import unittest
from unittest import mock

import list_agents


class FetchAgentsTests(unittest.TestCase):
    def test_fetch_agents_uses_data_wrapper(self):
        payload = {"data": [{"id": "a1", "name": "agent-one", "model": "gpt-4o"}]}

        response = io.BytesIO(json.dumps(payload).encode("utf-8"))
        response.__enter__ = lambda s: s
        response.__exit__ = lambda s, exc_type, exc, tb: False

        with mock.patch("list_agents.request.urlopen", return_value=response) as mocked_open:
            agents = list_agents.fetch_agents("https://example/", "token123")

        self.assertEqual(payload["data"], agents)
        called_request = mocked_open.call_args.args[0]
        self.assertEqual(
            "https://example/agents?api-version=2024-05-01-preview",
            called_request.full_url,
        )
        auth_header = called_request.headers["Authorization"]
        self.assertEqual(auth_header, "Bearer token123")

    def test_fetch_agents_supports_list_payload(self):
        payload = [{"id": "a1"}]

        response = io.BytesIO(json.dumps(payload).encode("utf-8"))
        response.__enter__ = lambda s: s
        response.__exit__ = lambda s, exc_type, exc, tb: False

        with mock.patch("list_agents.request.urlopen", return_value=response):
            agents = list_agents.fetch_agents("https://example", "token123")

        self.assertEqual(payload, agents)


class DisplayRowsTests(unittest.TestCase):
    def test_display_rows_outputs_tabular_text(self):
        out = io.StringIO()
        with mock.patch("sys.stdout", out):
            list_agents._display_rows([
                {"id": "a1", "name": "agent-one", "model": "gpt-4o"},
                {"id": "a2", "name": "agent-two", "model": "gpt-4.1"},
            ])

        self.assertEqual(
            "id\tname\tmodel\na1\tagent-one\tgpt-4o\na2\tagent-two\tgpt-4.1\n",
            out.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
