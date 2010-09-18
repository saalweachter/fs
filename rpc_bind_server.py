"""
RPC bind server.

"""

from rpc_bind import *


@rpc_program(prog=100000)
class RPCBPROG(object):
    def __init__(self):
        self.RPCBVERS = RPCBPROG.RPCBVERS()
        self.RPCBVERS4 = RPCBPROG.RPCBVERS4()

    @rpc_version(vers=3)
    class RPCBVERS(object):
        def __init__(self):
            pass
        @rpc_procedure(proc=1, args=rpcb, ret=xdr_bool)
        def RPCBPROC_SET(self, arg):
            pass
        @rpc_procedure(proc=2, args=rpcb, ret=xdr_bool)
        def RPCBPROC_UNSET(self, arg):
            pass
        @rpc_procedure(proc=3, args=rpcb, ret=xdr_string)
        def RPCBPROC_GETADDR(self, arg):
            pass
        @rpc_procedure(proc=4, args=xdr_void, ret=rpcblist_ptr)
        def RPCBPROC_DUMP(self, arg):
            pass
        @rpc_procedure(proc=5, args=rpcb_rmtcallargs, ret=rpcb_rmtcallres)
        def RPCBPROC_CALLIT(self, arg):
            pass
        @rpc_procedure(proc=6, args=xdr_void, ret=xdr_uint)
        def RPCBPROC_GETTIME(self, arg):
            pass
        @rpc_procedure(proc=7, args=xdr_string, ret=netbuf)
        def RPCBPROC_UADDR2TADDR(self, arg):
            pass
        @rpc_procedure(proc=1, args=netbuf, ret=xdr_string)
        def RPCBPROC_TADDR2UADDR(self, arg):
            pass

    @rpc_version(vers=4)
    class RPCBVERS4(object):
        def __init__(self):
            pass
        @rpc_procedure(proc=1, args=rpcb, ret=xdr_bool)
        def RPCBPROC_SET(self, arg):
            pass
        @rpc_procedure(proc=2, args=rpcb, ret=xdr_bool)
        def RPCBPROC_UNSET(self, arg):
            pass
        @rpc_procedure(proc=3, args=rpcb, ret=xdr_string)
        def RPCBPROC_GETADDR(self, arg):
            pass
        @rpc_procedure(proc=4, args=xdr_void, ret=rpcblist_ptr)
        def RPCBPROC_DUMP(self):
            pass
        @rpc_procedure(proc=5, args=rpcb_rmtcallargs, ret=rpcb_rmtcallres)
        def RPCBPROC_BCAST(self, arg):
            """
            NOTE: RPCBPROC_BCAST has the same functionality as CALLIT;
            the new name is intended to indicate that this
            procedure should be used for broadcast RPC, and
            RPCBPROC_INDIRECT should be used for indirect calls.
            """
            pass
        @rpc_procedure(proc=6, args=xdr_void, ret=xdr_uint)
        def RPCBPROC_GETTIME(self):
            pass
        @rpc_procedure(proc=7, args=xdr_string, ret=netbuf)
        def RPCBPROC_UADDR2TADDR(self, arg):
            pass
        @rpc_procedure(proc=8, args=netbuf, ret=xdr_string)
        def RPCBPROC_TADDR2UADDR(self, arg):
            pass
        @rpc_procedure(proc=9, args=rpcb, ret=xdr_string)
        def RPCBPROC_GETVERSADDR(self, arg):
            pass
        @rpc_procedure(proc=10, args=rpcb_rmtcallargs, ret=rpcb_rmtcallres)
        def RPCBPROC_INDIRECT(self, arg):
            pass
        @rpc_procedure(proc=11, args=rpcb, ret=rpcb_entry_list_ptr)
        def RPCBPROC_GETADDRLIST(self, arg):
            pass
        @rpc_procedure(proc=12, args=xdr_void, ret=rpcb_stat_byvers)
        def RPCBPROC_GETSTAT(self):
            pass


if __name__ == "__main__":
    from rpc import rpc_server
    server = rpc_server(111)
    server.add_program(RPCBPROG())
    for i in range(60):
        print("loop.")
        server.cycle(1000.0)
    import sys
    sys.exit(0)

