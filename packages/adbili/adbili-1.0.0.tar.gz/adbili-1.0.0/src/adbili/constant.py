from dataclasses import dataclass

TimeoutSecond = 5 # 5s for timeout

Bili = [
    "tv.danmaku.bili", # Bilibili CN
    "com.bilibili.app.in", # Bilibili Google Play
]

PrimaryRoot = "/storage/emulated/0"
AndroidData = "/storage/emulated/0/Android/data"
EntryJson = "entry.json"
AudioFile = "audio.m4s"
Music = "/storage/emulated/0/Music"

@dataclass
class Entry:
    title: str
    type_tag: str
    total_time_milli: int
    owner_id: int # CN does not have owner_name
    cid: int
    # part: str # CN do not support it
