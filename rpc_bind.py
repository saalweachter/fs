"""
RPC binding protocols.
RFC 1833
"""


from xdr import xdr_struct, xdr_hyper, xdr_uhyper, xdr_array, xdr_string
from xdr import xdr_optional, xdr_opaque, xdr_int, xdr_uint, xdr_bool, xdr_void

from rpc import rpc_program, rpc_version, rpc_procedure


# rpcbind address for TCP/UDP
RPCB_PORT = 111

"""
A mapping of (program, version, network ID) to address

The network identifier  (r_netid):
This is a string that represents a local identification for a
network. This is defined by a system administrator based on local
conventions, and cannot be depended on to have the same value on
every system.
"""
class rpcb(xdr_struct):
    r_prog = xdr_hyper # program number
    r_vers = xdr_uhyper # version number
    r_netid = xdr_array(xdr_string) # network id
    r_addr = xdr_array(xdr_string) # universal address
    r_owner = xdr_array(xdr_string) # owner of this service

class rp__list(xdr_struct):
    rpcb_map = rpcb
    #rpcb_next = xdr_optional(rp__list)
rp__list.rpcb_next = xdr_optional(rp__list)

rpcblist_ptr = xdr_optional(rp__list) # results of RPCBPROC_DUMP

# Arguments of remote calls
class rpcb_rmtcallargs(xdr_struct):
    prog = xdr_uhyper # program number
    vers = xdr_uhyper # version number
    proc = xdr_uhyper # procedure number
    args = xdr_opaque() # argument

# Results of the remote call
class rpcb_rmtcallres(xdr_struct):
    addr = xdr_array(xdr_string) # remote universal address
    results = xdr_opaque() # result

"""
rpcb_entry contains a merged address of a service on a particular
transport, plus associated netconfig information.  A list of
rpcb_entry items is returned by RPCBPROC_GETADDRLIST.  The meanings
and values used for the r_nc_* fields are given below.

The network identifier  (r_nc_netid):

  This is a string that represents a local identification for a
  network.  This is defined by a system administrator based on
  local conventions, and cannot be depended on to have the same
  value on every system.

Transport semantics (r_nc_semantics):
 This represents the type of transport, and has the following values:
    NC_TPI_CLTS     (1)      Connectionless
    NC_TPI_COTS     (2)      Connection oriented
    NC_TPI_COTS_ORD (3)      Connection oriented with graceful close
    NC_TPI_RAW      (4)      Raw transport

Protocol family (r_nc_protofmly):
  This identifies the family to which the protocol belongs.  The
  following values are defined:
    NC_NOPROTOFMLY   "-"
    NC_LOOPBACK      "loopback"
    NC_INET          "inet"
    NC_IMPLINK       "implink"
    NC_PUP           "pup"
    NC_CHAOS         "chaos"
    NC_NS            "ns"
    NC_NBS           "nbs"
    NC_ECMA          "ecma"
    NC_DATAKIT       "datakit"
    NC_CCITT         "ccitt"
    NC_SNA           "sna"
    NC_DECNET        "decnet"
    NC_DLI           "dli"
    NC_LAT           "lat"
    NC_HYLINK        "hylink"
    NC_APPLETALK     "appletalk"
    NC_NIT           "nit"
    NC_IEEE802       "ieee802"
    NC_OSI           "osi"
    NC_X25           "x25"
    NC_OSINET        "osinet"
    NC_GOSIP         "gosip"

Protocol name (r_nc_proto):
  This identifies a protocol within a family.  The following are
  currently defined:
     NC_NOPROTO      "-"
     NC_TCP          "tcp"
     NC_UDP          "udp"
     NC_ICMP         "icmp"
"""

class rpcb_entry(xdr_struct):
    r_maddr = xdr_array(xdr_string) # merged address of service
    r_nc_netid = xdr_array(xdr_string) # netid field
    r_nc_semantics = xdr_uhyper # semantics of transport
    r_nc_protofmly = xdr_array(xdr_string) # protocol family
    r_nc_proto = xdr_array(xdr_string) # protocol name

# A list of addresses supported by a service.
class rpcb_entry_list(xdr_struct):
    rpcb_entry_map = rpcb_entry
#    rpcb_entry_next = xdr_optional(rpcb_entry_list)
rpcb_entry_list.rpcb_entry_next = xdr_optional(rpcb_entry_list)

rpcb_entry_list_ptr = xdr_optional(rpcb_entry_list)

# rpcbind statistics
#rpcb_highproc_2 = RPCBPROC_CALLIT
#rpcb_highproc_3 = RPCBPROC_TADDR2UADDR
#rpcb_highproc_4 = RPCBPROC_GETSTAT

RPCBSTAT_HIGHPROC = 13 # # of procs in rpcbind V4 plus one
RPCBVERS_STAT = 3 # provide only for rpcbind V2, V3 and V4
RPCBVERS_4_STAT = 2
RPCBVERS_3_STAT = 1
RPCBVERS_2_STAT = 0

# Link list of all the stats about getport and getaddr
class rpcbs_addrlist(xdr_struct):
    prog = xdr_uhyper
    vers = xdr_uhyper
    success = xdr_int
    failure = xdr_int
    netid = xdr_array(xdr_string)
#    next = xdr_optional(rpcbs_addrlist)
rpcbs_addrlist.next = xdr_optional(rpcbs_addrlist)

# Link list of all the stats about rmtcall
class rpcbs_rmtcalllist(xdr_struct):
    prog = xdr_uhyper
    vers = xdr_uhyper
    proc = xdr_uhyper
    success = xdr_int
    failure = xdr_int
    indirect = xdr_int # whether callit or indirect
    netid = xdr_array(xdr_string)
#    next = xdr_optional(rpcbs_rmtcalllist)
rpcbs_rmtcalllist.next = xdr_optional(rpcbs_rmtcalllist)

rpcbs_proc = xdr_array(xdr_int, size=RPCBSTAT_HIGHPROC)
rpcbs_addrlist_ptr = xdr_optional(rpcbs_addrlist)
rpcbs_rmtcalllist_ptr = xdr_optional(rpcbs_rmtcalllist)

class rpcb_stat(xdr_struct):
    info = rpcbs_proc
    setinfo = xdr_int
    unsetinfo = xdr_int
    addrinfo = rpcbs_addrlist_ptr
    rmtinfo = rpcbs_rmtcalllist_ptr

# One rpcb_stat structure is returned for each version of rpcbind
# being monitored.
rpcb_stat_byvers = xdr_array(rpcb_stat, size=RPCBVERS_STAT)

# netbuf structure, used to store the transport specific form of
# a universal transport address.
class netbuf(xdr_struct):
    maxlen = xdr_uint
    buf = xdr_opaque()


# rpcbind procedures
@rpc_program(prog=100000)
class RPCBPROG(object):
    @rpc_version(vers=3)
    class RPCBVERS(object):
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

