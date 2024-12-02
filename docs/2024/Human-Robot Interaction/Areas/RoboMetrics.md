# RoboMetrics

RoboMetrics is a tool developed to messure system usage in a distribuited manner. Is a Python library for measuring system resources. Specially focused on CPU, Memory and GPU usage. It is designed to be used in a wide range of applications, from monitoring system resources to testing and benchmarking.
![image](https://github.com/user-attachments/assets/b8e392b3-5e45-467b-bb27-090839dfd3a7)

Goals of RoboMetrics:

- Provide a simple way to measure resources without losing data in the process.
- Be able to measure resources in real-time.
- Interconnect workers in a network.

https://github.com/RoBorregos/robometrics

## Installation
To install the client install it via pip:

```bash
pip install roborregos-metrics-client
```

To install the server:
```bash
pip install roborregos-metrics-server
```

## Architecture
RoboMetrics is designed to be modular, extensible and distributed. It is composed of four main components:

- **Process**: This represent your normal Python/C++ process/application. Inn order to measure its resources, you only need to import the `robometrics.lib.register` module and call `register`.

```python
from robometrics.lib.register import Register

Register.async_auto_register() # Recomended for non-blocking calls

Register.auto_unregister()
```

- **Workers**: The worker is a module made to run in the background in a host machine. The worker is responsible for collecting data from the registered processes and sending it to the intake server (or in its defect, save the data locally). 

To start a worker, you only need to run the entry point `robometrics.worker.worker`.

```bash  
robometrics-worker
```

- **Intake Server**: The intake server is a server that receives data from the workers and stores it in a database. The server is responsible for managing the data and providing an API to access it.

The current implementation relies on a mongo database, but can be worked towards a more general solution. There is a docker-compose file that can be used to start the db. 

To start the server, you only need to run the entry point `robometrics.server.server`.

```bash
robometrics-server
```

- **RoboMetrics-Viz**: The visualization module is a web application that connects to the intake server and displays the data in a user-friendly way. The web application is built using Next.js and Vega-Lite.

Refer to the viz repo: [RoboMetrics-Viz](https://github.com/RoBorregos/robometrics-viz)


![Architecture](https://github.com/RoBorregos/robometrics/blob/main/.docs/images/Arch.jpeg?raw=true)


## Recomendations
The modules are pretend to used in a robotics enviroment or a distributed system. This way each host sould be responsible to run a worker and a process. The intake server can be run in a central server or in a server that is always on. (Other alternative is to run the worker and process without a central server and run `robometrics-sync` to sync the data to a central server)
