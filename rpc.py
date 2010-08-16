"""
RPC implementation.
"""

from xdr import xdr_enum, xdr_opaque, xdr_struct, xdr_uint, xdr_union

from xdrlib import Packer, Unpacker

class auth_flavor(xdr_enum):
    AUTH_NONE = 0
    AUTH_SYS = 1
    AUTH_SHORT = 2

class opaque_auth(xdr_struct):
    flavor = auth_flavor
    body = xdr_opaque(max=400)

class msg_type(xdr_enum):
    CALL = 0
    REPLY = 1

class reply_stat(xdr_enum):
    MSG_ACCEPTED = 0
    MSG_DENIED = 1

class accept_stat(xdr_enum):
    SUCCESS = 0
    PROG_UNAVAIL = 1
    PROG_MISMATCH = 2
    PROC_UNAVAIL = 3
    GARBAGE_ARGS = 4
    SYSTEM_ERR = 5

class reject_stat(xdr_enum):
    RPC_MISMATCH = 0
    AUTH_ERROR = 1

class auth_stat(xdr_enum):
    AUTH_OK = 0
    AUTH_BADCRED = 1
    AUTH_REJECTEDCRED = 2
    AUTH_BADVERF = 3
    AUTH_REJECTEDVERF = 4
    AUTH_TOOWEAK = 5
    AUTH_INVALIDRESP = 6
    AUTH_FAILED = 7

class call_body(xdr_struct):
    rpcvers = xdr_uint
    prog = xdr_uint
    vers = xdr_uint
    proc = xdr_uint
    cred = opaque_auth
    verf = opaque_auth

class mismatch_info(xdr_struct):
    low = xdr_uint
    high = xdr_uint

class accepted_reply(xdr_struct):
    verf = opaque_auth
    reply_data = xdr_union(stat=accept_stat)
    reply_data.SUCCESS.results = xdr_opaque(size=0)
    reply_data.PROG_MISMATCH.mismatch_info = mismatch_info
    # reply_data.default = void

class rejected_reply(xdr_union(stat=reject_stat)):
    RPC_MISMATCH.mismatch_info = mismatch_info
    AUTH_ERROR.error_stat = auth_stat

class reply_body(xdr_union(stat=reply_stat)):
    MSG_ACCEPTED.areply = accepted_reply
    MSG_DENIED.rreply = rejected_reply

class rpc_msg(xdr_struct):
    xid = xdr_uint
    body = xdr_union(mtype=msg_type)
    body.CALL.cbody = call_body
    body.REPLY.rbody = reply_body



class tcp_server(object):
    """
    The TCP server handles only the network portion of an RPC server.
    """
    def __init__(self, server_port):
        self.server_port = server_port

    def pop_message(self):
        """
        Pop a message.  Returns a (connection_id, opaque_bytes) pair.
        Returns None if no messages are waiting.
        """
        pass

    def push_message(self, connection_id, opaque_bytes, close=False):
        """
        Push a message back to the network.
        Set close=True if this is the last message being sent to this
        connection.
        """
        pass

    def cycle_network(self, timeout):
        """
        Cycle the network connection.
        """
        pass


class tcp_client(object):
    """
    The TCP Client handles only the network portion of an RPC client.
    """
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def pop_message(self):
        """
        Pop a message.  Returns a opaque_bytes if they exist.
        Returns None if no messages are waiting.
        """
        pass

    def push_message(self, opaque_bytes, close=False):
        """
        Push a message back to the network.
        Set close=True if this is the last message being sent to this
        connection.
        """
        pass

    def cycle_network(self, timeout):
        """
        Cycle the network connection.
        """
        pass




#opaque_auth(flavor=1, body="apples to apples").pack(3)

packer = Packer()
info = mismatch_info(low=2, high=4)
info.pack(packer)
buffer = packer.get_buffer()
print("packed data: " + str(buffer))

unpacker = Unpacker(buffer)
new_info = mismatch_info.unpack(unpacker)
print("low: %d" % new_info.low.value)
print("high: %d" % new_info.high.value)

reply = rejected_reply(stat=reject_stat.RPC_MISMATCH,
                       mismatch_info=mismatch_info(low=2, high=4))
packer = Packer()
reply.pack(packer)
print("packed data: %s" % packer.get_buffer())

packer = Packer()
reply = rejected_reply(stat=reject_stat.AUTH_ERROR,
                       error_stat = auth_stat.AUTH_FAILED)
reply.pack(packer)
print("packed data: %s" % packer.get_buffer())

msg = rpc_msg(xid=123,
              body=rpc_msg.body(mtype=msg_type.CALL,
                                cbody=call_body(rpcvers=2,
                                                prog=4,
                                                vers=6,
                                                proc=8,
                                                cred=opaque_auth(flavor=auth_flavor.AUTH_SYS, body=bytes()),
                                                verf=opaque_auth(flavor=auth_flavor.AUTH_SYS, body=bytes()))))

packer = Packer()
msg.pack(packer)
print("packed data: %s" % str(packer.get_buffer()))

unpacker = Unpacker(packer.get_buffer())
msg2 = rpc_msg.unpack(unpacker)
print(msg2.xid.value)
print(msg2.body.mtype.value)
print(msg2.body.cbody.rpcvers.value)
print(msg2.body.rbody.stat)
