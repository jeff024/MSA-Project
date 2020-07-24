import random
import time
import numpy as np
import math
import threading

from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device
CONNECTION_STRING = "HostName=myIotHub-jeff.azure-devices.net;DeviceId=myiotdevice;SharedAccessKey=W8wMH4BOCdfY1cZMuGITby97Wzn+nfWIFofukJmXHvs="

# Define the JSON message to send to IoT Hub.
voltage_source = 220
impedance = 2
MSG_TXT = '{{"Source_Voltage": {Source_Voltage}, "Load_Voltage": {Load_Voltage}}}'

INTERVAL = 0.01

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def device_method_listener(device_client):
    global INTERVAL
    while True:
        method_request = device_client.receive_method_request()
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        if method_request.name == "SetTelemetryInterval":
            try:
                INTERVAL = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)



def push_signal():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        # Start a thread to listen 
        device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
        device_method_thread.daemon = True
        device_method_thread.start()

        x = 0
        while True:
            
            # Build the message with simulated telemetry values.
            Source_Voltage = voltage_source * math.cos(2 * math.pi * x) + (random.random() * 15)
            Load_Voltage = (voltage_source * math.cos(2 * math.pi * (x + 0.02)) + (random.random() * 15)) / impedance
            msg_txt_formatted = MSG_TXT.format(Source_Voltage=Source_Voltage, Load_Voltage = Load_Voltage)
            message = Message(msg_txt_formatted)

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(INTERVAL)
            x += INTERVAL

    except KeyboardInterrupt:
        print ( "Signal Lost" )


if __name__ == '__main__':
    push_signal()