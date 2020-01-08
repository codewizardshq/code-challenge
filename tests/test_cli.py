import pytest

import CodeChallenge


@pytest.mark.skip(reason="broken")
def test_init_db(app):
    runner = app.test_cli_runner()
    result = runner.invoke(CodeChallenge.db_cli_bp.initdb_cmd)
    assert result.exit_code == 0
    assert result.output == "database initialized"
