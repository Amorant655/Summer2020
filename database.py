from influxdb import InfluxDBClient


class DataBaseConstants:
    DB_ADDRESS = "influx"
    DB_DBNAME = "bz"
    DB_MEASURE = "mesr"


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

    def get_data(self, time):
        pts = self._db_cli.query("SELECT * FROM " + DataBaseConstants.DB_MEASURE + " WHERE \"time\" > " + str(time) +
                                 ' GROUP BY "time()"',
                                 epoch="ns")
        return [a for a in pts.get_points()]
