import json
from json import JSONDecodeError
from random import choice
from threading import Timer

from send_packet import send_packet
from routing.router_port import RouterPort


class Router(object):
    def __init__(self, name, update_time, ports, logging=True):
        self.name = name
        self.update_time = update_time
        self.ports = dict()
        self._init_ports(ports)
        self.timer = None
        self.logging = logging
        self.distance_table = dict()
        self.routing_table = dict()

    def _success(self, message):
        """
        Internal method called when a packet is successfully received.
        :param message:
        :return:
        """
        print("[{}] {}: {}".format(self.name, 'Success! Data', message))

    def _log(self, message):
        """
        Internal method to log messages.
        :param message:
        :return: None
        """
        if self.logging:
            print("[{}] {}".format(self.name, message))

    def _init_ports(self, ports):
        """
        Internal method to initialize the ports.
        :param ports:
        :return: None
        """
        for port in ports:
            input_port = port['input']
            output_port = port['output']

            router_port = RouterPort(
                input_port, output_port, lambda p: self._new_packet_received(p)
            )

            self.ports[output_port] = router_port

    def _new_packet_received(self, packet):
        """
        Internal method called as callback when a packet is received.
        :param packet:
        :return: None
        """
        self._log("Packet received")
        message = packet.decode()

        try:
            message = json.loads(message)
        except JSONDecodeError:
            self._log("Malformed packet")
            return

        if 'port' in message and 'responseTo' in message and 'name' in message:
            if message['name'] == 'REPLACE THIS NAME':
                message['name'] = self.name
                send_packet(message['responseTo'], json.dumps(message))
            else:
                self.distance_table[message['name']] = 1
                self.routing_table[message['name']] = message['port']
                self._send_new_distance(message['name'])

        elif 'sender' in message and 'name' in message and 'distance' in message:
            name = message['name']
            distance = message['distance']
            if name not in self.distance_table:
                self.distance_table[name] = distance + 1
                self.routing_table[name] = message['sender']
                self._send_new_distance(name)
            elif self.distance_table[name] > distance + 1:
                self.distance_table[name] = distance + 1
                self.routing_table[name] = message['sender']
                self._send_new_distance(name)

        elif 'destination' in message and 'data' in message:
            if message['destination'] == self.name:
                self._success(message['data'])
            else:
                port = self.routing_table[message['destination']]
                self._log("Forwarding to port {}".format(port))
                self.ports[port].send_packet(packet)
        else:
            self._log("Malformed packet")

    def _broadcast(self):
        """
        Internal method to broadcast
        :return: None
        """
        self._log("Broadcasting")
        self.timer = Timer(self.update_time, lambda: self._broadcast())
        self.timer.start()

    def start(self):
        """
        Method to start the routing.
        :return: None
        """
        self._log("Starting")
        self._broadcast()
        for port in self.ports.values():
            port.start()

    def stop(self):
        """
        Method to stop the routing.
        Is in charge of stop the router ports threads.
        :return: None
        """
        self._log("Stopping")
        if self.timer:
            self.timer.cancel()

        for port in self.ports.values():
            port.stop_running()

        for port in self.ports.values():
            port.join()

        self._log("Stopped")

    def init_table(self):
        for port, router_port in self.ports.items():
            send_packet(port, json.dumps({'port': port,
                                          'responseTo': router_port.input_port,
                                          'name': 'REPLACE THIS NAME'}))

    def _send_new_distance(self, name):
        for port, router_port in self.ports.items():
            send_packet(port, json.dumps({'sender': router_port.input_port,
                                          'name': name,
                                          'distance': self.distance_table[name]}))


