import subprocess
import re

def get_wifi_ip():
    # ipconfig 명령 실행
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    output = result.stdout

    # Wi-Fi 어댑터의 IPv4 주소만 추출
    match = re.search(r"무선 LAN 어댑터 Wi-Fi.*?IPv4 주소.*?: ([\d.]+)", output, re.DOTALL)
    if match:
        return match.group(1)
    return None