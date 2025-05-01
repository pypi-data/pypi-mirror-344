import readline

from adbili.constant import Entry

def time_range_filter(entry: Entry, min_sec:int, max_sec:int,) -> bool:
    return min_sec < entry.total_time_milli/1000 < max_sec

def create_entry_from_json(js: dict) -> Entry:
    return Entry(
        title=js["title"],
        type_tag=js["type_tag"],
        total_time_milli=js["total_time_milli"],
        owner_id=js["owner_id"],
        cid=js["page_data"]["cid"],
        # part=js["page_data"]["part"], # for Google Play
    )


def get_line(prompt: str) -> str:
    return input(prompt)
