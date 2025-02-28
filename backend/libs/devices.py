from core.database import get_db


def get_devices():
    db = get_db().cursor()
    db.execute("select * from devices")

    devices = []
    while (row := db.fetchone()):
        data = {"hostname": row[0], "mac": row[1], "interface": row[2]}
        devices.append(data)

    return devices
