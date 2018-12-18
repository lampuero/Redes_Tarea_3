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
        self.route_table = dict()

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


    def _init_table(self):
        print(type(self.ports))
        for port, routerport in self.ports.items():
            send_packet(port, json.dumps({'port': port, 'responseTo': routerport.input_port,'name': 'REPLACE THIS NAME'}))

    def send_distance_table(self):
        for port, routerport in self.ports:
            send_packet(port, json.dumps({'sender': routerport.input_port, 'table': self.distance_table}))

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
                message['name']= self.name
                send_packet(message['responseTo'], json.dumps(message))
            else:
                self.distance_table[message['name']] = 1
                self.route_table[message['name']] = message['port']
                self.send_distance_table()

        if 'sender' in message and 'table' in message:
            dt = message['table']
            for name, distance in dt:
                if name not in self.distance_table:
                    self.distance_table[name] = distance + 1
                    self.route_table[name] = message['sender']
                    self.send_distance_table()
                elif self.distance_table[name] > distance +1 :
                    self.distance_table[name] = distance + 1
                    self.route_table[name] = message['sender']
                    self.send_distance_table()


        if 'destination' in message and 'data' in message:
            if message['destination'] == self.name:
                self._success(message['data'])
            else:
                # Randomly choose a port to forward
                # port = choice(list(self.ports.keys()))
                port = self.route_table[message['destination']]
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
        self._init_table()
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
