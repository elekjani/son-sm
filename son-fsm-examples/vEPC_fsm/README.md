# vEPC FSM
Simple FSM mimicing the functionality of the configuration FSM example. It waits for the configuration messages and advertises the IP address for the relevant EPC components (MME, HSS, Geteway) and then start them in the appropriate order.

## Requires
* Docker

## Implementation
* implemented in Python 3.4
* dependecies: amqp-storm
* The main implementation can be found in: `son-fsm-examples/vEPC-fsm/vEPC-fsm/vEPC-fsm.py`

## How to run it

* To run the vEPC FSM locally, you need:
 * a running RabbitMQ broker (see general README.md of [son-mano framework repository](https://github.com/sonata-nfv/son-mano-framework) for info on how to do this)
 * a running Service Specific Registry (SMR) connected to the broker (see general README.md of [SMR repository](https://github.com/sonata-nfv/son-mano-framework) for info on how to do this)

* Run the vEPC FSM (directly in your terminal not in a Docker container):
 * (do in `son-sm/`)
 * `python3.4 son-fsm-examples/vEPC-fsm/vEPC-fsm/vEPC-fsm.py`

* Or: run the vEPC FSM (in a Docker container):
 * (do in `son-sm/`)
 * `docker build -t sonfsmfunctionvEPC -f son-fsm-examples/vEPC/Dockerfile .`
 * `docker run -it --rm --link broker:broker  --name sonfsmfunctionvEPC  sonfsmfunctionvEPC`
