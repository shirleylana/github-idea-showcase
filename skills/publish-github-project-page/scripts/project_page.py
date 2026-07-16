#!/usr/bin/env python3
"""Validate, merge, and render GitHub project-page data."""

import copy
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil


NUMERIC_CLAIM = re.compile(r"\d+(?:\.\d+)?\s*(?:%|倍|元|万|小时|分钟)")


def fingerprint_repo(repo):
    payload = {
        key: repo.get(key)
        for key in ("full_name", "updated_at", "default_branch", "readme_sha")
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_site(data):
    errors = []
    if not isinstance(data.get("profile"), dict):
        errors.append("profile must be an object")
    if not isinstance(data.get("site"), dict):
        errors.append("site must be an object")
    if not isinstance(data.get("projects"), list):
        return errors + ["projects must be an array"]

    seen = set()
    for project in data["projects"]:
        repo = project.get("repo", "<unknown>")
        if repo in seen:
            errors.append(f"{repo}: duplicate repository")
        seen.add(repo)
        if project.get("visibility") != "public":
            errors.append(f"{repo}: repository must be public")
        if not project.get("url", "").startswith("https://github.com/"):
            errors.append(f"{repo}: url must be a GitHub HTTPS URL")
        generated = project.get("generated") or {}
        approved = project.get("approved") or {}
        text = json.dumps({"generated": generated, "approved": approved}, ensure_ascii=False)
        if NUMERIC_CLAIM.search(text) and not project.get("evidence"):
            errors.append(f"{repo}: numeric claim requires evidence")
    return errors


def merge_site(existing, incoming):
    previous = {item["repo"]: item for item in existing.get("projects", [])}
    merged = copy.deepcopy(incoming)
    for project in merged.get("projects", []):
        old = previous.get(project["repo"])
        if old and old.get("approved"):
            project["approved"] = copy.deepcopy(old["approved"])
    return merged


def render_site(data, template_dir, output_dir):
    errors = validate_site(data)
    if errors:
        raise ValueError("\n".join(errors))
    template_dir = Path(template_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name in ("index.html", "styles.css", "app.js"):
        source = template_dir / name
        if not source.is_file():
            raise FileNotFoundError(f"missing template file: {source}")
        target = output_dir / name
        shutil.copyfile(source, target)
        written.append(target)
    data_target = output_dir / "projects.json"
    data_target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    written.append(data_target)
    return written


def read_json(path):
    return json.loads(Path(path).read_text())


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate a project data file")
    validate.add_argument("--data", required=True)
    render = commands.add_parser("render", help="render a static project site")
    render.add_argument("--data", required=True)
    render.add_argument("--template", required=True)
    render.add_argument("--output", required=True)
    merge = commands.add_parser("merge", help="merge incoming data while preserving approved copy")
    merge.add_argument("--existing", required=True)
    merge.add_argument("--incoming", required=True)
    merge.add_argument("--output", required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        errors = validate_site(read_json(args.data))
        if errors:
            print("\n".join(errors))
            return 1
        print("Project data is valid.")
        return 0
    if args.command == "render":
        files = render_site(read_json(args.data), args.template, args.output)
        print(f"Rendered {len(files)} files to {args.output}")
        return 0
    merged = merge_site(read_json(args.existing), read_json(args.incoming))
    errors = validate_site(merged)
    if errors:
        print("\n".join(errors))
        return 1
    Path(args.output).write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
    print(f"Merged data written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
