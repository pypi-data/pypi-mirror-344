[allure-pytest](https://pypi.org/project/allure-pytest/) only reports tests that were attempted

If a test case does not run (because the runner set up failed or because a CI job timed out on a previous test), the test case will be omitted from Allure Report.

This plugin creates default ["unknown" status](https://allurereport.org/docs/test-statuses/#unknown) results for each test case that's expected to run. After the tests run, the default result can be included for any test case that does not have an actual test result—so that those test cases show up as "unknown" in the Allure Report.

For example, to merge the actual test results with the default "unknown" results:
```python
import dataclasses
import json
import pathlib


@dataclasses.dataclass(frozen=True)
class Result:
    test_case_id: str
    path: pathlib.Path

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.test_case_id == other.test_case_id


actual_results = pathlib.Path("allure-results")
default_results = pathlib.Path("allure-default-results")

results: dict[pathlib.Path, set[Result]] = {
    actual_results: set(),
    default_results: set(),
}
for directory, results_ in results.items():
    for path in directory.glob("*-result.json"):
        with path.open("r") as file:
            id_ = json.load(file)["testCaseId"]
        results_.add(Result(id_, path))

actual_results.mkdir(exist_ok=True)

missing_results = results[default_results] - results[actual_results]
for default_result in missing_results:
    # Move to `actual_results` directory
    default_result.path.rename(actual_results / default_result.path.name)
```

As of 2025-01-31, the "unknown" status is not used by the allure-pytest adapter.

Upstream feature request to replace this plugin: https://github.com/allure-framework/allure-python/issues/821

## Usage
Generate default results
```
pytest --allure-default-dir=allure-default-results
```
