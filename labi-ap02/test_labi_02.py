from labi_02 import *
import random
import json
import csv
import hashlib
def test_country_test_3():
    server_list = json.load(open("servers.json", 'r'))
    countries = list(dict.fromkeys([i['country'] for i in server_list['servers']]))
    for _ in range(50):
        c_country = random.choice(countries)
        result = country_test_3(c_country)
        assert type(result) == SpeedTestResult
        assert [i for i in server_list['servers'] if i['id'] == result.server_id][0]['country'] == c_country
        assert len(result.getObjList()) == 6


def test_id_test_4():
    server_list = json.load(open("servers.json", 'r'))
    ids = list(dict.fromkeys([i['id'] for i in server_list['servers']]))
    for _ in range(50):
        c_id = random.choice(ids)
        result = country_test_3(c_id)
        assert type(result) == SpeedTestResult
        assert result.server_id == c_id
        assert len(result.getObjList()) == 6


def test_report_8():
    for _ in range(50):
        test_list = [SpeedTestResult(random.randint(0, 50), random.randint(10, 100), random.randrange(0, 10), random.randint(0, 15)) for _ in range(10)]
        report_8(test_list, "test_report.csv")
        reader = csv.DictReader(open("test_report.csv", 'r'))
        report = []
        for row in reader:
            report.append(row)
        keys = [i for i in report[random.randint(0, 10)]]
        assert keys == ["Contador", "Id Do Servidor", "Data e Hora no Formato ISO", "Latência", "Largura de Banda", "Check"]
        c_test = random.randint(0, 10)
        assert len(report[c_test]) == 6
        test_hash = hashlib.sha256()
        test_hash.update("".join(list(report[c_test][:-56])))


def test_calc_download_time():
    server_list = json.load(open("servers.json", 'r'))
    ids = list(dict.fromkeys([i['id'] for i in server_list['servers']]))
    for _ in range(50):
        result = calc_download_time(random.randint(10, 100), random.choice(ids))
        assert 0 < result <= 1000
        assert type(result) == float

    result = calc_download_time(-1, random.choice(ids))
    assert result == 0

    result = calc_download_time(1, 132893218497821309812)
    assert result == 0

    result = calc_download_time(1, -1)
    assert result == 0


def test_calc_latency():
    server_list = json.load(open("servers.json", 'r'))
    ids = list(dict.fromkeys([i['id'] for i in server_list['servers']]))
    for _ in range(50):
        result = calc_latency(random.choice(ids))
        assert 0 < result <= 1000
        assert type(result) == float

    result = calc_latency(312231124123131241232412312)
    assert result == -1

    result = calc_latency(-123)
    assert result == -1




