import argparse
import requests
import subprocess


class TorProxy:
    def __init__(self):
        self.comment = ""

    def get_comment(self):
        comment = argparse.ArgumentParser(
            description="This script use to make all network connection over tor"
        )
        comment.add_argument(
            "-c", type=str, metavar="comment", required=True, help="start or stop"
        )
        args = comment.parse_args()
        self.comment = (args.c).lower()

        if self.comment not in ["start", "stop"]:
            print(f"Unknow comment : {self.comment}. please check comment")
            exit()

    def get_ip_address(self):
        try:
            proxies = {
                "http": "socks5://localhost:9050",
                "https": "socks5://localhost:9050",
            }
            ip = requests.get("https://api.ipify.org", proxies=proxies).text
        except requests.ConnectionError:
            ip = requests.get("https://api.ipify.org").text
        return ip

    def check_tor_status(self):
        check_tor_info = subprocess.Popen(
            ["brew", "info", "tor"], stdout=subprocess.DEVNULL
        )
        if check_tor_info.wait() != 0:
            print("Tor not installed. Please try after tor installation")
            exit()

    def start_tor_service(self):
        print(f"Your IP address: {self.get_ip_address()}")
        print("Starting tor services...")
        start_tor_service = subprocess.Popen(
            ["brew", "services", "start", "tor"], stdout=subprocess.DEVNULL
        )
        if start_tor_service.wait() != 0:
            print("Something went wrong...")
            exit()
        else:
            print("Tor service started")

    def activate_network_proxy(self):
        # add tor proxy
        set_network_proxy = subprocess.Popen(
            ["networksetup", "-setsocksfirewallproxy", "wi-fi", "localhost", "9050"],
            stdout=subprocess.DEVNULL,
        )
        if set_network_proxy.wait() != 0:
            print("Something went wrong...")
        else:
            print("Tor Proxy added")

        # Turn on network with tor proxy
        connect_to_tor_proxy = subprocess.Popen(
            ["networksetup", "-setsocksfirewallproxystate", "wi-fi", "on"],
            stdout=subprocess.DEVNULL,
        )
        if connect_to_tor_proxy.wait() != 0:
            print("Something went wrong...")
        else:
            print("Connected to Tor proxy")
            print(f"Tor IP address: {self.get_ip_address()}")

    def deactivate_network_proxy(self):
        # Turn off network with tor proxy
        disconnect_tor_proxy = subprocess.Popen(
            ["networksetup", "-setsocksfirewallproxystate", "wi-fi", "off"],
            stdout=subprocess.DEVNULL,
        )
        if disconnect_tor_proxy.wait() != 0:
            print("Something went wrong...")
        else:
            print("Disconnected to Tor proxy")

    def stop_tor_service(self):
        print("Stopping tor services...")
        start_tor_service = subprocess.Popen(
            ["brew", "services", "stop", "tor"], stdout=subprocess.DEVNULL
        )
        if start_tor_service.wait() != 0:
            print("Something went wrong...")
        else:
            print("Tor service stopped")

    def tor_proxy(self):
        if self.comment == "start":
            self.start_tor_service()
            self.activate_network_proxy()
        else:
            self.deactivate_network_proxy()
            self.stop_tor_service()


if __name__ == "__main__":
    tor_proxy = TorProxy()
    tor_proxy.get_comment()
    tor_proxy.check_tor_status()
    tor_proxy.tor_proxy()
