import pytest
import json


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    x = yield
    x._result.weight = getattr(item._obj, "weight", 0)
    x._result.number = getattr(item._obj, "number", None)
    x._result.visibility = getattr(item._obj, "visibility", "visible")
    x._result.hide_errors = getattr(item._obj, "hide_errors", None)
    x._result.tags = getattr(item._obj, "tags", [])
    x._result.leaderboard_column = getattr(item._obj, "leaderboard_column", None)
    x._result.leaderboard_sort_order = getattr(
        item._obj, "leaderboard_sort_order", "desc"
    )
    x._result.leaderboard_value = getattr(item._obj, "leaderboard_value", None)
    x._result.score = getattr(item._obj, "score", None)


def build_report(test):
    result = {
        "name": test.location[2],
        "status": test.outcome,
        "score": 0,
        "max_score": test.weight,
        "output": "",
        "tags": test.tags,
        "visibility": test.visibility,
    }

    if test.score is None:
        result["score"] = test.weight
    else:
        result["score"] = test.score

    if test.outcome == "failed":
        if test.hide_errors:
            result["output"] = test.hide_errors
        else:
            result["output"] = str(test.longrepr.chain[0][0].reprentries[0])

    if test.number is not None:
        result["number"] = test.number

    return result


def build_leaderboard(test):
    if test.leaderboard_column is None or test.leaderboard_value is None:
        return None

    leaderboard = {
        "column_name": test.leaderboard_column,
        "sort_order": test.leaderboard_sort_order,
        "value": test.leaderboard_value,
    }

    return leaderboard


def pytest_terminal_summary(terminalreporter, exitstatus):
    json_results = {"tests": [], "leaderboard": []}

    all_tests = []
    if "passed" in terminalreporter.stats:
        all_tests = all_tests + terminalreporter.stats["passed"]
    if "failed" in terminalreporter.stats:
        all_tests = all_tests + terminalreporter.stats["failed"]

    for s in all_tests:
        test = s
        report = build_report(test)
        leaderboard = build_leaderboard(test)
        json_results["tests"].append(report)
        if leaderboard:
            json_results["leaderboard"].append(leaderboard)

    with open("results.json", "w") as results:
        results.write(json.dumps(json_results, indent=4))
