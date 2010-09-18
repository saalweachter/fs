"""
The basic NFS server itself.
"""

from nfs import *


class verifier_source(object):
    def __init__(self):
        from random import Random
        self.random = Random()
    def get(self):
        return bytes(self.random.sample(range(256), 8))


if __name__ == "__main__":
    source = verifier_source()
    print("getting verifier sources!")
    print(source.get())
    print(source.get())


class NFS_state(object):
    def __init__(self):
        self.clients = []
        self.next_client_id = 1
        self.verifier_source = verifier_source()

    def set_clientid(self, rpc_msg, x, v, k):
        """
        Let:

        x be the value of the client.id subfield of the SETCLIENTID4args
        structure.

        v be the value of the client.verifier subfield of the
        SETCLIENTID4args structure.

        c be the value of the clientid field returned in the
        SETCLIENTID4resok structure.

        k represent the value combination of the fields callback and
        callback_ident fields of the SETCLIENTID4args structure.

        s be the setclientid_confirm value returned in the
        SETCLIENTID4resok structure.
        """
        for client in self.clients:
            if client.xid == rpc_msg.xid:
                return client.c, client.s
        class _client(object):
            def __init__(self, xid, c, x, v, k, s):
                self.xid = xid
                self.c = c
                self.x = x
                self.v = v
                self.k = k
                self.s = s
                self.confirmed = False
        cid = self.next_client_id
        self.next_client_id += 1
        client = _client(rpc_msg.xid, cid, x, v, k, self.verifier_source.get())
        self.clients.append(client)
        return client.c, client.s



@rpc_program(prog=100003)
class NFS4_PROGRAM(object):
    def __init__(self):
        self.NFS_V4 = NFS4_PROGRAM.NFS_V4()
    @rpc_version(vers=4)
    class NFS_V4(object):
        def __init__(self):
            self.state = NFS_state()

        @rpc_procedure(proc=0, args=xdr_void, ret=xdr_void)
        def NFSPROC4_NULL(self):
            pass

        @rpc_procedure(proc=1, args=COMPOUND4args, ret=COMPOUND4res)
        def NFSPROC4_COMPOUND(self, rpc_msg, args):
            print("in nfsproc4_compound")
            print("msg: %s" % str(rpc_msg))
            print("args: %s" % str(args))
            rs = []
            status = nfsstat4.NFS4_OK
            for cmd in args.argarray:
                stat, res = self.execute_command(rpc_msg, cmd)
                rs.append(res)
                status = stat
            return COMPOUND4res(status=status,
                                tag=args.tag,
                                resarray=COMPOUND4res.resarray(rs))

        def execute_command(self, rpc_msg, cmd):
            print("in execute command")
            print("cmd: %s" % str(cmd))
            print("cmd.argop: %d" % cmd.argop)
            if cmd.argop == nfs_opnum4.OP_SETCLIENTID:
                opsetclientid = self.SETCLIENTID(rpc_msg, cmd.opsetclientid)
                return opsetclientid.status, nfs_resop4(resop=nfs_opnum4.OP_SETCLIENTID,
                                                        opsetclientid=opsetclientid)

        def SETCLIENTID(self, rpc_msg, args):
            print("in SETCLIENTID")
            print("client: %s" % str(args.client))
            print("callback: %s" % str(args.callback))
            print("callback_ident: %s" % str(args.callback_ident))
            c, s = self.state.set_clientid(rpc_msg,
                                           args.client.id, args.client.verifier,
                                           (args.callback, args.callback_ident))
            return SETCLIENTID4res(status=nfsstat4.NFS4_OK,
                                   resok4=SETCLIENTID4resok(clientid=c,
                                                            setclientid_confirm=s))


if __name__ == "__main__":
    from rpc import rpc_server
    server = rpc_server(2049)
    server.add_program(NFS4_PROGRAM())
    for i in range(60):
        print("loop.")
        server.cycle(1000.0)
    import sys
    sys.exit(0)



