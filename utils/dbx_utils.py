from constants import (
    DEVICE_TABLE_BRONZE,
    SERVER_HOSTNAME,
    HTTP_PATH,
    ACCESS_TOKEN,
    DB_NAME,
    DEVICE_TABLE_SILVER,
    DEVICE_TABLE_GOLD
)


from databricks import sql


import datetime as dt

app_start_ts = dt.datetime.now() 



def get_bme_data(TempReading, HumidityReading, EventTimestamp, EventDate):
    connection0 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor0 = connection0.cursor()
    cursor0.execute(
        f"SELECT * FROM {DB_NAME}.{DEVICE_TABLE_SILVER} WHERE EventTimestamp >= '{app_start_ts}'::timestamp ORDER BY EventTimestamp ASC;"

    )
    df = cursor0.fetchall_arrow()
    df = df.to_pandas()
    cursor0.close()
    connection0.close()
    return df

def get_moving_average(Temperature_Moving_Average, Humidity_Moving_Average, TimestampSecond):
    connection1 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor1 = connection1.cursor()
    cursor1.execute(
        f"SELECT * FROM {DB_NAME}.{DEVICE_TABLE_GOLD} WHERE TimestampSecond >= '{app_start_ts}'::timestamp ORDER BY TimestampSecond ASC;"
    )
    df1 = cursor1.fetchall_arrow()
    df1 = df1.to_pandas()
    cursor1.close()
    connection1.close()
    return df1


