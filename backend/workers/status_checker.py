import subprocess
import threading

from wakeonlan import send_magic_packet

import nmap
import paramiko


class StatusChecker:

    def __init__(self, network: str):
        self.devices = []
        self.mapping = {}
        self.devices_status = {}
        self.network = network
        self.running = False


    def run(self):
        self.check_status()
        threading.Timer(10, self.run).start()


    def check_status(self):
        """
        Check if device is up using arp table of the router.
        :param mac: mac address of the given device
        :param config: config of the project
        :return: True if device is up, False otherwise
        """

        for device in self.devices:
            # Scan network if mac previously not found in the ARP table
            if not self.mapping[device.mac]:
                self.scan()

        try:
            result = subprocess.run(['ip', 'neigh'], capture_output=True, text=True, check=True)

            # Get all mac of managed devices
            targeted_mac = [device.mac for device in self.devices]
            for line in result.stdout.strip().split('\n'):
                if len(targeted_mac) == 0:
                    break

                if line:
                    parts = line.split()

                    # Get only [IP_ADDRESS dev INTERFACE lladdr MAC_ADDRESS STATE] format
                    if len(parts) >= 4:
                        # Check if target is a managed device
                        mac = parts[4] if len(parts) > 4 and parts[3] == "lladdr" else ""

                        if mac and mac in targeted_mac:
                            status = parts[-1] if len(parts) > 5 else ""

                            # Store mac along its IP
                            ip = parts[0]
                            self.mapping[mac] = ip

                            # Check for status
                            self.devices_status[mac] = True if status == "REACHABLE" else False
                            targeted_mac.remove(mac)

            # mac not in ARP table
            for mac in targeted_mac:
                self.devices_status[mac] = False
                self.mapping[mac] = None

        except subprocess.CalledProcessError:
            return


    def scan(self):
        """
        Scan network using nmap to fill arp table.
        """
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=self.network, arguments='-sn -PE')
        except nmap.PortScannerError:
            return
