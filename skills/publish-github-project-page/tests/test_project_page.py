import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
TEMPLATE_DIR = ROOT / "assets" / "site-template"
PRISM_TEMPLATE_DIR = ROOT / "assets" / "site-template-prism"


def load_module():
    path = ROOT / "scripts" / "project_page.py"
    spec = importlib.util.spec_from_file_location("project_page", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fixture(name):
    return json.loads((FIXTURES / name).read_text())


class ProjectPageTests(unittest.TestCase):
    def test_merge_preserves_approved_copy(self):
        project_page = load_module()
        merged = project_page.merge_site(fixture("existing.json"), fixture("incoming.json"))
        self.assertEqual(merged["projects"][0]["approved"]["value"], "人工确认价值")
        self.assertEqual(merged["projects"][0]["generated"]["value"], "新的 AI 建议")

    def test_private_repository_is_rejected(self):
        project_page = load_module()
        data = copy.deepcopy(fixture("incoming.json"))
        data["projects"][0]["visibility"] = "private"
        self.assertIn("must be public", "\n".join(project_page.validate_site(data)))

    def test_numeric_claim_without_evidence_is_rejected(self):
        project_page = load_module()
        data = copy.deepcopy(fixture("incoming.json"))
        data["projects"][0]["generated"]["production_value"] = "效率提升 80%"
        data["projects"][0]["evidence"] = []
        self.assertIn("numeric claim", "\n".join(project_page.validate_site(data)))

    def test_fingerprint_is_stable_and_change_sensitive(self):
        project_page = load_module()
        repo = {"full_name": "demo/tool", "updated_at": "2026-01-01", "default_branch": "main", "readme_sha": "a"}
        self.assertEqual(project_page.fingerprint_repo(repo), project_page.fingerprint_repo(copy.deepcopy(repo)))
        changed = {**repo, "readme_sha": "b"}
        self.assertNotEqual(project_page.fingerprint_repo(repo), project_page.fingerprint_repo(changed))

    def test_render_writes_complete_static_site(self):
        project_page = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            files = project_page.render_site(fixture("incoming.json"), TEMPLATE_DIR, Path(tmp))
            self.assertEqual(
                {path.name for path in files},
                {"index.html", "styles.css", "app.js", "projects.json"},
            )
            html = Path(tmp, "index.html").read_text()
            self.assertIn('role="tablist"', html)
            self.assertIn('aria-label="Project categories"', html)

    def test_render_rejects_invalid_data_before_writing(self):
        project_page = load_module()
        data = fixture("incoming.json")
        data["projects"][0]["visibility"] = "private"
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "must be public"):
                project_page.render_site(data, TEMPLATE_DIR, Path(tmp))
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_prism_template_is_renderable_and_has_real_filtering(self):
        project_page = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            project_page.render_site(fixture("incoming.json"), PRISM_TEMPLATE_DIR, Path(tmp))
            html = Path(tmp, "index.html").read_text()
            app = Path(tmp, "app.js").read_text()
            self.assertIn('class="intro"', html)
            self.assertIn("function filterProjects", app)
            self.assertIn("module.exports = { filterProjects }", app)


if __name__ == "__main__":
    unittest.main()
