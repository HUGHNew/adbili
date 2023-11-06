"""
parameter:
serial: specify usb device
private: specify private key name
target: target direction to save songs
prompt: rename when copy
"""
import json
from typing import Callable
from functools import partial

from adb_shell.adb_device import AdbDevice
import fire

from constant import Bili, Music, Entry
from command import app_exist, collect_entries, get_audio_m4s
from utils import (
    get_default_device,
    get_default_signer,
    create_entry_from_json,
    get_line,
)
from filter import time_range_filter


def process_app(
    device: AdbDevice,
    appid: str,
    target: str,
    prompt: bool,
    filter_partial: Callable[[Entry], bool],
):
    tmp = "entry.tmp.json"
    entries_getter = collect_entries(appid)
    entries: list[str] = device.shell(entries_getter).splitlines()
    for entry_json in entries:
        device.pull(entry_json, tmp)
        with open(tmp) as tf:
            entry = create_entry_from_json(json.load(tf))
        audio_file = get_audio_m4s(entry_json, entry.type_tag)

        if not filter_partial(entry):
            continue  # apply filter
        dest = entry.title
        if prompt:
            opt = get_line(f"audio name: [{entry.title}] (Press , to skip) ")
            if opt == ",":
                continue
            elif not opt.isspace():
                dest = opt
        cp_cmd = f"cp {audio_file} {target}/{dest}.mp3"
        device.shell(cp_cmd)
        print("[Done]", cp_cmd)


def main(
    serial: str = None,
    target: str = Music,
    private: str = "./key", # 
    prompt: bool = True,
    app: str = None,  # app filter
):
    if app:
        assert app in Bili, f"Unknown appId: {app}. It is not in {Bili}"
    device = get_default_device(serial)
    avail = device.connect(rsa_keys=get_default_signer(private))
    if not avail:
        print("connecting error")
        return
    for appid in Bili:
        if app and appid != app:
            continue
        result = device.shell(app_exist(appid))
        if not result:
            process_app(
                device,
                appid,
                target,
                prompt,
                partial(time_range_filter, min_sec=1 * 60, max_sec=5 * 60),
            )
    device.close()

if __name__ == "__main__":
    fire.Fire(main)
