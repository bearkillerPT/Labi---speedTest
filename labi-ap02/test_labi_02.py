from labi_02 import *
import random
import json
import csv
import hashlib
import time
import pytest

number_of_tests = 1   # int(argv[1])


def test_country_test_3():
    load_server()
    global number_of_tests
    server_list = json.load(open("servers.json", 'r'))
    countries = list(dict.fromkeys([i['country'] for i in server_list['servers']]))
    for _ in range(number_of_tests):
        c_country = random.choice(countries)
        result = country_test_3(c_country)
        assert type(result) == SpeedTestResult
        assert [i for i in server_list['servers'] if i['id'] == result.server_id][0]['country'] == c_country
        assert len(result.getObjDict()) == 6

test_country_test_3()
def test_id_test_4():
    load_server()
    global number_of_tests
    server_list = json.load(open("servers.json", 'r'))
    countries = list(([i['country'] for i in server_list['servers']]))
    for _ in range(number_of_tests):
        c_country = random.choice(countries)
        result = country_test_3(c_country)
        assert type(result) == SpeedTestResult
        assert len(result.getObjDict()) == 6


def test_report_8():
    load_server()
    global number_of_tests
    for _ in range(number_of_tests):
        test_list = [SpeedTestResult(random.randint(0, 50), float(random.randrange(10, 100)), random.randint(0, 10)) for _ in range(10)]
        report_8(test_list, "test_report.csv")
        reader = csv.DictReader(open("test_report.csv", 'r'))
        report = []
        for row in reader:
            report.append(row)
        keys = [i for i in report[random.randint(0, 10)]]
        assert keys == ["Contador", "Id Do Servidor", "Data e Hora no Formato ISO", "Latencia", "Largura de Banda", "Check"]
        c_test = random.randint(0, 9)
        assert len(report[c_test]) == 6

def test_calc_download():
    load_server()
    global number_of_tests
    server_list = json.load(open("servers.json", 'r'))
    ids = list(dict.fromkeys([i['id'] for i in server_list['servers']]))
    for _ in range(number_of_tests):
        result = calc_download(random.choice(server_list['servers']))
        assert 0 <= result <= 100
        assert type(result) == float

    result = calc_download(random.choice(server_list['servers']))
    assert result == 0


def test_calc_latency():
    load_server()
    global number_of_tests
    server_list = json.load(open("servers.json", 'r'))
    servers = list(([i for i in server_list['servers']]))
    for _ in range(number_of_tests):
        result = calc_latency(random.choice(servers))
        assert -1 <= result <= 1000
        assert type(result) == int

    result = calc_latency(random.choice(server_list['servers']))
    assert result == -1

    #result = calc_latency({})
    #assert result == -1


def test_run_test():
    load_server()
    global number_of_tests
    server_list = json.load(open("servers.json", 'r'))
    ids = list(dict.fromkeys([i['id'] for i in server_list['servers']]))
    for i in range(number_of_tests):
        r_interval = random.randrange(2, 5)
        r_num = random.randint(1, 5)
        r_id = random.choice(ids)
        s_time = time.time()
        result = run_tests(r_interval, r_num, r_id)
        e_time = time.time() - s_time

        assert e_time > r_interval * r_num
        assert type(result) == list
        assert type(result[random.randint(0, len(result)-1)]) == SpeedTestResult















