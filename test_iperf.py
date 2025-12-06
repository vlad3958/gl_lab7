import pytest
from iperf_client import client, parser


def test_client_receives_output():
    server_ip = "192.168.0.10"

    stdout, stderr = client(server_ip)

    # 1. Якщо stderr містить "connect failed" → сервер недоступний
    assert "connect failed" not in stdout.lower(), "iperf3 не зміг підключитися до сервера"

    # 2. stdout повинен містити інтервали "sec"
    assert "sec" in stdout, "Клієнт не отримав реальний трафік від сервера"

    # 3. мінімальна перевірка
    assert "MBytes" in stdout, "Вивід iperf3 неправильний або порожній"


def test_parser_extracts_intervals():
    """
    Тест перевіряє, що парсер правильно виділяє інтервали з виводу iperf.
    """
    sample_output = """
    [  5]   1.00-2.00   sec   3.91 MBytes  32.8 Mbits/sec    0   320.0
    [  5]   2.00-3.00   sec   4.25 MBytes  35.4 Mbits/sec    1   310.0
    """

    intervals = parser(sample_output)

    assert len(intervals) == 2, "FAIL: парсер повинен повернути 2 інтервали"

    assert intervals[0]["Transfer"] == 3.91, "FAIL: невірне значення Transfer"
    assert intervals[1]["Retr"] == 1, "FAIL: невірне значення Retr"
