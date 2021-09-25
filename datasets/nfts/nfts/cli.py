from moonstreamdb.db import yield_db_session_ctx

from .materialize import get_rows, EventType

if __name__ == "__main__":
    with yield_db_session_ctx() as db_session:
        rows = get_rows(db_session, EventType.TRANSFER)
        for row in rows:
            print(row)
