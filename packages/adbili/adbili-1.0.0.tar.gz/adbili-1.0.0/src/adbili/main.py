import json
from typing import Callable
from functools import partial

from adbili.constant import Bili, Music, Entry
from adbili.command import app_exist, collect_entries, get_audio_m4s, list_download, list_cid
from adbili.utils import (
    create_entry_from_json,
    get_line,
    time_range_filter,
)
from adbili import devices


def process_app(
    device: devices.IDevice,
    appid: str,
    target: str,
    prompt: bool,
    recursive: bool,
    filter_partial: Callable[[Entry], bool],
):
    cmd_list_download = list_download(appid)
    items = device.run(cmd_list_download).splitlines()
    # breakpoint()
    for avid in items:
        cmd_ls_item = list_cid(appid, avid)
        item_entry = device.run(cmd_ls_item).splitlines()
        if len(item_entry) > 1 and not recursive:
            continue
        for ep in item_entry:
            entry_json_file = f"{cmd_ls_item.split()[-1]}/{ep}/entry.json"
            entry_json = device.run(f"cat {entry_json_file}")
            entry = create_entry_from_json(json.loads(entry_json))
            audio_file = get_audio_m4s(entry_json_file, entry.type_tag)
            if not filter_partial(entry):
                continue  # apply filter
            dest = entry.title.strip()
            if prompt:
                opt = get_line(f"audio name: [{entry.title}] (Press , to skip) ")
                if opt == ",":
                    continue
                elif not opt.isspace():
                    dest = opt
            cp_cmd = f"cp {audio_file} {target}/{dest}.mp3"
            device.run(cp_cmd)
            print("[Done]", cp_cmd)

def app(
    host: str = "",
    port: int = 0,
    target: str = Music,
    prompt: bool = True,
    app: str | None = None,  # app filter
    recursive: bool = False, # allow video collection
):
    assert app in Bili, f"Unknown appId: {app}. It is not in {Bili}"
    with devices.open(host, port) as device:
        result = device.run(app_exist(app))
        if result:
            print(f"[{app}] not exists")
            return
        process_app(
            device,
            app,
            target,
            prompt,
            recursive,
            partial(time_range_filter, min_sec=1 * 60, max_sec=5 * 60),
        )
