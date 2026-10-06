"""Pytest hooks for readable terminal output."""

from __future__ import annotations

import pytest


def pytest_runtest_setup(item: pytest.Item) -> None:
    print(f"\n>>> Running: {item.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> None:
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    if report.passed:
        print(f"<<< Status: PASS — {item.name}")
    elif report.failed:
        print(f"<<< Status: FAIL — {item.name}")
        detail = str(report.longrepr).strip().split("\n")[-1]
        print(f"    Detail: {detail}")
    elif report.skipped:
        print(f"<<< Status: SKIP — {item.name}")
