from .constant import AndroidData, EntryJson, AudioFile


def app_exist(appid: str):
    return f"[ -e {AndroidData}/{appid} ] || echo NO"


def list_download(appid: str):
    return f"ls {AndroidData}/{appid}/download"


def list_cid(appid: str, avid: str):
    return f"ls {AndroidData}/{appid}/download/{avid}"


def get_entry_json(appid: str, avid: str, cid: str):
    return f"{AndroidData}/{appid}/{avid}/{cid}/{EntryJson}"


def collect_entries(appid: str):
    return f"ls {AndroidData}/{appid}/download/*/*/{EntryJson}"

def get_audio_m4s(entry: str, tag: str):
    entry_dir = entry[: -len(EntryJson)]
    audio_file = f"{entry_dir}{tag}/{AudioFile}"
    return audio_file
