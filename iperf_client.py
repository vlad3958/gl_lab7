import subprocess
import sys
import re


server_ip = "192.168.0.169"


def client(server_ip):
    """
    Виконує команду iperf3 як клієнт, повертає stdout та stderr.
    """
    try:
        # запускаємо iperf3
        process = subprocess.Popen(
            [r"C:\Users\Влад\Downloads\iperf3.1.1_32\iperf3.exe", "-c", server_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        return stdout, stderr

    except Exception as e:
        return "", str(e)


def parser(raw_output):
    """
    Парсить вивід iperf3 клієнта.
    Повертає список словників:
    [
        {"Interval": "1.00-2.00", "Transfer": 3.91, "Bitrate": 32.8, "Retr": 0, "Cwnd": 320.0},
        ...
    ]
    """

    intervals = []

    # регулярка для рядків iperf інтервалів (підходить під більшість версій iperf3)
    pattern = r"\s*(\d+\.\d+-\d+\.\d+)\s+sec\s+([\d\.]+)\s+MBytes\s+([\d\.]+)\s+Mbits/sec\s+(\d+)\s+([\d\.]+)"

    for match in re.finditer(pattern, raw_output):
        interval, transfer, bitrate, retr, cwnd = match.groups()

        intervals.append({
            "Interval": interval,
            "Transfer": float(transfer),
            "Bitrate": float(bitrate),
            "Retr": float(retr),
            "Cwnd": float(cwnd)
        })

    return intervals


# ---------------- MAIN SCRIPT -------------------

result, error = client(server_ip)

print("=== RAW OUTPUT ===")
print(result)
print("=== END RAW OUTPUT ===")


if error:
    print("Помилка підключення або виконання команди:")
    print(error)
    sys.exit(1)

# Парсимо результат
intervals = parser(result)

# Фільтрація інтервалів
print("Інтервали з Transfer > 2 та Bitrate > 20:\n")
for item in intervals:
    if item["Transfer"] > 2 and item["Bitrate"] > 20:
        print(item)
