"""
Basic TCP client/server for the purposes of ONC-RPC.
"""

def _length_from_bytes(four_bytes):
    """
    The RPC standard calls for the length of a message to be sent as the least
    significant 31 bits of an XDR encoded unsigned integer.  The most
    significant bit encodes a True/False bit which indicates that this message
    will be the last.
    """
    from xdrlib import Unpacker
    unpacker = Unpacker(four_bytes)
    val = unpacker.unpack_uint()
    unpacker.done()
    if val < 2**31:
        return (val, False)
    return (val-2**31, True)

def _bytes_from_length(len, closing):
    """
    The RPC standard calls for the length of a message to be sent as the least
    significant 31 bits of an XDR encoded unsigned integer.  The most
    significant bit encodes a True/False bit which indicates that this message
    will be the last.
    """
    assert 0 <= len < 2**31
    from xdrlib import Packer
    if closing:
        len += 2**31
    packer = Packer()
    packer.pack_uint(len)
    return packer.get_buffer()


class tcp_client(object):
    """
    The TCP Client handles only the network portion of an RPC client.
    """
    def __init__(self, socket):
        self.socket = socket
        self.socket.setblocking(0)
        self.in_messages = []
        self.out_messages = []
        self.in_buffer = bytes()
        self.out_buffer = bytes()
        self.next_in_message = None
        self.closing = False

    @staticmethod
    def connect(server_host, server_port):
        """
        Connect to a server.
        """
        import socket as _socket
        socket = _socket.create_connection((server_host, server_port))
        socket = tcp_client(socket)
        socket.server_host = server_host
        socket.server_port = server_port
        return socket

    def pop_message(self):
        """
        Pop a message.  Returns a opaque_bytes if they exist.
        Returns None if no messages are waiting.
        """
        if not self.in_messages:
            return None
        return self.in_messages.pop(0)

    def push_message(self, opaque_bytes, close=False):
        """
        Push a message back to the network.
        Set close=True if this is the last message being sent to this
        connection.
        """
        self.out_messages.append((opaque_bytes, close))

    def cycle_network(self, timeout):
        """
        Cycle the network connection.
        """
        self._push_data_around()
        import select as _select
        import time as _time
        p = _select.poll()
        self._register(p)
        events = p.poll(timeout)
        self._handle(events)
        self._push_data_around()

    def _register(self, poll):
        if self.out_buffer:
            poll.register(self.socket)
        else:
            import select
            poll.register(self.socket, select.POLLIN | select.POLLPRI)

    def _handle(self, events):
        for fd, event in events:
            if fd != self.socket.fileno():
                continue
            import select
            if event & select.POLLIN or event & select.POLLPRI:
                # read
                try:
                    while True:
                        bytes = self.socket.recv(4096)
                        if not bytes:
                            break
                        self.in_buffer += bytes
                        if len(bytes) < 4096:
                            break
                except:
                    pass
            if event & select.POLLOUT:
                # write
                try:
                    if len(self.out_buffer) < 4096:
                        bytes = self.out_buffer
                    else:
                        bytes = self.out_buffer[:4096]
                    n = self.socket.send(bytes)
                    self.out_buffer = self.out_buffer[n:]
                except:
                    pass

    def _push_data_around(self):
        # in-messages.
        while True:
            if self.next_in_message is not None:
                if len(self.in_buffer) < self.next_in_message:
                    break
                message = self.in_buffer[:self.next_in_message]
                self.in_buffer = self.in_buffer[self.next_in_message:]
                self.in_messages.append(message)
                self.next_in_message = None
            # we are now trying to read the next four bytes.
            if len(self.in_buffer) < 4:
                break
            l, closing = _length_from_bytes(self.in_buffer[:4])
            self.in_buffer = self.in_buffer[4:]
            self.next_in_message = l
            if closing: self.closing = True
        # out-messages.
        while self.out_messages:
            bytes, closing = self.out_messages.pop(0)
            self.out_buffer += _bytes_from_length(len(bytes), closing)
            self.out_buffer += bytes



class tcp_server(object):
    """
    The TCP server handles only the network portion of an RPC server.
    """
    def __init__(self, server_port):
        import socket as _socket
        self.server_port = server_port
        self.socket = _socket.socket()
        self.socket.bind(("localhost", self.server_port))
        self.socket.listen(5)
        self.in_messages = []
        self.clients = {}
        self.next_client_id = 0

    def pop_message(self):
        """
        Pop a message.  Returns a (connection_id, opaque_bytes) pair.
        Returns None if no messages are waiting.
        """
        if not self.in_messages:
            return None
        return self.in_messages.pop(0)

    def push_message(self, client_id, opaque_bytes, close=False):
        """
        Push a message back to the network.
        Set close=True if this is the last message being sent to this
        connection.
        """
        if client_id in self.clients:
            self.clients[client_id].push_message(opaque_bytes, close=close)

    def cycle_network(self, timeout):
        """
        Cycle the network connection.
        """
        self._push_data_around()
        import select as _select
        import time as _time
        p = _select.poll()
        self._register(p)
        events = p.poll(timeout)
        self._handle(events)
        self._push_data_around()

    def _push_data_around(self):
        for client_id, client in self.clients.items():
            while True:
                message = client.pop_message()
                if not message: break
                self.in_messages.append((client_id, message))
        for client in self.clients.values():
            client._push_data_around()

    def _register(self, poll):
        import select as _select
        poll.register(self.socket, _select.POLLIN | _select.POLLPRI)
        for client in self.clients.values():
            client._register(poll)

    def _handle(self, events):
        for fd, event in events:
            if fd != self.socket.fileno():
                continue
            import select as _select
            if event & _select.POLLIN or event & _select.POLLPRI:
                socket, address = self.socket.accept()
                socket = tcp_client(socket)
                socket.address = address
                self.clients[self.next_client_id] = socket
                self.next_client_id += 1
        for client in self.clients.values():
            client._handle(events)



if __name__ == "__main__":
    import threading
    class ServerThread(threading.Thread):
        def run(self):
            server = tcp_server(10010)
            for i in range(50):
                print("Loop!")
                server.cycle_network(5000.0)
                while True:
                    m = server.pop_message()
                    if not m: break
                    client_id, message = m
                    server.push_message(client_id, message)


    server = ServerThread()
    server.start()

    import time
    time.sleep(3.0)

    client = tcp_client.connect("localhost", 10010)

    client.push_message("hello, world!".encode("utf-8"))
    client.cycle_network(100.0)
    time.sleep(3.0)
    client.cycle_network(100.0)
    time.sleep(3.0)
    client.cycle_network(100.0)
    time.sleep(3.0)
    m = client.pop_message()
    print("message:")
    print(m)

    server.join()


