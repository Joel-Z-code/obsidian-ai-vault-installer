# -*- coding: utf-8 -*-
"""Tests for the Vault generator in skills/.../scripts/create_vault.py.

They focus on the installer's safety contract: it only writes inside the
target Vault, never deletes, never overwrites existing files, and reports a
passing self-test for a freshly created Vault.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "obsidian-ai-vault-installer" / "scripts" / "create_vault.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("create_vault", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def cv():
    module = _load_module()
    yield module
    sys.modules.pop("create_vault", None)


def run(cv, argv):
    return cv.create_vault(cv.build_parser().parse_args(argv))


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_creates_valid_vault(cv, tmp_path, capsys):
    code = run(cv, ["--base-dir", str(tmp_path), "--vault-name", "AI知识库"])
    result = json.loads(capsys.readouterr().out)

    assert code == 0
    assert result["status"] == "ok"
    assert result["validation_errors"] == []
    assert result["skipped_existing_files"] == 0
    assert result["created_files"] > 0

    root = Path(result["vault_path"])
    assert root == (tmp_path / "AI知识库")
    for rel in ["AGENTS.md", "CLAUDE.md", "README.md", "00 收件箱/README.md", "Clippings/README.md"]:
        assert (root / rel).is_file()
    for rel in ["09 image", "10 About me", "05 工具箱/Templates", "06 计划/04 每日记录"]:
        assert (root / rel).is_dir()
    assert (root / "07 系统方法/安装完成报告.md").is_file()
    assert "自测结果：通过" in (root / "07 系统方法/MVP自测报告.md").read_text(encoding="utf-8")


def test_generated_jsonl_indexes_are_parseable(cv, tmp_path, capsys):
    run(cv, ["--base-dir", str(tmp_path), "--vault-name", "v"])
    root = Path(json.loads(capsys.readouterr().out)["vault_path"])

    indexes = sorted(p.relative_to(root).as_posix() for p in root.rglob("*.jsonl"))
    assert "00 收件箱/inbox_index.jsonl" in indexes
    assert "06 计划/04 每日记录/daily_log.jsonl" in indexes
    for rel in indexes:
        rows = read_jsonl(root / rel)
        assert rows
        assert all(set(row) >= {"time", "task", "status"} for row in rows)


def test_second_run_on_same_base_dir_creates_a_sibling_vault(cv, tmp_path, capsys):
    run(cv, ["--base-dir", str(tmp_path), "--vault-name", "v"])
    first = Path(json.loads(capsys.readouterr().out)["vault_path"])
    (first / "AGENTS.md").write_text("user edit", encoding="utf-8")

    run(cv, ["--base-dir", str(tmp_path), "--vault-name", "v"])
    second = Path(json.loads(capsys.readouterr().out)["vault_path"])

    assert second != first
    assert second.name.startswith("v-")
    assert (first / "AGENTS.md").read_text(encoding="utf-8") == "user edit"


def test_existing_target_without_supplement_is_not_touched(cv, tmp_path, capsys):
    target = tmp_path / "vault"
    target.mkdir()
    (target / "notes.md").write_text("my notes", encoding="utf-8")

    code = run(cv, ["--target", str(target)])
    result = json.loads(capsys.readouterr().out)

    assert code == 0
    assert Path(result["vault_path"]) != target
    assert sorted(p.name for p in target.iterdir()) == ["notes.md"]
    assert (target / "notes.md").read_text(encoding="utf-8") == "my notes"


def test_supplement_existing_only_adds_missing_files(cv, tmp_path, capsys):
    target = tmp_path / "vault"
    (target / "00 收件箱").mkdir(parents=True)
    (target / "AGENTS.md").write_text("keep me", encoding="utf-8")
    (target / "00 收件箱/inbox_index.jsonl").write_text(
        json.dumps({"time": "t", "task": "kept", "status": "done"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    code = run(cv, ["--target", str(target), "--supplement-existing"])
    result = json.loads(capsys.readouterr().out)

    assert code == 0
    assert Path(result["vault_path"]) == target
    assert result["skipped_existing_files"] == 2
    assert (target / "AGENTS.md").read_text(encoding="utf-8") == "keep me"
    assert [row["task"] for row in read_jsonl(target / "00 收件箱/inbox_index.jsonl")] == ["kept"]
    assert (target / "CLAUDE.md").is_file()
    assert (target / "07 系统方法/工作流-收件箱处理.md").is_file()


def test_validate_vault_reports_missing_files_and_broken_jsonl(cv, tmp_path, capsys):
    run(cv, ["--base-dir", str(tmp_path), "--vault-name", "v"])
    root = Path(json.loads(capsys.readouterr().out)["vault_path"])

    assert cv.validate_vault(root) == (True, [])

    (root / "CLAUDE.md").unlink()
    (root / "02 选题管理/topics_index.jsonl").write_text("{not json}\n", encoding="utf-8")
    ok, errors = cv.validate_vault(root)

    assert not ok
    assert "missing: CLAUDE.md" in errors
    assert any("topics_index.jsonl:1" in err for err in errors)


def test_unique_target_appends_timestamp_only_when_taken(cv, tmp_path):
    assert cv.unique_target(tmp_path, "v") == (tmp_path / "v").resolve()

    (tmp_path / "v").mkdir()
    fallback = cv.unique_target(tmp_path, "v")

    assert fallback != (tmp_path / "v").resolve()
    assert fallback.name.startswith("v-")
