# msa-project2

## Overview
This python script generates telemetry data of the voltages of source and load in a circuit system with noise. 
- Source: 220V AC
- Load impedance: 2 Ohm with delay of half the peroid

By using connection String, we can easily send telemetry data to Iot Hub and therefore get the data visualizing in Power BI.

## Report
This report contains a graph that  used telemetry data received from IOT Hub, containing values of the voltages of source and load. (Note that these telemetry data are simulated by python, not real data). This graph clearly shows the operating voltage across the source and the load impedance.

Using this graph, one can easily determine if the circuit system is operating as expected or it needs fix without really touching the circuit.