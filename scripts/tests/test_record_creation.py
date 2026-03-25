#!/usr/bin/env python3
"""Tests for scripts/create_record.py — record scaffolding with sequential IDs."""
import sys
import pathlib

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from create_record import create_record, next_id, slugify  # noqa: E402


class TestSlugify:
    def test_basic_slug(self) -> None:
        assert slugify("My Test Decision") == "my-test-decision"

    def test_special_characters(self) -> None:
        assert slugify("API Design / Proposal") == "api-design-proposal"

    def test_leading_trailing_hyphens(self) -> None:
        assert slugify("--hello--") == "hello"

    def test_consecutive_hyphens(self) -> None:
        assert slugify("foo   bar") == "foo-bar"


class TestNextId:
    def test_empty_dir(self, tmp_path: pathlib.Path) -> None:
        assert next_id(tmp_path, "ADR") == "ADR-001"

    def test_existing_files(self, tmp_path: pathlib.Path) -> None:
        (tmp_path / "ADR-001-first.md").touch()
        (tmp_path / "ADR-002-second.md").touch()
        assert next_id(tmp_path, "ADR") == "ADR-003"

    def test_non_sequential_files(self, tmp_path: pathlib.Path) -> None:
        (tmp_path / "ADR-005-fifth.md").touch()
        assert next_id(tmp_path, "ADR") == "ADR-006"


class TestCreateRecord:
    def test_create_adr_file_exists(self, tmp_path: pathlib.Path) -> None:
        path = create_record("adr", "Test Decision", output_dir=tmp_path)
        assert path.exists()
        assert path.parent == tmp_path / "adr"
        assert path.name.startswith("ADR-001-")

    def test_create_adr_frontmatter(self, tmp_path: pathlib.Path) -> None:
        path = create_record("adr", "Test Decision", output_dir=tmp_path)
        content = path.read_text(encoding="utf-8")
        assert "record_id: \"ADR-001\"" in content
        assert "type: \"adr\"" in content
        assert "status: \"DRAFT\"" in content
        assert "title: \"Test Decision\"" in content
        assert "created_at:" in content

    def test_create_adr_sections(self, tmp_path: pathlib.Path) -> None:
        path = create_record("adr", "Test Decision", output_dir=tmp_path)
        content = path.read_text(encoding="utf-8")
        assert "# Context" in content
        assert "# Decision" in content
        assert "# Consequences" in content
        assert "# Verification" in content

    def test_create_rfc_file_exists(self, tmp_path: pathlib.Path) -> None:
        path = create_record("rfc", "API Design", output_dir=tmp_path)
        assert path.exists()
        assert path.parent == tmp_path / "rfc"
        assert path.name.startswith("RFC-001-")

    def test_create_rfc_sections(self, tmp_path: pathlib.Path) -> None:
        path = create_record("rfc", "API Design", output_dir=tmp_path)
        content = path.read_text(encoding="utf-8")
        assert "# Summary" in content
        assert "# Design / Proposal" in content
        assert "# Verification" in content

    def test_sequential_id(self, tmp_path: pathlib.Path) -> None:
        path1 = create_record("adr", "First", output_dir=tmp_path)
        path2 = create_record("adr", "Second", output_dir=tmp_path)
        assert "ADR-001-" in path1.name
        assert "ADR-002-" in path2.name

    def test_invalid_type(self, tmp_path: pathlib.Path) -> None:
        with pytest.raises(ValueError):
            create_record("invalid", "Bad Type", output_dir=tmp_path)

    def test_slug_generation(self, tmp_path: pathlib.Path) -> None:
        path = create_record("adr", "My Test Decision", output_dir=tmp_path)
        assert "my-test-decision" in path.name
