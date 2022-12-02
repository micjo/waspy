from typing import Dict, List

from db.db_orm import get_entry_from_daybook, add_account_entry, get_daybook_all_formats, update_account_format


def add_daybook_routes(router):
    @router.get("/daybook/entry")
    async def get_daybook(account:str, nr_of_entries=1):
        return get_entry_from_daybook(account, nr_of_entries)

    @router.post("/daybook/entry")
    async def post_daybook(account: str,entry: Dict):
        return add_account_entry(account, entry)

    @router.post("/daybook/format")
    async def post_daybook_format(account: str, format: List):
        update_account_format(account, format)

    @router.get("/daybook/format")
    async def get_daybook_formats():
        return get_daybook_all_formats()

