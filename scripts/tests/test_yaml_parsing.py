#!/usr/bin/env python3
"""
TDD Cycle: P0-1 PyYAML 도입
RED Phase: PyYAML 기반 YAML 파싱 테스트

이 테스트는 generate.py와 gatekeeper.py의 load_config 함수가
PyYAML을 사용하여 YAML을 올바르게 파싱하는지 검증합니다.
"""
import pathlib
import tempfile
import unittest

# Import the modules under test
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from generate import load_config as generate_load_config
from gatekeeper import load_config as gatekeeper_load_config


class TestYAMLParsingWithPyYAML(unittest.TestCase):
    """PyYAML 기반 YAML 파싱 테스트"""

    def setUp(self):
        """테스트용 임시 YAML 파일 생성"""
        self.test_yaml_content = '''version: "1.0"

project:
  name: "test-project"
  description: "A test project"

workspaces:
  primary:
    name: "main"
    branch: "main"
    runtime: "python3.11"

processes:
  enabled:
    - P0
    - P1
    - P3

tools:
  claude:
    enabled: true
    hook_enforcement: true
  codex:
    enabled: false

records:
  wp_path: "docs/work-packets"
  adr_path: "docs/adr"
  changelog_path: "docs/CHANGELOG.md"
'''
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = pathlib.Path(self.temp_dir) / "test-config.yaml"
        self.config_path.write_text(self.test_yaml_content, encoding="utf-8")

    def tearDown(self):
        """임시 파일 정리"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_load_config_parses_project_section(self):
        """generate.py load_config가 project 섹션을 올바르게 파싱하는지 검증"""
        config = generate_load_config(self.config_path)

        self.assertIn("project", config)
        self.assertEqual(config["project"]["name"], "test-project")
        self.assertEqual(config["project"]["description"], "A test project")

    def test_generate_load_config_parses_nested_workspaces(self):
        """generate.py load_config가 중첩된 workspaces 섹션을 파싱하는지 검증"""
        config = generate_load_config(self.config_path)

        self.assertIn("workspaces", config)
        self.assertIn("primary", config["workspaces"])
        self.assertEqual(config["workspaces"]["primary"]["name"], "main")
        self.assertEqual(config["workspaces"]["primary"]["branch"], "main")
        self.assertEqual(config["workspaces"]["primary"]["runtime"], "python3.11")

    def test_generate_load_config_parses_list_values(self):
        """generate.py load_config가 리스트 값(processes.enabled)을 파싱하는지 검증"""
        config = generate_load_config(self.config_path)

        self.assertIn("processes", config)
        self.assertIn("enabled", config["processes"])
        self.assertIsInstance(config["processes"]["enabled"], list)
        self.assertEqual(config["processes"]["enabled"], ["P0", "P1", "P3"])

    def test_generate_load_config_parses_boolean_values(self):
        """generate.py load_config가 boolean 값을 올바르게 파싱하는지 검증"""
        config = generate_load_config(self.config_path)

        self.assertIn("tools", config)
        self.assertIn("claude", config["tools"])
        self.assertIs(config["tools"]["claude"]["enabled"], True)
        self.assertIs(config["tools"]["claude"]["hook_enforcement"], True)
        self.assertIs(config["tools"]["codex"]["enabled"], False)

    def test_gatekeeper_load_config_parses_config(self):
        """gatekeeper.py load_config가 설정을 파싱하는지 검증"""
        config = gatekeeper_load_config(self.config_path)

        # gatekeeper load_config merges defaults with file content
        self.assertIn("records_dir", config)
        self.assertIn("skills_dir", config)
        self.assertIn("gatekeeper", config)

    def test_yaml_with_special_characters(self):
        """특수 문자가 포함된 YAML 파싱 검증"""
        special_yaml = '''project:
  name: "프로젝트-한글"
  description: 'Description with single quotes and "double quotes"'
'''
        special_path = pathlib.Path(self.temp_dir) / "special.yaml"
        special_path.write_text(special_yaml, encoding="utf-8")

        config = generate_load_config(special_path)
        self.assertEqual(config["project"]["name"], "프로젝트-한글")

    def test_yaml_with_multiline_string(self):
        """여러 줄 문자열이 포함된 YAML 파싱 검증 (PyYAML 고유 기능)"""
        multiline_yaml = '''project:
  name: "test"
  description: |
    This is a multiline
    description that spans
    multiple lines.
'''
        multiline_path = pathlib.Path(self.temp_dir) / "multiline.yaml"
        multiline_path.write_text(multiline_yaml, encoding="utf-8")

        config = generate_load_config(multiline_path)
        self.assertIn("multiple lines", config["project"]["description"])


class TestYAMLParsingEdgeCases(unittest.TestCase):
    """엣지 케이스 테스트"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_empty_list_parsing(self):
        """빈 리스트 파싱 검증"""
        yaml_content = '''processes:
  enabled: []
'''
        path = pathlib.Path(self.temp_dir) / "empty_list.yaml"
        path.write_text(yaml_content, encoding="utf-8")

        config = generate_load_config(path)
        self.assertEqual(config["processes"]["enabled"], [])

    def test_null_value_parsing(self):
        """null 값 파싱 검증"""
        yaml_content = '''project:
  name: "test"
  description: null
'''
        path = pathlib.Path(self.temp_dir) / "null_value.yaml"
        path.write_text(yaml_content, encoding="utf-8")

        config = generate_load_config(path)
        self.assertIsNone(config["project"]["description"])

    def test_numeric_value_parsing(self):
        """숫자 값 파싱 검증"""
        yaml_content = '''settings:
  timeout: 30
  ratio: 0.5
'''
        path = pathlib.Path(self.temp_dir) / "numeric.yaml"
        path.write_text(yaml_content, encoding="utf-8")

        config = generate_load_config(path)
        self.assertEqual(config["settings"]["timeout"], 30)
        self.assertEqual(config["settings"]["ratio"], 0.5)


if __name__ == "__main__":
    unittest.main()
