"""
RPC implementation.
According to RPC 1831.
"""

from xdr import xdr_enum, xdr_opaque, xdr_struct, xdr_uint, xdr_union, xdr_string, xdr_array, xdr_void, xdr_int

class auth_flavor(xdr_enum):
    AUTH_NONE = 0
    AUTH_SYS = 1
    AUTH_SHORT = 2
    # added by RPC 2203
    RPCSEC_GSS = 6

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



def rpc_program(prog):
    def _rpc_program(cls):
        cls.program_id = prog
        def get_version_decl(cls, vers):
            for v in cls.__dict__.values():
                try:
                    if v.version_id == vers:
                        return v
                except AttributeError as e:
                    pass
        def get_version_impl(self, vers):
            for v in self.__dict__.values():
                try:
                    if v.version_id == vers:
                        return v
                except AttributeError as e:
                    pass
        cls.get_version_decl = classmethod(get_version_decl)
        cls.get_version_impl = get_version_impl
        return cls

    return _rpc_program

def rpc_version(vers):
    def _rpc_version(cls):
        cls.version_id = vers
        def get_procedure_by_id(cls, proc):
            for k, v in cls.__dict__.items():
                try:
                    if v.procedure_id == proc:
                        return v
                except AttributeError as e:
                    pass
        def get_procedure_by_name(cls, proc):
            for k, v in cls.__dict__.items():
                if k == proc:
                    return v
        cls.get_procedure_by_id = classmethod(get_procedure_by_id)
        cls.get_procedure_by_name = classmethod(get_procedure_by_name)
        return cls
    return _rpc_version

def rpc_procedure(proc, args, ret):
    def _rpc_procedure(fxn):
        fxn.procedure_id = proc
        fxn.argument_type = args
        fxn.return_type = ret
        return fxn
    return _rpc_procedure


@rpc_program(prog=0)
class PING_PROG(object):
    def __init__(self):
        self.PING_VERS_ORIG = PING_PROG.PING_VERS_ORIG()
        self.PING_VERS_PINGBACK = PING_PROG.PING_VERS_PINGBACK()

    @rpc_version(vers=2)
    class PING_VERS_PINGBACK(object):
        @rpc_procedure(proc=0, args=xdr_void, ret=xdr_void)
        def PINGPROC_NULL(self):
            pass

        @rpc_procedure(proc=1, args=xdr_void, ret=xdr_int)
        def PINGPROC_PINGPROC(self):
            return 0

    @rpc_version(vers=1)
    class PING_VERS_ORIG(object):
        @rpc_procedure(proc=0, args=xdr_void, ret=xdr_void)
        def PINGPROC_NULL(self):
            pass

    PING_VERS = 2


if __name__ == "__main__":
    print("ping_vers: %d" % PING_PROG.PING_VERS)
    print("version 1: %s" % str(PING_PROG.get_version_decl(1)))
    print("version 2: %s" % str(PING_PROG.get_version_decl(2)))
    ping_prog = PING_PROG()
    print("version 1: %s" % str(ping_prog.get_version_impl(1)))
    print("version 2: %s" % str(ping_prog.get_version_impl(2)))
    ping_prog_vers = ping_prog.get_version_impl(PING_PROG.PING_VERS)
    print("proc 1: %s" % str(ping_prog_vers.get_procedure_by_id(1)))
    print("proc PINGPROC_PINGPROC: %s" % str(ping_prog_vers.get_procedure_by_name("PINGPROC_PINGPROC")))


class rpc_client(object):
    def __init__(self, prog, vers):
        self.program = prog
        self.version = self.program.get_version_impl(vers)
        self.xid = 1

    def __getattr__(self, proc):
        procedure = self.version.get_procedure_by_name(proc)
        if not procedure:
            raise AttributeError
        print("procedure: %s" % str(procedure))
        class _procedure(object):
            def __init__(self, procedure, tcp_client, prog, vers, xid):
                self.procedure = procedure
                self.tcp_client = tcp_client
                self.prog = prog
                self.vers = vers
                self.xid = xid
            def __call__(self, arg):
                msg = rpc_msg(xid=self.xid,
                              body=rpc_msg.body(mtype=msg_type.CALL,
                                                cbody=call_body(rpcvers=2,
                                                                prog=self.prog,
                                                                vers=self.vers,
                                                                proc=self.procedure.procedure_id,
                                                                cred=opaque_auth.NONE(),
                                                                verf=opaque_auth.NONE())))
                from xdrlib import Packer
                packer = Packer()
                msg.pack(packer)
                print("msg: %s" % packer.get_buffer())

        xid = self.xid
        self.xid += 1
        return _procedure(procedure, None,
                          self.program.program_id, self.version.version_id, xid)


if __name__ == "__main__":
    print("client!")
    client = rpc_client(PING_PROG(), PING_PROG.PING_VERS)
    print(client)
    print(client.PINGPROC_PINGPROC)
    print("fin!")



class rpc_server(object):
    """
    Run an RPC server.
    """
    def __init__(self, server_port):
        from tcp import tcp_server
        self.tcp_server = tcp_server(server_port)
        self.programs = {}

    def add_program(self, prog):
        self.programs[prog.program_id] = prog

    def cycle_network(self, timeout):
        self.tcp_server.cycle_network(timeout)

    def cycle(self, timeout):
        self.tcp_server.cycle_network(timeout)
        while True:
            m = self.tcp_server.pop_message()
            if not m: break
            client_id, message = m
            print("Got message!")
            print("Client id: %d" % client_id)
            print("Message: %s" % message)
            response = self.handle_message(message, client_id)
            print("Response: %s" % response)
            if response is not None:
                print("Sending response.")
                self.tcp_server.push_message(client_id, response)

    def handle_message(self, opaque_bytes, client_id):
        """
        Handles a message, start to finish.
        Takes the opaque bytes representing the XDR encoded RPC message.
        Produces an RPC reply, also encoded as opaque bytes.
        """
        from xdrlib import Unpacker, Packer
        unpacker = Unpacker(opaque_bytes)
        msg = rpc_msg.unpack(unpacker)
        print(msg.body.mtype.value)
        if msg.body.mtype != msg_type.CALL:
            print("No reply!")
            return None # do not reply to such a bad message.
        #response = self.handle_message(msg,
        #                               opaque_bytes[unpacker.get_position():])
        print("Well-formed message!")
        print("rpc version: %d" % msg.body.cbody.rpcvers)
        print("program id: %d" % msg.body.cbody.prog)
        print("version id: %d" % msg.body.cbody.vers)
        print("procedure id: %d" % msg.body.cbody.proc)
        print("cred flavor: %d" % msg.body.cbody.cred.flavor)
        print("verf flavor: %d" % msg.body.cbody.verf.flavor)
        print("remaining bytes: %s" % opaque_bytes[unpacker.get_position():])

        if msg.body.cbody.cred.flavor == auth_flavor.AUTH_SYS:
            print("using system auth")
            unpacker2 = Unpacker(msg.body.cbody.cred.body.bytes)
            params = authsys_parms.unpack(unpacker2)
            print(params)

        def _pack(reply):
            packer = Packer()
            reply.pack(packer)
            return packer.get_buffer()
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
            print("no such program!")
            reply = rpc_msg(xid=msg.xid,
                            body=_body(mtype=msg_type.REPLY,
                                       rbody=_rbody(stat=reply_stat.MSG_ACCEPTED,
                                                    areply=_areply(verf=opaque_auth.NONE(),
                                                                   reply_data=_rdata(stat=accept_stat.PROG_UNAVAIL)))))
            return _pack(reply)

        program = self.programs[msg.body.cbody.prog]
        print("program: %s" % str(program))
        version = program.get_version_impl(msg.body.cbody.vers)
        print("version: %s" % str(version))
        procedure = version.get_procedure_by_id(msg.body.cbody.proc)
        print("procedure: %s" % str(procedure))
        response = procedure(msg, opaque_bytes[unpacker.get_position():])
        return response




if __name__ == "__main__":
    server = rpc_server(2049)
    for i in range(60):
        print("loop.")
        server.cycle(1000.0)
    import sys
    sys.exit(0)

if __name__ == "__main__":
    print("Ping prog: %s" % dir(PING_PROG))
    print("versions: %s" % PING_PROG.versions())
    for v in PING_PROG.versions():
        print("version: %d" % v.version_id)
    print("dict: %s" % str(PING_PROG.__dict__))
    client = rpc_client(prog=PING_PROG, vers=PING_PROG.PING_VERS)
    print("client: %s" % str(client))
    print("client program: %s" % str(client.program))
    print("client version: %s" % str(client.version))
    p = client.PINGPROC_NULL
    print("client procedure: %s" % str(p))
    p(1)
    sys.exit(0)



'''

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


'''



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

