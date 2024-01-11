import pytz
import socket
import datetime
from locust import events
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


BUCKET = "ml_app"
ORG = "tokopedia"
TOKEN = "pAQsjdWvk0Sui1krYuv_t_OjRRh9gDLgJUxhyYvr3MOEyJu-hHjC1EUlBCIbjAIcamaBCd01qCAG6DwK3McdTw=="
URL = "http://localhost:8086"


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
                            time,
                            context,
                            response_time,
                            response_length,
                            response,
                            exception,
                            measurement="REST_Table",
                            **kwargs):
        point = influxdb_client.Point(measurement_name=measurement)\
            .tag("hostname", hostname)\
            .tag("requestName", request_name)\
            .tag("requestType", request_type)\
            .tag("context", context)\
            .tag("exception", exception)\
            .tag("response", response)\
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


class EventInfluxHandler():

    hostname = socket.gethostname()
    influxDBClient = InfluxClient()
    database_name = "locustdb"

    # @staticmethod
    # def init_influx_client():
    #     EventInfluxHandler.influxDBClient().drop_database(EventInfluxHandler.database_name)
    #     EventInfluxHandler.influxDBClient().create_database(EventInfluxHandler.database_name)
    #     EventInfluxHandler.influxDBClient().switch_database(EventInfluxHandler.database_name)

    @staticmethod
    @events.request.add_listener
    def request_success_handler(request_type, name, response, response_time, response_length, context, exception, **kwargs):
        EventInfluxHandler.influxDBClient.influxdb_write_data(
            hostname=EventInfluxHandler.hostname,
            request_name=name,
            request_type=request_type,
            time=datetime.datetime.now(tz=pytz.UTC),
            context=context,
            response_time=response_time,
            response_length=response_length,
            response=response,
            exception=exception,
        )