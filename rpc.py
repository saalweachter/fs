"""
RPC implementation.
"""

from xdr import xdr_enum, xdr_opaque, xdr_struct, xdr_uint, xdr_union, xdr_string, xdr_array

class auth_flavor(xdr_enum):
    AUTH_NONE = 0
    AUTH_SYS = 1
    AUTH_SHORT = 2

class opaque_auth(xdr_struct):
    flavor = auth_flavor
    body = xdr_opaque(max=400)
    @staticmethod
    def NONE():
        return opaque_auth(flavor=auth_flavor.AUTH_NONE, body=bytes())

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



class authsys_parms(xdr_struct):
    stamp = xdr_uint
    machinename = xdr_string(max=255)
    uid = xdr_uint
    gid = xdr_uint
    gids = xdr_array(xdr_uint, max=16)



class PING_PROG(rpc_program(prog=0)):
    PING_VERS_PINGBACK = rpc_version(vers=2)
    PING_VERS_PINGBACK.PINGPROC_NULL = rpc_procedure(proc=0,
                                                     args=rpc_void,
                                                     ret=rpc_void)
    PING_VERS_PINGBACK.PINGPROC_PINGPROC = rpc_procedure(proc=1,
                                                         args=rpc_void,
                                                         ret=rpc_int)
    PING_VERS_ORIG = rpc_version(vers=1)
    PING_VERS_ORIG.PINGPROC_NULL = rpc_procedure(proc=0,
                                                 args=rpc_void,
                                                 ret=rpc_void)



class rpc_program(object):
    """
    Base class for an RPC program.
    """
    def __init__(self, program_id, version_id):
        self.program_id = program_id
        self.version_id = version_id
        self.procedures = {}

    def get_procedure(self, procedure_id):
        if procedure_id not in self.procedures:
            return None
        return self.procedures[procedure_id]



class rpc_server(object):
    """
    Run an RPC server.
    """
    def __init__(self, server_port):
        from tcp import tcp_server
        #self.tcp_server = tcp_server(server_port)
        self.programs = {}

    def cycle_network(self, timeout):
        self.tcp_server.cycle_network(timeout)

    def handle_message(self, opaque_bytes):
        """
        Handles a message, start to finish.
        Takes the opaque bytes representing the XDR encoded RPC message.
        Produces an RPC reply, also encoded as opaque bytes.
        """
        from xdrlib import Unpacker, Packer
        unpacker = Unpacker(opaque_bytes)
        msg = rpc_msg.unpack(unpacker)
        def _pack(reply):
            packer = Packer()
            reply.pack(packer)
            return packer.get_buffer()
        print(msg.body.mtype.value)
        if msg.body.mtype != msg_type.CALL:
            print("No reply!")
            return None # do not reply to such a bad message.
        _body = rpc_msg.body
        _rbody = reply_body
        _rreply = rejected_reply
        _areply = accepted_reply
        _rdata = accepted_reply.reply_data
        
        if msg.body.cbody.rpcvers != 2:
            reply = rpc_msg(xid=msg.xid,
                            body=_body(mtype=msg_type.REPLY,
                                       rbody=_rbody(stat=reply_stat.MSG_DENIED,
                                                    rreply=_rreply(stat=reject_stat.RPC_MISMATCH,
                                                                   mismatch_info=mismatch_info(low=2, high=2)))))
            return _pack(reply)
        if msg.body.cbody.prog not in self.programs:
            reply = rpc_msg(xid=msg.xid,
                            body=_body(mtype=msg_type.REPLY,
                                       rbody=_rbody(stat=reply_stat.MSG_ACCEPTED,
                                                    areply=_areply(verf=_AUTH_NON(),
                                                                   reply_data=_rdata(stat=accept_stat.PROG_UNAVAIL)))))
            return _pack(reply)

        program_versions = self.programs[msg.body.cbody.prog]
        if msg.body.cbody.vers not in program_versions:
            min, max = None, None
            for k in self.programs[msg.body.cbody.prog].keys():
                if min is None: min = k
                elif k < min: min = k
                if max is None: max = k
                elif k > max: max = k
            m = mismatch_info(low=min, high=max)
            a=accepted_reply.reply_data(stat=accept_stat.PROG_MISMATCH,
                                        mismatch_info=m)
            b=accepted_reply(verf=opaque_auth.NONE(),
                             reply_data=a)
            c=reply_body(stat=reply_stat.MSG_ACCEPTED, areply=b)
            reply = rpc_msg(xid=msg.xid,
                            body=rpc_msg.body(mtype=msg_type.REPLY,
                                              rbody=c))
            return _pack(reply)

        program = program_versions[msg.body.cbody.vers]
        procedure = program.get_procedure(msg.body.cbody.proc)
        if procedure is None:
            a=accepted_reply.reply_data(stat=accept_stat.PROC_UNAVAIL)
            b=accepted_reply(verf=opaque_auth.NONE(),
                             reply_data=a)
            c=reply_body(stat=reply_stat.MSG_ACCEPTED,
                         areply=b)
            reply = rpc_msg(xid=msg.xid,
                            body=rpc_msg.body(mtype=msg_type.REPLY,
                                              rbody=c))
            return _pack(reply)

        arg_bytes = unpacker.get_buffer()[unpacker.get_position():]
        try:
            args = procedure.parse_args(arg_bytes)
        except:
            a=accepted_reply.reply_data(stat=accept_stat.GARBAGE_ARGS)
            b=accepted_reply(verf=opaque_auth.NONE(),
                             reply_data=a)
            c=reply_body(stat=reply_stat.MSG_ACCEPTED,
                         areply=b)
            reply = rpc_msg(xid=msg.xid,
                            body=rpc_msg.body(mtype=msg_type.REPLY,
                                              rbody=c))
            return _pack(reply)

        try:
            res = procedure.handle(args)
        except:
            a=accepted_reply.reply_data(stat=accept_stat.SYSTEM_ERR)
            b=accepted_reply(verf=opaque_auth.NONE(),
                             reply_data=a)
            c=reply_body(stat=reply_stat.MSG_ACCEPTED,
                         areply=b)
            reply = rpc_msg(xid=msg.xid,
                            body=rpc_msg.body(mtype=msg_type.REPLY,
                                              rbody=c))
            return _pack(reply)
        print(type(res))
 
    def register_program(self, program):
        """
        Register a program to respond to messages.
        """
        if program.program_id not in self.programs:
            self.programs[program.program_id] = {}
        self.programs[program.program_id][program.version_id] = program


from xdrlib import Unpacker, Packer

m = rpc_msg(xid=2,
            body=rpc_msg.body(mtype=msg_type.CALL,
                              cbody=call_body(rpcvers=2,
                                              prog=0,
                                              vers=1,
                                              proc=0,
                                              cred=opaque_auth.NONE(),
                                              verf=opaque_auth.NONE())))


packer = Packer()
m.pack(packer)
print(packer.get_buffer())


class ping_vers_orig(rpc_program):
    class pingproc_null(object):
        def __init__(self):
            pass
        def parse_args(self, bytes):
            # no args
            return None
        def handle(self, args):
            return None
    def __init__(self):
        rpc_program.__init__(self, 0, 1)
        self.procedures[0] = ping_vers_orig.pingproc_null()


server = rpc_server(10010)
server.register_program(ping_vers_orig())

res = server.handle_message(packer.get_buffer())

print(type(res))
print(res)


#opaque_auth(flavor=1, body="apples to apples").pack(3)






"""
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
"""

