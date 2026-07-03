from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_smoke_check_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "smoke_check.py"
    spec = importlib.util.spec_from_file_location("smoke_check", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_smoke_check_main_reports_expected_lines(capsys) -> None:
    smoke_check = _load_smoke_check_module()

    assert smoke_check.main() == 0

    output = capsys.readouterr().out
    assert "smoke_check_status=pass" in output
    assert "generated_demo_verdict=valid" in output
    assert "validation_roundtrip_verdict=valid" in output
    assert "cross_run_bundle_verdict=invalid" in output
    assert "summary_failed_checks_present=true" in output
