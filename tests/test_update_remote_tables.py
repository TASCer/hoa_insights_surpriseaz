from hoa_insights_surpriseaz.database import update_remote_tables
from hoa_insights_surpriseaz.my_secrets import (
    test_bluehost_uri,
    test_debian_uri,
    test_bluehost_dbname,
)
from pathlib import Path
# from hoa_insights_surpriseaz.main import 
# TODO FINISH THIS
def test_update_remote_tables() -> None:
    p: Path = Path.cwd().parent / "hoa_insights_surpriseaz" / "src" / "hoa_insights_surpriseaz" / "output" / "csv" / "financial" 
    # assert p is type(Path())
    assert (
        update_remote_tables.all(
            file_path=p, local_db=test_debian_uri, remote_db=test_bluehost_uri
        )
        is None
    )
