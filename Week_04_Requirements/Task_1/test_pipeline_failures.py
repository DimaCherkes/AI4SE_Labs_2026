"""Regression checks for failed live runs and unsupported mock claims."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import requirements_agent as agent
import verify_pipeline


ROOT = Path(__file__).resolve().parent


class PipelineFailureTests(unittest.TestCase):
    def test_live_run_without_key_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "corpus"
            corpus.mkdir()
            (corpus / "request.txt").write_text(
                "The system shall let staff export a report of monthly payments.\n",
                encoding="utf-8",
            )
            output = root / "requirements.md"
            output.write_text("PREVIOUS_VALID_OUTPUT", encoding="utf-8")
            env = os.environ.copy()
            env["OPENAI_API_KEY"] = ""
            result = subprocess.run(
                [sys.executable, str(ROOT / "requirements_agent.py"),
                 "--corpus-dir", str(corpus), "--output-file", str(output)],
                cwd=root, env=env, capture_output=True, text=True, timeout=30,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("OPENAI_API_KEY", result.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "PREVIOUS_VALID_OUTPUT")

    def test_arbitrary_mock_corpus_has_no_invented_rejections(self):
        documents = [{"source_path": "request.txt", "content": "The system shall export reports."}]
        result = agent._get_mock_dedup_and_blacklist(documents, [])
        self.assertEqual(result["blacklist"], [])

    def test_exhausted_audit_does_not_route_to_approved_export(self):
        state = {"audit_report": {"passed": False, "issues": ["REQ-001: duplicate"]},
                 "iteration_count": 3, "max_iterations": 3}
        with self.assertRaisesRegex(RuntimeError, "Audit did not pass"):
            agent.should_refine(state)

    def test_blacklist_citations_must_resolve_to_corpus_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "real.txt").write_text("Source", encoding="utf-8")
            document = (ROOT / "requirements.md").read_text(encoding="utf-8")
            document = document.replace(
                "- **Sources:** `email_staff_login.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`",
                "- **Sources:** `RAW-999`", 1)
            output = root / "requirements.md"
            output.write_text(document, encoding="utf-8")
            results = verify_pipeline.verify_document_compliance(str(output), str(root))
            self.assertFalse(results["TST-DOC-09"][0])

    def test_llm_candidate_ids_resolve_to_real_source_paths(self):
        paths = {"notes/request.txt", "mail.eml"}
        raw = {"RAW-007": ["notes/request.txt", "mail.eml"],
               "RAW-053": ["mail.eml"]}
        self.assertEqual(
            agent._resolve_candidate_sources(["RAW-007", "request.txt"], raw, paths),
            ["notes/request.txt", "mail.eml"],
        )
        with self.assertRaisesRegex(ValueError, "Citation does not identify"):
            agent._resolve_candidate_sources(["RAW-999"], raw, paths)
        self.assertEqual(agent._resolve_candidate_sources(["RAW-53"], raw, paths),
                         ["mail.eml"])

    def test_live_extraction_error_does_not_use_mock_candidates(self):
        class FailingLLM:
            def with_structured_output(self, _schema):
                return self

            def invoke(self, _messages):
                raise OSError("synthetic API failure")

        state = {"mock_mode": False, "documents": [
            {"source_path": "request.txt", "title": "Request",
             "content": "The service shall export payment reports."}
        ]}
        with patch.object(agent, "get_llm", return_value=FailingLLM()):
            with self.assertRaisesRegex(RuntimeError, "Extraction failed for batch"):
                agent.extract_requirements(state)

    def test_consolidated_requirement_source_must_be_cited(self):
        corpus = ROOT / "data/corpus"
        document = (ROOT / "requirements.md").read_text(encoding="utf-8")
        document = document.replace(
            "conversations/conv_pines023_patron_characteristics.eml",
            "survey_results_2009.txt",
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "requirements.md"
            output.write_text(document, encoding="utf-8")
            results = verify_pipeline.verify_document_compliance(str(output), str(corpus))
            self.assertFalse(results["TST-DOC-08"][0])
            self.assertIn("patron_characteristics", results["TST-DOC-08"][1])

    def test_pipeline_detects_dropped_consolidated_source(self):
        docs = [{"source_path": "patrons.eml",
                 "content": "Subject: SUMMARY: Patron characteristics requirement\nRequirement consolidated: group by age."}]
        self.assertEqual(agent._missing_consolidated_sources(docs, []), {"patrons.eml"})
        self.assertEqual(agent._missing_consolidated_sources(
            docs, [{"sources": ["patrons.eml"]}]), set())

    def test_refiner_can_repair_a_blacklist_item(self):
        class FakeLLM:
            def with_structured_output(self, _schema):
                return self

            def invoke(self, _messages):
                return agent.RefinementResult(updated_blacklist=[agent.BlacklistItem(
                    id="BLK-001", title="Rejected automatic deletion",
                    rationale="The source rejects automatic deletion because staff must inspect each record before a permanent change is approved.",
                    sources=["decision.txt"],
                )])

        state = {"mock_mode": False, "documents": [], "refined_requirements": [],
                 "blacklist": [{"id": "BLK-001", "title": "Rejected automatic deletion",
                                "rationale": "Too short", "sources": ["decision.txt"]}],
                 "audit_report": {"issues": ["BLK-001 blacklist justification too short"],
                                  "feedback": "Expand the rationale"}, "iteration_count": 0}
        with patch.object(agent, "get_llm", return_value=FakeLLM()):
            result = agent.refine_requirements(state)
        self.assertGreaterEqual(len(result["blacklist"][0]["rationale"].split()), 15)

    def test_refiner_can_merge_duplicate_requirements(self):
        original = [
            {"id": "REQ-001", "title": "Staff cancellation record", "explanation": "Original one", "priority": "Must Have", "sources": ["a.txt"], "subsystem": "General"},
            {"id": "REQ-002", "title": "Record staff cancellation", "explanation": "Original two", "priority": "Must Have", "sources": ["b.txt"], "subsystem": "General"},
        ]

        class FakeLLM:
            def with_structured_output(self, _schema):
                return self

            def invoke(self, _messages):
                return agent.RefinementResult(
                    updated_requirements=[agent.Requirement(**{
                        **original[0], "explanation": "Record each staff cancellation with a timestamp and retain it for review. " * 5
                    })],
                    removed_requirement_ids=["REQ-002"],
                )

        state = {"mock_mode": False, "documents": [], "refined_requirements": original,
                 "blacklist": [], "audit_report": {"issues": ["REQ-001: DUPLICATE of REQ-002"],
                                                 "feedback": "Merge the two"}, "iteration_count": 0}
        with patch.object(agent, "get_llm", return_value=FakeLLM()):
            result = agent.refine_requirements(state)
        self.assertEqual(len(result["refined_requirements"]), 1)
        self.assertEqual(result["refined_requirements"][0]["sources"], ["a.txt", "b.txt"])

    def test_dedup_discards_only_uncited_items(self):
        class FakeLLM:
            def with_structured_output(self, _schema):
                return self

            def invoke(self, _messages):
                base = {"title": "Export monthly payment reports",
                        "explanation": "The service shall export monthly payment reports for authorized staff. " * 5,
                        "priority": "Must Have", "subsystem": "Reports"}
                return agent.DeduplicationResult(refined_requirements=[
                    agent.Requirement(id="REQ-001", sources=["request.txt"], **base),
                    agent.Requirement(id="REQ-002", sources=[], **base),
                ], blacklist=[])

        state = {"mock_mode": False, "raw_requirements": [
            {"id": "RAW-001", "sources": ["request.txt"]}],
            "documents": [{"source_path": "request.txt", "content": "Export monthly reports."}]}
        with patch.object(agent, "get_llm", return_value=FakeLLM()):
            result = agent.resolve_conflicts_and_deduplicate(state)
        self.assertEqual(len(result["refined_requirements"]), 1)
        self.assertEqual(result["refined_requirements"][0]["sources"], ["request.txt"])


if __name__ == "__main__":
    unittest.main()
