import pytz
import urllib
import datetime
import numpy as np
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


BUCKET = "ml_app"
ORG = "tokopedia"
TOKEN = "pAQsjdWvk0Sui1krYuv_t_OjRRh9gDLgJUxhyYvr3MOEyJu-hHjC1EUlBCIbjAIcamaBCd01qCAG6DwK3McdTw=="
URL = "http://localhost:8086"


'''
Data to capture:
{
    'measurement': 'REST_Table',
    'tags': {
        'hostname': 'localhost',
        'requestName': '/predict',
        'requestType': 'POST',
        'status': 'PASS',
    },
    'time': timestamp,
    'fields': {
        'responseTime': 5146.123,
        'responseLength': 81582,
    }
}
'''


class InfluxClient:

    def __init__(self,
                 bucket="ml_app",
                 organisation="tokopedia",
                 token="pAQsjdWvk0Sui1krYuv_t_OjRRh9gDLgJUxhyYvr3MOEyJu-hHjC1EUlBCIbjAIcamaBCd01qCAG6DwK3McdTw==",
                 url="http://localhost:8086") -> None:

        self.bucket = bucket
        self.organisation = organisation
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=organisation
        )

        self.write_api = self.client.write_api(
            write_options=SYNCHRONOUS
        )

    def influxdb_write_data(self, hostname,
                            request_name,
                            request_type,
                            status,
                            time,
                            response_time,
                            response_length,
                            measurement="REST_Table",
                            **kwargs):
        point = influxdb_client.Point(measurement_name=measurement)\
            .tag("hostname", hostname)\
            .tag("requestName", request_name)\
            .tag("requestType", request_type)\
            .tag("status", status)\
            .field("responseTime", response_time)\
            .field("responseLength", response_length)\
            .time(time=time)

        self.write_api.write(bucket=self.bucket,
                             org=self.organisation, record=point)

    def influxdb_query_data(self, query, **kwargs):
        query_api = self.client.query_api()
        return query_api.query(org=self.organisation, query=query)

    def influxdb_read_data(self, result, **kwargs):
        
        records = []
        for table1_record, table2_record in zip(*result):
            # for table1_record, table2_record in zip(table1.records, table2.records):
            records.append((table1_record.get_measurement(), table1_record.get_time(), \
                            table1_record.get_field(), table1_record.get_value(), \
                                table2_record.get_time(), table2_record.get_field(), \
                                    table2_record.get_value()))
                
        return records



if __name__ == "__main__":
    url = "http://127.0.0.1:54329/predict"
    hostname = urllib.parse.urlparse(url).hostname
    requestName = urllib.parse.urlparse(url).path
    # Generating random data-points
    data_points = []
    for i in range(40):
        temp_data_point = {
            "measurement": "REST_Table",
            "hostname": hostname,
            "requestName": requestName,
            "requestType": "POST",
            "status": "PASS",
            "responseTime": np.random.rand(1)[0]*20,
            "responseLength": np.random.randint(low=1000, high=5000, size=1)[0]
        }

        data_points.append(temp_data_point)
    

    influx = InfluxClient()

    # Writing data to influxdb
    for data in data_points:

        influx.influxdb_write_data(
            hostname=data['hostname'],
            request_name=data['requestName'],
            request_type=data['requestType'],
            status=data['status'],
            response_time=data['responseTime'],
            response_length=data['responseLength'],
            measurement=data['measurement'],
            time=datetime.datetime.now(tz=pytz.UTC)
        )

    influx_query = 'from(bucket: "ml_app")\
        |> range(start: -5m)\
            |> filter(fn: (r) => r["_measurement"] == "REST_Table")\
                |> filter(fn: (r) => r["hostname"] == "127.0.0.1")'
    
    influx_query_result = influx.influxdb_query_data(influx_query)
    print(influx_query_result[0], influx_query_result[1])


    influx_result = influx.influxdb_read_data(influx_query_result)
    print(influx_result)