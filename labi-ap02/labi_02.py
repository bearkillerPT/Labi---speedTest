from sys import argv, exit
from speed_test_result import SpeedTestResult
from typing import List
interval = 0
num = 0
s_id = 0
country = ""


def usage(message):
    print(message)
    print("Usage python3 " + argv[0].split("/")[-1] + " interval num [country or id]")
    exit(1)


def validate():
    global interval, num, s_id, country
    try:
        interval = int(argv[1])
        num = int(argv[2])
        if(len(argv) == 4):
            if(argv[3][0].isnumeric()):
                s_id = int(argv[3])
            else:
                country = argv[3]
        if(len(argv) > 4):
            usage("Too Many Arguments")
    except IndexError as e:
        usage("Not Enough Arguments")
    except ValueError as e:
        usage("Invalid Argument Type: " + e.args[0].split('\'')[1])


# TODO testes com pais como parametro
def country_test_3(country: str) -> SpeedTestResult:
    """ This function will test the connection speed and latency
    with a random server of the country passed as argument.
    :param country, country where the target server is located.
    :return SpeedTestResult object with the results of the test.
    """
    pass


# TODO testes com id como parametro
def id_test_4(server_id: int) -> SpeedTestResult:
    """ This function will test the connection speed and latency
    with a random server of the country passed as argument.
    :param server_id, id of target server.
    :return SpeedTestResult object with the results of the test.
    """
    pass


# TODO criação do report no fim do teste
def report_8(results: List[SpeedTestResult], reportName: str) -> None:
    """ This function will generate a test report based on the results
    obtained in the network tests.
    :param results, list of speed_test_result objects of which the report will be created.
    :param reportName, a string with the name of the output report file.
    :return nothing, the generated report will be output as a file.
    """
    pass


# TODO calculo da velocidade de download
def calc_download_time(size: int, server_id: int) -> float:
    """ This function will calculate the download time
    :param size, integer with the size in bytes of the download
    :param server_id, id of target server.
    :return floating point that is the time, in seconds, that the download took
    """
    pass


# TODO calculo da latencia
def calc_latency(server_id: int) -> int:
    """ This function will calculate the latency
    :param server_id, id of target server.
    :return integer, time, in ms, that the connection took
    """
    pass


# TODO implementar testes
def run_tests(interval, num, id_or_country):
    """This function will make the tests based on parameter and return an array of SpeedTestResult
    :param interval: interval in which the test will be made
    :param num: number of tests to be run
    :param id_or_country: country or id of the target server
    :return: SpeedTestResult list with results
    """
    if(type(id_or_country) == type(1)):
        s_id = id_or_country
    else:
        country = id_or_country


if __name__ == '__main__':
    """Main function that will be executed, if and only if, the current file is the main module"""
    validate()
