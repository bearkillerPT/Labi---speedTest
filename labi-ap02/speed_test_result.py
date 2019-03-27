import datetime
import hashlib


class SpeedTestResult:
    count = 0

    def __init__(self, server_id: int, download_size: int, download_time: float, latency: int):
        """Constructor of the class, initializes all variables.
        :param server_id: id of the target server.
        :param download_size: size of the download made.
        :param download_time: time that took to do the download.
        :param latency: latency of the connection to the server.
        """
        assert type(server_id) == int and type(download_size) == int and type(download_time) == float and type(latency) == int
        self.server_id = server_id
        self.download_size = download_size
        self.download_time = download_time
        self.latency = latency
        self.date = datetime.datetime.now()
        SpeedTestResult.count += 1
        self.count = SpeedTestResult.count

    def getDownloadSpeed(self) -> float:
        """Calculate download speed based on the download size and time.
        :return: Download Speed.
        """
        return float(self.download_size) / float(self.download_time)

    def getObjList(self) -> list:
        """Returns an list of all the attributes, with a verification hash as last item
         that will be used in the report.
        :return: List of Attributes.
        """
        concat_attrib = str(self.count) + str(self.server_id) + str(self.date) + str(self.latency) + str(self.getDownloadSpeed())
        check_hash = hashlib.sha256()
        check_hash.update(concat_attrib.encode())
        check = check_hash.hexdigest()
        return [self.count, self.server_id, str(self.date), self.latency, self.getDownloadSpeed(), check]


