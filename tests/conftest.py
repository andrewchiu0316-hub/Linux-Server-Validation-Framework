from __future__ import annotations

import pytest

from framework.diagnostics import collect_diagnostics


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        area = getattr(item, "validation_area", "general")
        service = getattr(item, "service_name", None)
        path = collect_diagnostics(area, str(report.longrepr), service)
        report.user_properties.append(("diagnostics", str(path)))


@pytest.hookimpl(trylast=True)
def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when != "call":
        return
    label = report.nodeid.split("::")[-1].replace("test_", "").replace("_", " ").title()
    for acronym in ("Cpu", "Os", "Cpp", "Tcp"):
        label = label.replace(acronym, acronym.upper())
    if report.passed:
        print(f"[PASS] {label}")
    elif report.failed:
        print(f"[FAIL] {label}\nReason: {report.longreprtext.splitlines()[-1]}")
