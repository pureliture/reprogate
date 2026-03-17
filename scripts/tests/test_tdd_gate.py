#!/usr/bin/env python3
"""
TDD Cycle: P0-2 TDD Gate 구현
RED Phase: TDD Gate 테스트

TDD Gate는 테스트 파일 없이 구현 코드를 작성하려 할 때 차단합니다.
- 구현 파일 작성 시 → 해당 테스트 파일 존재 여부 확인
- 테스트 파일 작성 시 → 항상 허용
- TDD 모드가 비활성화되어 있으면 → 차단하지 않음
"""
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from hooks.claude_pretooluse_guard import (
    is_test_file,
    find_corresponding_test,
    should_enforce_tdd_gate,
    check_tdd_gate,
)


class TestIsTestFile(unittest.TestCase):
    """테스트 파일 판별 테스트"""

    def test_python_test_file_with_test_prefix(self):
        """test_ 접두사가 있는 Python 파일은 테스트 파일"""
        self.assertTrue(is_test_file("test_example.py"))
        self.assertTrue(is_test_file("tests/test_example.py"))
        self.assertTrue(is_test_file("src/tests/test_module.py"))

    def test_python_test_file_with_test_suffix(self):
        """_test 접미사가 있는 Python 파일은 테스트 파일"""
        self.assertTrue(is_test_file("example_test.py"))
        self.assertTrue(is_test_file("tests/module_test.py"))

    def test_python_implementation_file(self):
        """일반 Python 파일은 테스트 파일이 아님"""
        self.assertFalse(is_test_file("example.py"))
        self.assertFalse(is_test_file("src/module.py"))
        self.assertFalse(is_test_file("scripts/generate.py"))

    def test_javascript_test_file(self):
        """JavaScript/TypeScript 테스트 파일 판별"""
        self.assertTrue(is_test_file("example.test.js"))
        self.assertTrue(is_test_file("example.test.ts"))
        self.assertTrue(is_test_file("example.test.tsx"))
        self.assertTrue(is_test_file("example.spec.js"))
        self.assertTrue(is_test_file("example.spec.ts"))

    def test_javascript_implementation_file(self):
        """일반 JavaScript 파일은 테스트 파일이 아님"""
        self.assertFalse(is_test_file("example.js"))
        self.assertFalse(is_test_file("component.tsx"))

    def test_java_test_file(self):
        """Java 테스트 파일 판별"""
        self.assertTrue(is_test_file("ExampleTest.java"))
        self.assertTrue(is_test_file("src/test/java/ExampleTest.java"))

    def test_java_implementation_file(self):
        """일반 Java 파일은 테스트 파일이 아님"""
        self.assertFalse(is_test_file("Example.java"))
        self.assertFalse(is_test_file("src/main/java/Example.java"))

    def test_non_code_files(self):
        """코드가 아닌 파일은 테스트 파일이 아님"""
        self.assertFalse(is_test_file("README.md"))
        self.assertFalse(is_test_file("config.yaml"))
        self.assertFalse(is_test_file("data.json"))


class TestFindCorrespondingTest(unittest.TestCase):
    """대응하는 테스트 파일 찾기 테스트"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.root = pathlib.Path(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_find_python_test_with_test_prefix(self):
        """Python 구현 파일에 대응하는 test_ 접두사 테스트 파일 찾기"""
        # Setup: tests/test_module.py exists
        tests_dir = self.root / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_module.py").write_text("# test", encoding="utf-8")

        # Implementation file
        impl_path = self.root / "src" / "module.py"

        result = find_corresponding_test(str(impl_path), str(self.root))
        self.assertIsNotNone(result)
        self.assertIn("test_module.py", result)

    def test_find_python_test_with_same_directory(self):
        """같은 디렉토리에 있는 테스트 파일 찾기"""
        # Setup: src/test_module.py exists
        src_dir = self.root / "src"
        src_dir.mkdir()
        (src_dir / "test_module.py").write_text("# test", encoding="utf-8")

        impl_path = self.root / "src" / "module.py"

        result = find_corresponding_test(str(impl_path), str(self.root))
        self.assertIsNotNone(result)

    def test_find_javascript_test(self):
        """JavaScript 구현 파일에 대응하는 테스트 파일 찾기"""
        # Setup: component.test.tsx exists
        src_dir = self.root / "src"
        src_dir.mkdir()
        (src_dir / "component.test.tsx").write_text("// test", encoding="utf-8")

        impl_path = self.root / "src" / "component.tsx"

        result = find_corresponding_test(str(impl_path), str(self.root))
        self.assertIsNotNone(result)

    def test_no_corresponding_test_found(self):
        """대응하는 테스트 파일이 없는 경우"""
        impl_path = self.root / "src" / "module.py"

        result = find_corresponding_test(str(impl_path), str(self.root))
        self.assertIsNone(result)


class TestShouldEnforceTddGate(unittest.TestCase):
    """TDD Gate 적용 여부 판단 테스트"""

    def test_enforce_for_python_implementation(self):
        """Python 구현 파일에 대해 TDD Gate 적용"""
        self.assertTrue(should_enforce_tdd_gate("src/module.py"))

    def test_skip_for_test_file(self):
        """테스트 파일에 대해서는 TDD Gate 미적용"""
        self.assertFalse(should_enforce_tdd_gate("tests/test_module.py"))
        self.assertFalse(should_enforce_tdd_gate("component.test.tsx"))

    def test_skip_for_documentation(self):
        """문서 파일에 대해서는 TDD Gate 미적용"""
        self.assertFalse(should_enforce_tdd_gate("README.md"))
        self.assertFalse(should_enforce_tdd_gate("docs/guide.md"))

    def test_skip_for_config_files(self):
        """설정 파일에 대해서는 TDD Gate 미적용"""
        self.assertFalse(should_enforce_tdd_gate("config.yaml"))
        self.assertFalse(should_enforce_tdd_gate("package.json"))
        self.assertFalse(should_enforce_tdd_gate(".gitignore"))
        self.assertFalse(should_enforce_tdd_gate("requirements.txt"))

    def test_skip_for_init_files(self):
        """__init__.py 파일에 대해서는 TDD Gate 미적용"""
        self.assertFalse(should_enforce_tdd_gate("src/__init__.py"))


class TestCheckTddGate(unittest.TestCase):
    """TDD Gate 전체 검사 테스트"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.root = pathlib.Path(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_allow_when_test_exists(self):
        """테스트 파일이 존재하면 허용"""
        # Setup: test file exists
        tests_dir = self.root / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_module.py").write_text("# test", encoding="utf-8")

        impl_path = str(self.root / "src" / "module.py")

        allowed, reason = check_tdd_gate(impl_path, str(self.root), tdd_enabled=True)
        self.assertTrue(allowed)
        self.assertEqual(reason, "")

    def test_deny_when_no_test_exists(self):
        """테스트 파일이 없으면 차단"""
        impl_path = str(self.root / "src" / "module.py")

        allowed, reason = check_tdd_gate(impl_path, str(self.root), tdd_enabled=True)
        self.assertFalse(allowed)
        self.assertIn("TDD", reason)
        self.assertIn("test", reason.lower())

    def test_allow_when_tdd_disabled(self):
        """TDD 모드가 비활성화되면 허용"""
        impl_path = str(self.root / "src" / "module.py")

        allowed, reason = check_tdd_gate(impl_path, str(self.root), tdd_enabled=False)
        self.assertTrue(allowed)

    def test_allow_for_test_file(self):
        """테스트 파일 작성은 항상 허용"""
        test_path = str(self.root / "tests" / "test_module.py")

        allowed, reason = check_tdd_gate(test_path, str(self.root), tdd_enabled=True)
        self.assertTrue(allowed)

    def test_allow_for_non_code_file(self):
        """코드가 아닌 파일 작성은 허용"""
        doc_path = str(self.root / "README.md")

        allowed, reason = check_tdd_gate(doc_path, str(self.root), tdd_enabled=True)
        self.assertTrue(allowed)


if __name__ == "__main__":
    unittest.main()
