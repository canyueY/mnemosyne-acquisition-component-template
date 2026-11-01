"""Offline checks of the inert template, not acquisition or Node integration."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "mnemosyne_acquisition_template"
sys.path.insert(0, str(ROOT / "src"))

from mnemosyne_acquisition_template import (  # noqa: E402
    TEMPLATE_ONLY,
    TemplateMnemosyneBridge,
    TemplateNotImplementedError,
    TemplateResearchHook,
    TemplateSourceAdapter,
)
from mnemosyne_acquisition_template.contracts import (  # noqa: E402
    AcquisitionBatch,
    AcquisitionRequest,
    ConnectionProfile,
    ResearchSignals,
    SourceIdentity,
    SubmissionReceipt,
)


def example(filename):
    return json.loads((ROOT / "examples" / filename).read_text(encoding="utf-8"))


class TemplateBoundaryTests(unittest.TestCase):
    def test_all_extension_methods_raise_instead_of_succeeding(self):
        source = TemplateSourceAdapter()
        bridge = TemplateMnemosyneBridge()
        research = TemplateResearchHook()
        profile = ConnectionProfile()
        calls = [
            (source.read, (AcquisitionRequest(source_id="fictional", intent="test"),)),
            (source.normalize, ({},)),
            (bridge.inspect_connection, (profile,)),
            (bridge.map_observation, (None, profile)),
            (bridge.submit_observation, ({}, profile)),
            (bridge.read_cognition_state, (None, profile)),
            (research.assess, (ResearchSignals(), {})),
        ]
        for method, arguments in calls:
            with self.subTest(method=method.__qualname__):
                with self.assertRaises(TemplateNotImplementedError):
                    method(*arguments)

    def test_every_public_extension_is_covered_and_only_raises(self):
        expected = {
            "TemplateSourceAdapter": {"read", "normalize"},
            "TemplateMnemosyneBridge": {
                "inspect_connection", "map_observation", "submit_observation", "read_cognition_state"
            },
            "TemplateResearchHook": {"assess"},
        }
        for cls in (TemplateSourceAdapter, TemplateMnemosyneBridge, TemplateResearchHook):
            public = {name for name, fn in inspect.getmembers(cls, inspect.isfunction) if not name.startswith("_")}
            self.assertEqual(expected[cls.__name__], public)
        tree = ast.parse((SOURCE / "stubs.py").read_text(encoding="utf-8"))
        methods = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        self.assertEqual(7, len(methods))
        for method in methods:
            self.assertEqual(1, len(method.body))
            self.assertIsInstance(method.body[0], ast.Raise)
            self.assertEqual("TemplateNotImplementedError", method.body[0].exc.func.id)

    def test_runtime_imports_cannot_include_io_or_platform_libraries(self):
        allowed = {"__future__", "abc", "dataclasses", "typing"}
        local = {"contracts", "ports", "errors", "stubs"}
        for file in SOURCE.glob("*.py"):
            tree = ast.parse(file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertIn(alias.name, allowed, (file.name, alias.name))
                if isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module, local if node.level else allowed, (file.name, node.module))

    def test_runtime_has_no_hidden_calls_or_executable_top_level_work(self):
        safe_calls = {"dataclass", "field", "abstractmethod", "NotImplementedError", "TemplateNotImplementedError"}
        for file in SOURCE.glob("*.py"):
            tree = ast.parse(file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    self.assertIsInstance(node.func, ast.Name, file.name)
                    self.assertIn(node.func.id, safe_calls, (file.name, node.func.id))
                self.assertNotIsInstance(node, (ast.With, ast.AsyncWith, ast.For, ast.AsyncFor, ast.While), file.name)
            for statement in tree.body:
                self.assertIsInstance(statement, (ast.Expr, ast.Import, ast.ImportFrom, ast.ClassDef, ast.Assign), file.name)
                if isinstance(statement, ast.Expr):
                    self.assertIsInstance(statement.value, ast.Constant, file.name)
                    self.assertIsInstance(statement.value.value, str, file.name)
        self.assertTrue(TEMPLATE_ONLY)

    def test_no_cli_server_or_dependency_is_declared(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertRegex(pyproject, r"(?m)^dependencies\s*=\s*\[\s*\]\s*$")
        self.assertNotIn("[project.scripts]", pyproject)
        self.assertNotIn("[project.entry-points", pyproject)
        self.assertFalse((SOURCE / "__main__.py").exists())

    def test_example_manifest_is_not_an_installable_capability_claim(self):
        manifest = example("mnemosyne.component.example.json")
        self.assertEqual([], manifest["interfaces"]["provides"])
        self.assertEqual([], manifest["interfaces"]["requires"])
        self.assertEqual([], manifest["permissions"])
        self.assertEqual([], manifest["banks"])
        self.assertTrue(manifest["metadata"]["template_only"])
        self.assertFalse(manifest["metadata"]["implemented"])
        self.assertFalse(manifest["metadata"]["automatic_start"])
        self.assertNotIn("entry", manifest)
        self.assertFalse(any(manifest["lifecycle"].values()))
        for filename in ("mnemosyne.component.json", "component.json", "manifest.json"):
            self.assertFalse((ROOT / filename).exists())
            self.assertFalse((ROOT / "examples" / filename).exists())

    def test_connection_and_policy_defaults_are_not_grants(self):
        config = example("component.config.example.json")
        self.assertFalse(config["implemented"])
        self.assertFalse(config["automatic_acquisition_enabled"])
        self.assertFalse(config["network_allowed"])
        self.assertEqual([], config["granted_permissions"])
        for key in ("base_url", "credential_reference", "authorization_reference", "bank_id"):
            self.assertIsNone(config["connection"][key])
        self.assertFalse(any(config["policy"].values()))
        profile = ConnectionProfile()
        self.assertIsNone(profile.base_url)
        self.assertIsNone(profile.bank_id)
        self.assertIsNone(profile.credential_reference)

    def test_research_profile_is_documented_but_not_implemented(self):
        policy = example("research-policy.example.json")
        self.assertFalse(policy["implemented"])
        self.assertFalse(policy["automatic_search_enabled"])
        profile = policy["suggested_profile_for_derivatives"]
        self.assertAlmostEqual(1.0, sum(profile["gap_weights"].values()))
        self.assertEqual(0.70, profile["minimum_task_relevance"])
        self.assertEqual(0.60, profile["minimum_gap_score"])
        self.assertFalse(profile["private_text_in_public_query"])
        self.assertFalse(profile["limits"]["allow_paid_providers"])
        signals = ResearchSignals()
        self.assertIsNone(signals.task_relevance)
        self.assertIsNone(signals.evidence_gap)
        with self.assertRaises(TemplateNotImplementedError):
            TemplateResearchHook().assess(signals, policy)

    def test_fictional_content_hash_and_roles_are_consistent(self):
        item = example("acquired-item.example.json")
        wire = example("observation.example.json")
        digest = hashlib.sha256(item["content"].encode("utf-8")).hexdigest()
        self.assertEqual(digest, item["source"]["content_hash"])
        self.assertEqual(digest, wire["metadata"]["source_ref"]["content_hash"])
        self.assertEqual(item["content"], wire["content"])
        self.assertIn("虚构", item["content"])
        self.assertEqual("author_claim", item["source"]["source_role"])
        self.assertEqual("system", wire["source_kind"])
        self.assertEqual("partial", item["coverage"]["completeness"])
        self.assertIsNone(item["source"]["locator"]["page"])
        self.assertFalse(wire["metadata"]["policy"]["allow_store"])
        SourceIdentity(**item["source"])  # Logical shape only, not runtime validation.

    def test_receipt_cannot_claim_unsent_observation_or_cognition(self):
        data = example("receipt.example.json")
        self.assertTrue(data["illustrative_only"])
        self.assertEqual("not_attempted", data["submission"]["transport_state"])
        self.assertIsNone(data["submission"]["observation_id"])
        self.assertIsNone(data["cognition"])
        receipt = SubmissionReceipt(correlation_id="fictional", idempotency_key="fictional")
        self.assertEqual("not_attempted", receipt.transport_state)
        self.assertIsNone(receipt.observation_id)

    def test_empty_batch_is_just_data_not_a_successful_read(self):
        self.assertEqual("unknown", AcquisitionBatch().completeness)
        self.assertEqual((), AcquisitionBatch().deletion_markers)
        with self.assertRaises(TemplateNotImplementedError):
            TemplateSourceAdapter().read(AcquisitionRequest(source_id="fixture", intent="read"))

    def test_document_links_are_local_and_resolvable(self):
        for path in (ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#")):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).is_file(), (path.name, target))

    def test_license_is_mit_and_documents_dont_claim_a_live_component(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("没有业务能力的模板", readme)
        self.assertIn("不证明", (ROOT / "docs" / "ACCEPTANCE.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
