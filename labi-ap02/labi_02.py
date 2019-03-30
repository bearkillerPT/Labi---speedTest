import sys
from sys import argv, exit
from speed_test_result import SpeedTestResult
from typing import List
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import Crypto
import json
import random
import csv
import socket
import time

MB = 1024 ** 2
interval = 0
num = 0
s_id = 0
id_or_country = ""
servers = None


def usage(message):
    print(message)
    print("Usage python3 " + argv[0].split("/")[-1] + " interval num [country or id]")
    exit(1)


def validate() -> None:
    """This function will validate the input made through the terminal in the sys.argv variable
    :return: None
    """
    global interval, num, s_id, id_or_country, servers
    try:
        interval = int(argv[1])
        num = int(argv[2])
        if(len(argv) == 4):
                id_or_country = argv[3]
        if(len(argv) > 4):
            usage("Too Many Arguments")
    except IndexError as e:
        usage("Not Enough Arguments")
    except ValueError as e:
        usage("Invalid Argument Type: " + e.args[0].split('\'')[1])


def random_test(country: str) -> SpeedTestResult:
    """ This function will test the connection speed and latency
    with a random server of the country passed as argument.
    :param country, country where the target server is located.
    :return SpeedTestResult object with the results of the test.
    """
    global servers
    i_list_server = [i for i in servers]
    target_server = random.choice(i_list_server)
    i_server_id = target_server['id']
    i_download_speed = calc_download(target_server)
    i_latency = calc_latency(target_server)
    return(SpeedTestResult(i_server_id, i_download_speed, i_latency))


def country_test_3(country: str) -> SpeedTestResult:
    """ This function will test the connection speed and latency
    with a random server of the country passed as argument.
    :param country, country where the target server is located.
    :return SpeedTestResult object with the results of the test.
    """
    global servers
    i_list_server = [i for i in servers if i['country'] == country]
    target_server = random.choice(i_list_server)
    i_server_id = target_server['id']
    i_download_speed = calc_download(target_server)
    i_latency = calc_latency(target_server)
    return(SpeedTestResult(i_server_id, i_download_speed, i_latency))


def id_test_4(server_id: int) -> SpeedTestResult:
    """ This function will test the connection speed and latency
    with a random server of the country passed as argument.
    :param server_id, id of target server.
    :return SpeedTestResult object with the results of the test.
    """
    global servers
    i_list_server = [i for i in servers if i['id'] == server_id]
    target_server = i_list_server[0]
    i_server_id = target_server['id']
    i_download_speed = calc_download(target_server)
    i_latency = calc_latency(target_server)
    return (SpeedTestResult(i_server_id, i_download_speed, i_latency))


def report_8(results: List[SpeedTestResult], report_name: str) -> None:
    """ This function will generate a test report based on the results
    obtained in the network tests.
    :param results, list of speed_test_result objects of which the report will be created.
    :param reportName, a string with the name of the output report file.
    :return nothing, the generated report will be output as a file.
    """
    with open(report_name, 'w', newline='') as csvfile:
        labels = ["Contador", "Id Do Servidor", "Data e Hora no Formato ISO", "Latência", "Largura de Banda", "Check"]
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=labels)
        writer.writeheader()
        for i in results:
            writer.writerow(i.getObjDict())
    create_signed_document("key.priv", "report.sig")



def calc_download(server: dict) -> (float, float):
    """ This function will calculate the download time
    :param server, target server.
    :return floating point tuple that is the time and size of download
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_url = server['host'].split(':')[0]
        s_port = int(server['host'].split(':')[1])
        s.connect((s_url, s_port))
    except socket.gaierror as e:
        print("error")
        return 0


    s.send(b"DOWNLOAD 100000000\n")
    received = b""
    c_time = time.time()
    e_time = time.time() - c_time
    while(len(received) and e_time < 2):
        received = s.recv(1024)
        e_time = time.time() - c_time
    while(len(s.recv(32)) != 0): pass
    s.send(("DOWNLOAD " + str(MB) + "\n").encode())
    c_time = time.time()
    a = s.recv(MB, (socket.MSG_WAITALL))
    e_time = time.time() - c_time
    s.send(b"QUIT \n")
    s.close()
    return 1/(e_time)



def calc_latency(server: dict) -> int:
    """ This function will calculate the latency
    :param server, target server.
    :return integer, time, in ms, that the connection took
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_url = server['host'].split(':')[0]
        s_port = int(server['host'].split(':')[1])
        s.connect((s_url, s_port))
    except socket.gaierror as e:
        return -1
    time_list = []
    for _ in range(10):
        c_time = time.time()
        s.send(("PING "+str(c_time*1000)+"\n").encode())
        s.recv(48)
        time_list.append((time.time()-c_time)*1000)

    s.send(b"QUIT \n")
    time_average = sum(time_list)/len(time_list)
    return round(time_average)


def run_tests(interval, num, id_or_country) -> List[SpeedTestResult]:
    """This function will make the tests based on parameter and return an array of SpeedTestResult
    :param interval: interval in which the test will be made
    :param num: number of tests to be run
    :param id_or_country: country or id of the target server
    :return: SpeedTestResult list with results
    """
    result = []
    if(type(id_or_country) == int):
        for _ in range(num):
            result.append(id_test_4(id_or_country))
            time.sleep(interval)
    elif(len(id_or_country) == 0):
        for _ in range(num):
            result.append(random_test(id_or_country))
            time.sleep(interval)
    else:
        for _ in range(num):
            result.append(country_test_3(id_or_country))
            time.sleep(interval)
    return result


def create_signed_document(key_path: str, report_name: str, signature_name: str) -> None:
    """This function will generate a file with the signature of the report
    :param key_path: The path to the file that contains the key
    :param signature_name: The name of the signature file that will be generated
    :return: None
    """
    key = None
    with open(key_path, 'r') as key_file:
        key = RSA.importKey(key_file.read())

    signed_doc = None
    with open(report_name, 'r') as rep:
        report_string = rep.read()

    report_string += (len(report_string) % 128) * " "
    report_splited_bstring = []
    for i in range(0,len(report_string),len(report_string)//128):
        report_splited_bstring.append(report_string[i:i+len(report_string)//128].encode('utf-8'))

    cipher = PKCS1_OAEP.new(key)
    output = bytearray()
    with open(signature_name, 'wb') as o_file:
        for i in report_splited_bstring:
            o_file.write(cipher.encrypt(i))



if __name__ == '__main__':
    """Main function that will be executed, if and only if, the current file is the main module"""
    with open("servers.json", 'r') as s_file:
        servers_file = json.load(s_file)
        servers = servers_file['servers']
    validate()
    testes = run_tests(interval, num, 1902)
    report_8(testes, "report.csv")
    create_signed_document("key.priv", "report.csv", "report.sig")

