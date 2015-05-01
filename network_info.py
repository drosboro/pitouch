import subprocess

def network_info():
  essid = subprocess.check_output(["iwgetid", "-r"]).strip()
  txt = "SSID: " + essid

  ip_addr = subprocess.check_output(["hostname", "-I"]).strip()
  txt += "\nIP: " + ip_addr

  return txt