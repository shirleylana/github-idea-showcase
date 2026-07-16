# Project data contract

Use UTF-8 JSON with these top-level keys:

```json
{
  "profile": {
    "login": "owner",
    "name": "Display name",
    "bio": "Short profile introduction",
    "avatar_url": "https://avatars.githubusercontent.com/...",
    "html_url": "https://github.com/owner"
  },
  "site": {
    "title": "Project Notebook",
    "language": "zh-CN",
    "theme_color": "#77543d",
    "categories": ["工作提效"]
  },
  "projects": [
    {
      "repo": "owner/repository",
      "url": "https://github.com/owner/repository",
      "visibility": "public",
      "fingerprint": "sha256 from repository evidence",
      "generated": {
        "name": "Project name",
        "value": "One-sentence value",
        "production_value": "Qualitative outcome after adoption",
        "category": "工作提效",
        "technologies": ["Python"]
      },
      "approved": null,
      "evidence": ["README: relevant paraphrased evidence"],
      "confidence": "high"
    }
  ]
}
```

## Rules

- `visibility` must equal `public`.
- `repo` is the stable merge key.
- `approved` is either `null` or the same shape as `generated`.
- Render `approved` when present; otherwise render `generated`.
- Never replace a non-null prior `approved` object during merge.
- Use `high`, `medium`, or `low` for `confidence`.
- Evidence must be a short paraphrase with its source location, not copied documentation.
- Do not state money, percentages, time savings, user counts, or multipliers without explicit repository or user evidence.
- Keep categories user-defined. When none are supplied, infer the smallest useful set and request confirmation.

## Fingerprints

Pass repository `full_name`, `updated_at`, `default_branch`, and README blob SHA to `fingerprint_repo`. Re-analyze when the fingerprint changes; otherwise reuse prior generated analysis.
