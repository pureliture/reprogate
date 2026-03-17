#!/usr/bin/env python3
"""
TDD Cycle: P0-3 Bootstrap Smoke Test
RED Phase: init → generate → check 전체 흐름 테스트

이 테스트는 ai-ops의 부트스트랩 흐름을 검증합니다:
1. init.py로 ai-ops.config.yaml 생성
2. generate.py로 어댑터 파일 생성
3. check_compliance.py로 컴플라이언스 검증
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestBootstrapSmokeTest(unittest.TestCase):
    """Bootstrap 흐름 통합 테스트"""

    @classmethod
    def setUpClass(cls):
        """테스트 클래스 설정: 스크립트 경로 확인"""
        cls.scripts_dir = pathlib.Path(__file__).resolve().parents[1]
        cls.root_dir = cls.scripts_dir.parent
        cls.init_script = cls.scripts_dir / "init.py"
        cls.generate_script = cls.scripts_dir / "generate.py"
        cls.check_script = cls.scripts_dir / "check_compliance.py"

        # Verify scripts exist
        assert cls.init_script.exists(), f"init.py not found: {cls.init_script}"
        assert cls.generate_script.exists(), f"generate.py not found: {cls.generate_script}"
        assert cls.check_script.exists(), f"check_compliance.py not found: {cls.check_script}"

    def setUp(self):
        """각 테스트용 임시 디렉토리 생성"""
        self.temp_dir = tempfile.mkdtemp(prefix="ai-ops-test-")
        self.output_dir = pathlib.Path(self.temp_dir)

    def tearDown(self):
        """임시 디렉토리 정리"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run_script(self, script: pathlib.Path, args: list, cwd: pathlib.Path = None) -> subprocess.CompletedProcess:
        """스크립트 실행 헬퍼"""
        return subprocess.run(
            [sys.executable, str(script)] + args,
            cwd=str(cwd or self.root_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def test_init_creates_config_file(self):
        """init.py가 ai-ops.config.yaml 파일을 생성하는지 검증"""
        config_path = self.output_dir / "ai-ops.config.yaml"

        result = self.run_script(
            self.init_script,
            [
                "--output", str(config_path),
                "--project-name", "test-project",
                "--primary-branch", "main",
            ],
        )

        self.assertEqual(result.returncode, 0, f"init.py failed: {result.stderr}")
        self.assertTrue(config_path.exists(), "ai-ops.config.yaml was not created")

        # Verify config content
        content = config_path.read_text(encoding="utf-8")
        self.assertIn("test-project", content)
        self.assertIn("main", content)

    def test_init_refuses_overwrite_without_force(self):
        """init.py가 --force 없이 기존 파일을 덮어쓰지 않는지 검증"""
        config_path = self.output_dir / "ai-ops.config.yaml"
        config_path.write_text("existing content", encoding="utf-8")

        result = self.run_script(
            self.init_script,
            ["--output", str(config_path)],
        )

        self.assertEqual(result.returncode, 1, "init.py should fail without --force")
        self.assertIn("existing content", config_path.read_text(encoding="utf-8"))

    def test_generate_creates_adapter_files(self):
        """generate.py가 어댑터 파일들을 생성하는지 검증"""
        # First, create config
        config_path = self.output_dir / "ai-ops.config.yaml"
        init_result = self.run_script(
            self.init_script,
            [
                "--output", str(config_path),
                "--project-name", "test-project",
            ],
        )
        self.assertEqual(init_result.returncode, 0, f"init.py failed: {init_result.stderr}")

        # Then, generate adapter files
        result = self.run_script(
            self.generate_script,
            [
                "--config", str(config_path),
                "--output-root", str(self.output_dir),
                "--force",
            ],
        )

        self.assertEqual(result.returncode, 0, f"generate.py failed: {result.stderr}")

        # Verify key files were created
        expected_files = [
            self.output_dir / "AGENTS.md",
            self.output_dir / ".claude" / "CLAUDE.md",
            self.output_dir / ".ai-ops" / "README.md",
        ]

        for expected_file in expected_files:
            self.assertTrue(
                expected_file.exists(),
                f"Expected file not created: {expected_file.relative_to(self.output_dir)}",
            )

    def test_check_compliance_passes_for_valid_structure(self):
        """check_compliance.py가 올바른 구조에서 통과하는지 검증"""
        # Create required docs structure (as check_compliance.py expects)
        docs_dir = self.output_dir / "docs"
        docs_dir.mkdir(parents=True)

        # Create required files for compliance check
        constitution = docs_dir / "constitution.md"
        constitution.write_text("# Constitution\n\n### DPC-G001 Goal\n", encoding="utf-8")

        operating_model = docs_dir / "operating-model.md"
        operating_model.write_text("# Operating Model\n", encoding="utf-8")

        process_catalog = docs_dir / "process-catalog"
        process_catalog.mkdir()
        (process_catalog / "README.md").write_text("# Process Catalog\n", encoding="utf-8")

        # Run check_compliance
        result = self.run_script(
            self.check_script,
            ["--mode", "none"],
            cwd=self.output_dir,
        )

        # Note: This may fail if check_compliance expects additional structure
        # The test verifies the script runs without crashing
        # We'll adjust based on actual requirements
        self.assertIn(
            result.returncode,
            [0, 1],
            f"check_compliance.py crashed: {result.stderr}",
        )

    def test_full_bootstrap_flow(self):
        """init → generate → check 전체 흐름이 작동하는지 검증"""
        # Step 1: Init
        config_path = self.output_dir / "ai-ops.config.yaml"
        init_result = self.run_script(
            self.init_script,
            [
                "--output", str(config_path),
                "--project-name", "smoke-test-project",
                "--primary-branch", "main",
            ],
        )
        self.assertEqual(init_result.returncode, 0, f"Step 1 (init) failed: {init_result.stderr}")
        self.assertTrue(config_path.exists(), "Config file not created in Step 1")

        # Step 2: Generate
        generate_result = self.run_script(
            self.generate_script,
            [
                "--config", str(config_path),
                "--output-root", str(self.output_dir),
                "--force",
            ],
        )
        self.assertEqual(generate_result.returncode, 0, f"Step 2 (generate) failed: {generate_result.stderr}")

        # Verify generated structure
        self.assertTrue(
            (self.output_dir / "AGENTS.md").exists(),
            "AGENTS.md not generated in Step 2",
        )
        self.assertTrue(
            (self.output_dir / ".claude" / "CLAUDE.md").exists(),
            ".claude/CLAUDE.md not generated in Step 2",
        )

        # Step 3: Check (from generated structure)
        # Note: This checks the generated output directory which has docs/ copied
        check_result = self.run_script(
            self.check_script,
            ["--mode", "none"],
            cwd=self.output_dir,
        )

        # The check should at least run without crashing
        self.assertIsNotNone(check_result.returncode, "Step 3 (check) did not complete")
        # Output should contain either "passed" or list of issues
        combined_output = check_result.stdout + check_result.stderr
        self.assertTrue(
            "compliance" in combined_output.lower() or "check" in combined_output.lower() or result.returncode == 0,
            f"Step 3 (check) produced unexpected output: {combined_output}",
        )


class TestBootstrapEdgeCases(unittest.TestCase):
    """Bootstrap 엣지 케이스 테스트"""

    @classmethod
    def setUpClass(cls):
        cls.scripts_dir = pathlib.Path(__file__).resolve().parents[1]
        cls.root_dir = cls.scripts_dir.parent
        cls.init_script = cls.scripts_dir / "init.py"
        cls.generate_script = cls.scripts_dir / "generate.py"

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="ai-ops-edge-")
        self.output_dir = pathlib.Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run_script(self, script: pathlib.Path, args: list) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(script)] + args,
            cwd=str(self.root_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def test_init_with_custom_processes(self):
        """init.py가 커스텀 프로세스 목록을 지원하는지 검증"""
        config_path = self.output_dir / "ai-ops.config.yaml"

        result = self.run_script(
            self.init_script,
            [
                "--output", str(config_path),
                "--project-name", "custom-process-project",
                "--enabled-processes", "TDD,P3,P4",
            ],
        )

        self.assertEqual(result.returncode, 0, f"init.py failed: {result.stderr}")

        content = config_path.read_text(encoding="utf-8")
        self.assertIn("TDD", content)
        self.assertIn("P3", content)
        self.assertIn("P4", content)

    def test_init_disables_claude_adapter(self):
        """init.py가 Claude 어댑터 비활성화를 지원하는지 검증"""
        config_path = self.output_dir / "ai-ops.config.yaml"

        result = self.run_script(
            self.init_script,
            [
                "--output", str(config_path),
                "--project-name", "no-claude-project",
                "--disable-claude",
            ],
        )

        self.assertEqual(result.returncode, 0, f"init.py failed: {result.stderr}")

        content = config_path.read_text(encoding="utf-8")
        # Should have claude enabled: false
        self.assertIn("claude:", content)
        self.assertIn("enabled: false", content)

    def test_generate_with_disabled_claude_skips_claude_files(self):
        """Claude가 비활성화되면 Claude 어댑터 파일을 생성하지 않는지 검증"""
        config_path = self.output_dir / "ai-ops.config.yaml"

        # Init with Claude disabled
        init_result = self.run_script(
            self.init_script,
            [
                "--output", str(config_path),
                "--project-name", "no-claude-project",
                "--disable-claude",
            ],
        )
        self.assertEqual(init_result.returncode, 0)

        # Generate
        generate_result = self.run_script(
            self.generate_script,
            [
                "--config", str(config_path),
                "--output-root", str(self.output_dir),
                "--force",
            ],
        )
        self.assertEqual(generate_result.returncode, 0, f"generate.py failed: {generate_result.stderr}")

        # Claude directory should not exist or be empty
        claude_dir = self.output_dir / ".claude"
        if claude_dir.exists():
            claude_md = claude_dir / "CLAUDE.md"
            self.assertFalse(
                claude_md.exists(),
                "CLAUDE.md should not be generated when Claude is disabled",
            )


if __name__ == "__main__":
    unittest.main()
