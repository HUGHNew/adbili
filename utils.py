import os
import readline

from constant import Entry
from adb_shell.adb_device import AdbDeviceUsb
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

from constant import Entry


def get_default_signer(priv_name="./key"):
    if not os.path.exists(priv_name):
        keygen(priv_name)
        os.chmod(priv_name, 0o400)

    with open(priv_name) as f:
        priv = f.read()
    with open(priv_name + ".pub") as f:
        pub = f.read()
    signer = PythonRSASigner(pub, priv)
    return [signer]


def get_default_device(serial: str = None):
    return AdbDeviceUsb(serial)


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
