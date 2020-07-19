import time
from influxdb import InfluxDBClient


class DataBaseConstants:
    DB_ADDRESS = "influx"
    DB_DBNAME = "bz"
    DB_MEASURE = "mesr"


class TimeMeasure:
    time_begin = 0
    time_end = 0


class DataBase:
    def __init__(self):
        self._db_cli = InfluxDBClient(DataBaseConstants.DB_ADDRESS, database=DataBaseConstants.DB_DBNAME)

    def write_data(self, data: {}):
        if data:
            mes = [{
                "measurement": DataBaseConstants.DB_MEASURE,
                "fields": data
            }]
            self._db_cli.write_points(mes)

    def get_data(self, timeb, time_l=None, params: [] = None):
        qst = ''
        if params:
            params = ','.join(params)
        else:
            params = "*"
        if time_l is not None:
            qst = ' AND \"time\" < ' + str(time_l)
        query = "SELECT " + params + " FROM " + DataBaseConstants.DB_MEASURE + " WHERE \"time\" > " + str(timeb) + qst \
                + ' GROUP BY "time()"'
        print(query)
        TimeMeasure.time_begin = time.time()
        pts = self._db_cli.query(query, epoch="ns")
        TimeMeasure.time_end = time.time()

        return [a for a in pts.get_points()]
