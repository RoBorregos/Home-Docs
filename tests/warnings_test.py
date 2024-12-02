import os


class TestWarnings:
    # Check if strict build failed
    def test_no_warnings(self):
        result = os.popen(
            f"{os.sys.executable} -m mkdocs build --strict").read()
        assert "Aborted" not in result, "mkdocs build aborted with warnings"
