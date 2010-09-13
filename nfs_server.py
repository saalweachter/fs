"""
The basic NFS server itself.
"""

from nfs import *


@rpc_program(prog=100003)
class NFS4_PROGRAM(object):
    def __init__(self):
        self.NFS_V4 = NFS4_PROGRAM.NFS_V4()
    @rpc_version(vers=4)
    class NFS_V4(object):
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
            return SETCLIENTID4res(status=nfsstat4.NFS4_OK,
                                   resok4=SETCLIENTID4resok(clientid=1,
                                                            setclientid_confirm=b'01234567'))


if __name__ == "__main__":
    from rpc import rpc_server
    server = rpc_server(2049)
    server.add_program(NFS4_PROGRAM())
    for i in range(60):
        print("loop.")
        server.cycle(1000.0)
    import sys
    sys.exit(0)



