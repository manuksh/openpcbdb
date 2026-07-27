# IO storage API

The IO layer separates API behavior from physical storage.

Today OpenPCBDB uses JSON files because they are friendly to AI agents, git,
and human review. Later the same API can be backed by SQLite or binary storage.

::: openpcbdb.io.store.DbStore

::: openpcbdb.io.jsonDb
