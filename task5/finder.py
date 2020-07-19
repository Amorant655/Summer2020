from task1.database import DataBase, DataBaseConstants, TimeMeasure


variables = ['af', ]
begin_time = 1595029767288414880
end_time = 1595029770311130578

# ========================== using default params
# DataBaseConstants.DB_ADDRESS = 'addr'
# DataBaseConstants.DB_DBNAME = 'name'
# DataBaseConstants.DB_MEASURE = 'mes'
# ==========================


if __name__ == '__main__':
    params = None
    if variables:
        params = variables
    print(DataBase().get_data(begin_time, end_time, params))
    print("INFO: request duration ", TimeMeasure.time_end - TimeMeasure.time_begin, '(s)')
