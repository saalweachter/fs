"""
Basic NFS implementation.
"""

int32_t = xdr_int
uint32_t = xdr_uint
int64_t = xdr_hyper
uint64_t = xdr_uhyper

NFS4_FHSIZE = 128
NFS4_VERIFIER_SIZE = 8
NFS4_OPAQUE_LIMIT = 1024

attrlist4 = xdr_opaque()
bitmap4 = xdr_array(uint32_t)
changeid4 = uint64_t
clientid4 = uint64_t
utf8str_cs = xdr_opaque()
component4 = utf8str_cs
count4 = uint32_t
length4 = uint64_t
linktext4 = utf8str_cs
mode4 = uint32_t
nfs_cookie4 = uint64_t
nfs_fh4 = xdr_opaque(max=NFS4_FHSIZE)
class nfs_ftype4(xdr_enum):
    pass
class nfsstat4(xdr_enum):
    NFS4_OK = 0 # everything is okay
    NFS4ERR_PERM = 1 # caller not privileged
    NFS4ERR_NOENT = 2 # no such file/directory
    NFS4ERR_IO = 5 # hard I/O error
    NFS4ERR_NXIO = 6 # no such device
    NFS4ERR_ACCESS = 13 # access denied
    NFS4ERR_EXIST = 17 # file already exists
    NFS4ERR_XDEV = 18 # different filesystems
    # Unused/reserved        19
    NFS4ERR_NOTDIR = 20 # should be a directory
    NFS4ERR_ISDIR = 21 # should not be directory
    NFS4ERR_INVAL = 22 # invalid argument
    NFS4ERR_FBIG = 27 # file exceeds server max
    NFS4ERR_NOSPC = 28 # no space on filesystem
    NFS4ERR_ROFS = 30 # read-only filesystem
    NFS4ERR_MLINK = 31 # too many hard links
    NFS4ERR_NAMETOOLONG = 63 # name exceeds server max
    NFS4ERR_NOTEMPTY = 66 # directory not empty
    NFS4ERR_DQUOT = 69 # hard quota limit reached
    NFS4ERR_STALE = 70 # file no longer exists
    NFS4ERR_BADHANDLE = 10001 # Illegal filehandle
    NFS4ERR_BAD_COOKIE = 10003 # READDIR cookie is stale
    NFS4ERR_NOTSUPP = 10004 # operation not supported
    NFS4ERR_TOOSMALL = 10005 # response limit exceeded
    NFS4ERR_SERVERFAULT = 10006 # undefined server error
    NFS4ERR_BADTYPE = 10007 # type invalid for CREATE
    NFS4ERR_DELAY = 10008 # file "busy" - retry
    NFS4ERR_SAME = 10009 # nverify says attrs same
    NFS4ERR_DENIED = 10010 # lock unavailable
    NFS4ERR_EXPIRED = 10011 # lock lease expired
    NFS4ERR_LOCKED = 10012 # I/O failed due to lock
    NFS4ERR_GRACE = 10013 # in grace period
    NFS4ERR_FHEXPIRED = 10014 # filehandle expired
    NFS4ERR_SHARE_DENIED = 10015 # share reserve denied
    NFS4ERR_WRONGSEC = 10016 # wrong security flavor
    NFS4ERR_CLID_INUSE = 10017 # clientid in use
    NFS4ERR_RESOURCE = 10018 # resource exhaustion
    NFS4ERR_MOVED = 10019 # filesystem relocated
    NFS4ERR_NOFILEHANDLE = 10020 # current FH is not set
    NFS4ERR_MINOR_VERS_MISMATCH = 10021 # minor vers not supp
    NFS4ERR_STALE_CLIENTID = 10022 # server has rebooted
    NFS4ERR_STALE_STATEID = 10023 # server has rebooted
    NFS4ERR_OLD_STATEID = 10024 # state is out of sync
    NFS4ERR_BAD_STATEID = 10025 # incorrect stateid
    NFS4ERR_BAD_SEQID = 10026 # request is out of seq.
    NFS4ERR_NOT_SAME = 10027 # verify - attrs not same
    NFS4ERR_LOCK_RANGE = 10028 # lock range not supported
    NFS4ERR_SYMLINK = 10029 # should be file/directory
    NFS4ERR_RESTOREFH = 10030 # no saved filehandle
    NFS4ERR_LEASE_MOVED = 10031 # some filesystem moved
    NFS4ERR_ATTRNOTSUPP = 10032 # recommended attr not sup
    NFS4ERR_NO_GRACE = 10033 # reclaim outside of grace
    NFS4ERR_RECLAIM_BAD = 10034 # reclaim error at server
    NFS4ERR_RECLAIM_CONFLICT = 10035 # conflict on reclaim
    NFS4ERR_BADXDR = 10036 # XDR decode failed
    NFS4ERR_LOCKS_HELD = 10037 # file locks held at CLOSE
    NFS4ERR_OPENMODE = 10038 # conflict in OPEN and I/O
    NFS4ERR_BADOWNER = 10039 # owner translation bad
    NFS4ERR_BADCHAR = 10040 # utf-8 char not supported
    NFS4ERR_BADNAME = 10041 # name not supported
    NFS4ERR_BAD_RANGE = 10042 # lock range not supported
    NFS4ERR_LOCK_NOTSUPP = 10043 # no atomic up/downgrade
    NFS4ERR_OP_ILLEGAL = 10044 # undefined operation
    NFS4ERR_DEADLOCK = 10045 # file locking deadlock
    NFS4ERR_FILE_OPEN = 10046 # open file blocks op.
    NFS4ERR_ADMIN_REVOKED = 10047 # lockowner state revoked
    NFS4ERR_CB_PATH_DOWN = 10048 # callback path down

offset4 = uint64_t
pathname4 = xdr_array(component4)
qop4 = uint32_t
sec_oid4 = xdr_opaque()
seqid4 = uint32_t
utf8string = xdr_opaque()
utf8str_cis = xdr_opaque()
utf8str_mixed = xdr_opaque()
verifier4 = xdr_opaque(size=NFS4_VERIFIER_SIZE)
class nfstime(xdr_struct):
    seconds = int64_t
    nseconds = uint32_t
class time_how4(xdr_enum):
    SET_TO_SERVER_TIME4 = 0
    SET_TO_CLIENT_TIME4 = 1
class settime4(xdr_union(set_it=time_how4)):
    SET_TO_CLIENT_TIME4.time = nfstime4


# File access handle
nfs_fh4 = rpc_opaque(max=NFS4_FHSIZE)


# File attribute definitions

# FSID structure for major/minor
class fsid4(xdr_struct):
    major = uint64_t
    minor = uint64_t

# Filesystem locations attribute for relocation/migration

class fs_location4(xdr_struct):
    server = xdr_array(utf8str_cis)
    rootpath = pathname4

class fs_locations4(xdr_struct):
    fs_root = pathname4
    locations = xdr_array(fs_location4)

# Various Access Control Entry definitions

# Mask that indicates which Access Control Entries are supported.
# Values for the fattr4_aclsupport attribute.
ACL4_SUPPORT_ALLOW_ACL = 1
ACL4_SUPPORT_DENY_ACL = 2
ACL4_SUPPORT_AUDIT_ACL = 4
ACL4_SUPPORT_ALARM_ACL = 8

acetype4 = uint32_t
# acetype4 values, others can be added as needed.
ACE4_ACCESS_ALLOWED_ACE_TYPE = 0
ACE4_ACCESS_DENIED_ACE_TYPE = 1
ACE4_SYSTEM_AUDIT_ACE_TYPE = 2
ACE4_SYSTEM_ALARM_ACE_TYPE = 3

# ACE flag
aceflag4 = uint32_t

# ACE flag values
ACE4_FILE_INHERIT_ACE = 0x00000001
ACE4_DIRECTORY_INHERIT_ACE = 0x00000002
ACE4_NO_PROPAGATE_INHERIT_ACE = 0x00000004
ACE4_INHERIT_ONLY_ACE = 0x00000008
ACE4_SUCCESSFUL_ACCESS_ACE_FLAG = 0x00000010
ACE4_FAILED_ACCESS_ACE_FLAG = 0x00000020
ACE4_IDENTIFIER_GROUP = 0x00000040

# ACE mask
acemask4 = uint32_t

# ACE mask values
ACE4_READ_DATA = 0x00000001
ACE4_LIST_DIRECTORY = 0x00000001
ACE4_WRITE_DATA = 0x00000002
ACE4_ADD_FILE = 0x00000002
ACE4_APPEND_DATA = 0x00000004
ACE4_ADD_SUBDIRECTORY = 0x00000004
ACE4_READ_NAMED_ATTRS = 0x00000008
ACE4_WRITE_NAMED_ATTRS = 0x00000010
ACE4_EXECUTE = 0x00000020
ACE4_DELETE_CHILD = 0x00000040
ACE4_READ_ATTRIBUTES = 0x00000080
ACE4_WRITE_ATTRIBUTES = 0x00000100
ACE4_DELETE = 0x00010000
ACE4_READ_ACL = 0x00020000
ACE4_WRITE_ACL = 0x00040000
ACE4_WRITE_OWNER = 0x00080000
ACE4_SYNCHRONIZE = 0x00100000

# ACE4_GENERIC_READ -- defined as combination of
#      ACE4_READ_ACL |
#      ACE4_READ_DATA |
#      ACE4_READ_ATTRIBUTES |
#      ACE4_SYNCHRONIZE

ACE4_GENERIC_READ = 0x00120081

# ACE4_GENERIC_WRITE -- defined as combination of
#      ACE4_READ_ACL |
#      ACE4_WRITE_DATA |
#      ACE4_WRITE_ATTRIBUTES |
#      ACE4_WRITE_ACL |
#      ACE4_APPEND_DATA |
#      ACE4_SYNCHRONIZE

ACE4_GENERIC_WRITE = 0x00160106

# ACE4_GENERIC_EXECUTE -- defined as combination of
#      ACE4_READ_ACL
#      ACE4_READ_ATTRIBUTES
#      ACE4_EXECUTE
#      ACE4_SYNCHRONIZE

ACE4_GENERIC_EXECUTE = 0x001200A0

# Access Control Entry definition

class nfsace4(xdr_struct):
    type = acetype4
    flag = aceflag4
    access_mask = acemask4
    who = utf8str_mixed

# Field definitions for the fattr4_mode attribute
MODE4_SUID = 0x800 # set user id on execution
MODE4_SGID = 0x400 # set group id on execution
MODE4_SVTX = 0x200 # save text even after use
MODE4_RUSR = 0x100 # read permission: owner
MODE4_WUSR = 0x080 # write permission: owner
MODE4_XUSR = 0x040 # execute permission: owner
MODE4_RGRP = 0x020 # read permission: group
MODE4_WGRP = 0x010 # write permission: group
MODE4_XGRP = 0x008 # execute permission: group
MODE4_ROTH = 0x004 # read permission: other
MODE4_WOTH = 0x002 # write permission: other
MODE4_XOTH = 0x001 # execute permission: other

class specdata4(xdr_struct):
    specdata1 = uint32_t
    specdata2 = uint32_t

FH4_PERSISTENT = 0
FH4_NOEXPIRE_WITH_OPEN = 1
FH4_VOLATILE_ANY = 2
FH4_VOL_MIGRATION = 4
FH4_VOL_RENAME = 8

fattr4_supported_attrs = bitmap4
fattr4_type = nfs_ftype4
fattr4_fh_expire_type = uint32_t
fattr4_change = changeid4
fattr4_size = uint64_t
fattr4_link_support = xdr_bool
fattr4_symlink_support = xdr_bool
fattr4_named_attr = xdr_bool
fattr4_fsid = fsid4
fattr4_unique_handles = xdr_bool
fattr4_lease_time = uint32_t
fattr4_rdattr_error = nfsstat4
fattr4_acl = xdr_array(nfsace4)
fattr4_aclsupport = uint32_t
fattr4_archive = xdr_bool
fattr4_cansettime = xdr_bool
fattr4_case_insensitive = xdr_bool
fattr4_case_preserving = xdr_bool
fattr4_chown_restricted = xdr_bool
fattr4_fileid = uint64_t
fattr4_files_avail = uint64_t
fattr4_filehandle = nfs_fh4
fattr4_files_free = uint64_t
fattr4_files_total = uint64_t
fattr4_fs_locations = fs_locations4
fattr4_hidden = xdr_bool
fattr4_homogeneous = xdr_bool
fattr4_maxfilesize = uint64_t
fattr4_maxlink = uint32_t
fattr4_maxname = uint32_t
fattr4_maxread = uint64_t
fattr4_maxwrite = uint64_t
fattr4_mimetype = utf8str_cs
fattr4_mode = mode4
fattr4_mounted_on_fileid = uint64_t
fattr4_no_trunc = xdr_bool
fattr4_numlinks = uint32_t
fattr4_owner = utf8str_mixed
fattr4_owner_group = utf8str_mixed
fattr4_quota_avail_hard = uint64_t
fattr4_quota_avail_soft = uint64_t
fattr4_quota_used = uint64_t
fattr4_rawdev = specdata4
fattr4_space_avail = uint64_t
fattr4_space_free = uint64_t
fattr4_space_total = uint64_t
fattr4_space_used = uint64_t
fattr4_system = xdr_bool
fattr4_time_access = nfstime4
fattr4_time_access_set = settime4
fattr4_time_backup = nfstime4
fattr4_time_create = nfstime4
fattr4_time_delta = nfstime4
fattr4_time_metadata = nfstime4
fattr4_time_modify = nfstime4
fattr4_time_modify_set = settime4

# Mandatory Attributes
FATTR4_SUPPORTED_ATTRS = 0
FATTR4_TYPE = 1
FATTR4_FH_EXPIRE_TYPE = 2
FATTR4_CHANGE = 3
FATTR4_SIZE = 4
FATTR4_LINK_SUPPORT = 5
FATTR4_SYMLINK_SUPPORT = 6
FATTR4_NAMED_ATTR = 7
FATTR4_FSID = 8
FATTR4_UNIQUE_HANDLES = 9
FATTR4_LEASE_TIME = 10
FATTR4_RDATTR_ERROR = 11
FATTR4_FILEHANDLE = 19

# Recommended Attributes
FATTR4_ACL = 12
FATTR4_ACLSUPPORT = 13
FATTR4_ARCHIVE = 14
FATTR4_CANSETTIME = 15
FATTR4_CASE_INSENSITIVE = 16
FATTR4_CASE_PRESERVING = 17
FATTR4_CHOWN_RESTRICTED = 18
FATTR4_FILEID = 20
FATTR4_FILES_AVAIL = 21
FATTR4_FILES_FREE = 22
FATTR4_FILES_TOTAL = 23
FATTR4_FS_LOCATIONS = 24
FATTR4_HIDDEN = 25
FATTR4_HOMOGENEOUS = 26
FATTR4_MAXFILESIZE = 27
FATTR4_MAXLINK = 28
FATTR4_MAXNAME = 29
FATTR4_MAXREAD = 30
FATTR4_MAXWRITE = 31
FATTR4_MIMETYPE = 32
FATTR4_MODE = 33
FATTR4_NO_TRUNC = 34
FATTR4_NUMLINKS = 35
FATTR4_OWNER = 36
FATTR4_OWNER_GROUP = 37
FATTR4_QUOTA_AVAIL_HARD = 38
FATTR4_QUOTA_AVAIL_SOFT = 39
FATTR4_QUOTA_USED = 40
FATTR4_RAWDEV = 41
FATTR4_SPACE_AVAIL = 42
FATTR4_SPACE_FREE = 43
FATTR4_SPACE_TOTAL = 44
FATTR4_SPACE_USED = 45
FATTR4_SYSTEM = 46
FATTR4_TIME_ACCESS = 47
FATTR4_TIME_ACCESS_SET = 48
FATTR4_TIME_BACKUP = 49
FATTR4_TIME_CREATE = 50
FATTR4_TIME_DELTA = 51
FATTR4_TIME_METADATA = 52
FATTR4_TIME_MODIFY = 53
FATTR4_TIME_MODIFY_SET = 54
FATTR4_MOUNTED_ON_FILEID = 55

class fattr4(xdr_struct):
    attrmask = bitmap4
    attr_vals = attrlist4
class change_info4(xdr_struct):
    atomic = xdr_bool
    before = changeid4
    after = changeid4
class clientaddr4(xdr_struct):
    r_netid = xdr_string()
    r_addr = xdr_string()
class cb_client4(xdr_struct):
    cb_program = xdr_uint
    cb_location = clientaddr4
class nfs_client_id4(xdr_struct):
    verifier = verifier4
    id = xdr_opaque(max=NFS4_OPAQUE_LIMIT)
class open_owner4(xdr_struct):
    clientid = clientid4
    owner = xdr_opaque(max=NFS4_OPAQUE_LIMIT)
class lock_owner4(xdr_struct):
    clientid = clientid4
    owner = xdr_opaque(max=NFS4_OPAQUE_LIMIT)
class open_to_lock_owner4(xdr_struct):
    open_seqid = seqid4
    open_stateid = stateid4
    lock_seqid = seqid4
    lock_owner = lock_owner4
class stateid4(xdr_struct):
    seqid = uint32_t
    other = xdr_opaque(size=12)


class SECINFO4args(xdr_struct):
    # CURRENT_FH: directory
    name = component4

# From RFC 2203
class rpc_gss_svc_t(xdr_enum):
    RPC_GSS_SVC_NONE = 1
    RPC_GSS_SVC_INTEGRITY = 2
    RPC_GSS_SVC_PRIVACY = 3

class rpcsec_gss_info(xdr_struct):
    oid = sec_oid4
    qop = qop4
    service = rpc_gss_svc_t


class nfs_lock_type4(xdr_enum):
    READ_LT = 1
    WRITE_LT = 2
    READW_LT = 3 # blocking read
    WRITEW_LT = 4 # blocking write

# ACCESS: Check access permission
ACCESS4_READ = 1
ACCESS4_LOOKUP = 2
ACCESS4_MODIFY = 4
ACCESS4_EXTEND = 8
ACCESS4_DELETE = 16
ACCESS4_EXECUTE = 32

class ACCESS4args(xdr_struct):
    # CURRENT_FH: object
    access = uint32_t

class ACCESS4resok(xdr_struct):
    supported = uint32_t
    access = uint32_t

class ACCESS4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = ACCESS4resok

# CLOSE: Close a file and release share reservations
class CLOSE4args(xdr_struct):
    # CURRENT_FH: object
    seqid = seqid4
    open_stateid = stateid4

class CLOSE4res(xdr_union(status=nfsstat4)):
    NFS4_OK.open_stateid = stateid4

# COMMIT: Commit cached data on server to stable storage
class COMMIT4args(xdr_struct):
    # CURRENT_FH: file
    offset = offset4
    count = count4

class COMMIT4resok(xdr_struct):
    writeverf = verifier4

class COMMIT4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = COMMIT4resok

# CREATE: Create a non-regular file
class createtype4(xdr_union(type=nfs_ftype4)):
    NF4LNK.linkdata = linktext4
    NF4BLK.devdata = specdata4
    NF4CHR.devdata = specdata4

class CREATE4args(xdr_struct):
    # CURRENT_FH: directory for creation
    objtype = createtype4
    objname = component4
    createattrs = fattr4

class CREATE4resok(xdr_struct):
    cinfo = change_info4
    attrset = bitmap4 # attributes set

class CREATE4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = CREATE4resok

# DELEGPURGE: Purge Delegations Awaiting Recovery
class DELEGPURGE4args(xdr_struct):
    clientid = clientid4

class DELEGPURGE4res(xdr_struct):
    status = nfsstat4

# DELEGRETURN: Return a delegation
class DELEGRETURN4args(xdr_struct):
    # CURRENT_FH: delegated file
    deleg_stateid = stateid4

class DELEGRETURN4res(xdr_struct):
    status = nfsstat4

# GETATTR: Get file attributes
class GETATTR4args(xdr_struct):
    # CURRENT_FH: directory or file
    attr_request = bitmap4

class GETATTR4resok(xdr_struct):
    obj_attributes = fattr4

class GETATTR4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = GETATTR4resok

# GETFH: Get current filehandle
class GETFH4resok(xdr_struct):
    object = nfs_fh4

class GETFH4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = GETFH4resok

# LINK: Create link to an object
class LINK4args(xdr_struct):
    # SAVED_FH: source object
    # CURRENT_FH: target directory
    newname = component4

class LINK4resok(xdr_struct):
    cinfo = change_info4

class LINK4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = LINK4resok

# For LOCK, transition from open_owner to new lock_owner
class open_to_lock_owner4(xdr_struct):
    open_seqid = seqid4
    open_stateid = stateid4
    lock_seqid = seqid4
    lock_owner = lock_owner4

# For LOCK, existing lock_owner continues to request file locks
class exist_lock_owner4(xdr_struct):
    lock_stateid = stateid4
    lock_seqid = seqid4

class locker4(xdr_union(new_lock_owner=xdr_bool)):
    TRUE.open_owner = open_to_lock_owner4
    FALSE.lock_owner = exist_lock_owner4

# LOCK/LOCKT/LOCKU: Record lock management
class LOCK4args(xdr_struct):
    # CURRENT_FH: file
    locktype = nfs_lock_type4
    reclaim = xdr_bool
    offset = offset4
    length = length4
    locker = locker4

class LOCK4denied(xdr_struct):
    offset = offset4
    length = length4
    locktype = nfs_lock_type4
    owner = lock_owner4

class LOCK4resok(xdr_struct):
    lock_stateid = stateid4

class LOCK4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = LOCK4resok
    NFS4ERR_DENIED.denied = LOCK4denied

class LOCKT4args(xdr_struct):
    # CURRENT_FH: file
    locktype = nfs_lock_type4
    offset = offset4
    length = length4
    owner = lock_owner4

class LOCKT4res(xdr_union(status=nfsstat4)):
    NFS4ERR_DENIED.denied = LOCK4denied

class LOCKU4args(xdr_struct):
    # CURRENT_FH: file
    locktype = nfs_lock_type4
    seqid = seqid4
    lock_stateid = stateid4
    offset = offset4
    length = length4

class LOCKU4res(xdr_union(status=nfsstat4)):
    NFS4_OK.lock_stateid = stateid4

# LOOKUP: Lookup filename
class LOOKUP4args(xdr_struct):
    # CURRENT_FH: directory
    objname = component4

class LOOKUP4res(xdr_struct):
    # CURRENT_FH: object
    status = nfsstat4

# LOOKUPP: Lookup parent directory
class LOOKUPP4res(xdr_struct):
    # CURRENT_FH: directory
    status = nfsstat4

# NVERIFY: Verify attributes different
class NVERIFY4args(xdr_struct):
    # CURRENT_FH: object
    obj_attributes = fattr4

class NVERIFY4res(xdr_struct):
    status = nfsstat4

# Various definitions for OPEN
class createmode4(xdr_enum):
    UNCHECKED4 = 0
    GUARDED4 = 1
    EXCLUSIVE4 = 2

class createhow4(xdr_union(mode=createmode4)):
    UNCHECKED4.createattrs = fattr4
    GUARDED4.createattrs = fattr4
    EXCLUSIVE4.createverf = verifier4

class opentype4(xdr_enum):
    OPEN4_NOCREATE = 0
    OPEN4_CREATE = 1

class openflag4(xdr_union(opentype=opentype4)):
    OPEN4_CREATE.how = createhow4

# Next definitions used for OPEN delegation
class limit_by4(xdr_enum):
    NFS_LIMIT_SIZE = 1
    NFS_LIMIT_BLOCKS = 2
    # others as needed

class nfs_modified_limit4(xdr_struct):
    num_blocks = uint32_t
    bytes_per_block = uint32_t

class nfs_space_limit4(xdr_union(limitby=limit_by4)):
    # limit specified as file size
    NFS_LIMIT_SIZE.filesize = uint64_t
    # limit specified by number of blocks
    NFS_LIMIT_BLOCKS.mod_blocks = nfs_modified_limit4

# Share Access and Deny constants for open argument
OPEN4_SHARE_ACCESS_READ = 1
OPEN4_SHARE_ACCESS_WRITE = 2
OPEN4_SHARE_ACCESS_BOTH = 3

OPEN4_SHARE_DENY_NONE = 0
OPEN4_SHARE_DENY_READ = 1
OPEN4_SHARE_DENY_WRITE = 2
OPEN4_SHARE_DENY_BOTH = 3

class open_delegation_type4(xdr_enum):
    OPEN_DELEGATE_NONE = 0
    OPEN_DELEGATE_READ = 1
    OPEN_DELEGATE_WRITE = 2

class open_claim_type4(xdr_enum):
    CLAIM_NULL = 0
    CLAIM_PREVIOUS = 1
    CLAIM_DELEGATE_CUR = 2
    CLAIM_DELEGATE_PREV = 3

class open_claim_delegate_cur4(xdr_struct):
    delegate_stateid = stateid4
    file = component4

class open_claim4(xdr_union(claim=open_claim_type4)):
    # No special rights to file. Ordinary OPEN of the specified file.
    CLAIM_NULL.file = component4
    # CURRENT_FH: directory

    # Right to the file established by an open previous to server
    # reboot.  File identified by filehandle obtained at that time
    # rather than by name.
    CLAIM_PREVIOUS.delegate_type = open_delegation_type4
    # CURRENT_FH: file being reclaimed

    # Right to file based on a delegation granted by the server.
    # File is specified by name.
    CLAIM_DELEGATE_CUR.delegate_cur_info = open_claim_delegate_cur4
    # CURRENT_FH: directory

    # Right to file based on a delegation granted to a previous boot
    # instance of the client.  File is specified by name.
    CLAIM_DELEGATE_PREV,file_delegate_prev = component4
    # CURRENT_FH: directory

# OPEN: Open a file, potentially receiving an open delegation
class OPEN4args(xdr_struct):
    seqid = seqid4
    share_access = uint32_t
    share_deny = uint32_t
    owner = open_owner4
    openhow = openflag4
    claim = open_claim4

class open_read_delegation4(xdr_struct):
    # Stateid for delegation
    stateid = stateid4
    # Pre-recalled flag for delegations obtained by reclaim (CLAIM_PREVIOUS)
    recall = xdr_bool
    # Defines users who don't need an ACCESS call to open for read
    permissions = nfsace4

class open_write_delegation4(xdr_struct):
    # Stateid for delegation
    stateid = stateid4
    # Pre-recalled flag for delegations obtained by reclaim (CLAIM_PREVIOUS)
    recall = xdr_bool
    # Defines condition that the client must check to determine whether the
    # file needs to be flushed to the server on close.
    space_limit = nfs_space_limit4
    # Defines users who don't need an ACCESS call as part of a delegated open.
    permissions = nfsace4

class open_delegation4(xdr_union(delegation_type=open_delegation_type4)):
    OPEN_DELEGATE_READ.read = open_read_delegation4
    OPEN_DELEGATE_WRITE.write = open_write_delegation4

# Result flags
# Client must confirm open
OPEN4_RESULT_CONFIRM = 2
# Type of file locking behavior at the server
OPEN4_RESULT_LOCKTYPE_POSIX = 4

class OPEN4resok(xdr_struct):
    stateid = stateid4 # Stateid for open
    cinfo = change_info4 # Directory Change Info
    rflags = uint32_t # Result flags
    attrset = bitmap4 # attribute set for create
    delegation = open_delegation4 # Info on any open delegation

class OPEN4res(xdr_union(status=nfsstat4)):
    # CURRENT_FH: opened file
    NFS4_OK.resok4 = OPEN4resok

# OPENATTR: open named attributes directory
class OPENATTR4args(xdr_struct):
    # CURRENT_FH: object
    createdir = xdr_bool

class OPENATTR4res(xdr_struct):
    # CURRENT_FH: named attr directory
    status = nfsstat4

# OPEN_CONFIRM: confirm the open
class OPEN_CONFIRM4args(xdr_struct):
    # CURRENT_FH: opened file
    open_stateid = stateid4
    seqid = seqid4

class OPEN_CONFIRM4resok(xdr_struct):
    open_stateid = stateid4

class OPEN_CONFIRM4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = OPEN_CONFIRM4resok

# OPEN_DOWNGRADE: downgrade the access/deny for a file
class OPEN_DOWNGRADE4args(xdr_struct):
    # CURRENT_FH: opened file
    open_stateid = stateid4
    seqid = seqid4
    share_access = uint32_t
    share_deny = uint32_t

class OPEN_DOWNGRADE4resok(xdr_struct):
    open_stateid = stateid4

class OPEN_DOWNGRADE4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = OPEN_DOWNGRADE4resok

# PUTFH: Set current filehandle
class PUTFH4args(xdr_struct):
    object = nfs_fh4

class PUTFH4res(xdr_struct):
    # CURRENT_FH:
    status = nfsstat4

# PUTPUBFH: Set public filehandle
class PUTPUBFH4res(xdr_struct):
    # CURRENT_FH: public fh
    status = nfsstat4

# PUTROOTFH: Set root filehandle
class PUTROOTFH4res(xdr_struct):
    # CURRENT_FH: root fh
    status = nfsstat4

# READ: Read from file
class READ4args(xdr_struct):
    # CURRENT_FH: file
    stateid = stateid4
    offset = offset4
    count = count4

class READ4resok(xdr_struct):
    eof = xdr_bool
    data = xdr_opaque()

class READ4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = READ4resok

# READDIR: Read directory
class READDIR4args(xdr_struct):
    # CURRENT_FH: directory
    cookie = nfs_cookie4
    cookieverf = verifier4
    dircount = count4
    maxcount = count4
    attr_request = bitmap4

class entry4(xdr_struct):
    cookie = nfs_cookie4
    name = component4
    attrs = fattr4
    nextentry = xdr_optional(entry4)

class dirlist4(xdr_struct):
    entries = xdr_optional(entry4)
    eof = xdr_bool

class READDIR4resok(xdr_struct):
    cookieverf = verifier4
    reply = dirlist4

class READDIR4res(xdr_union(status=nfsstat4)):
    NFS4_OK.READDIR4resok = resok4

# READLINK: Read symbolic link
class READLINK4resok(xdr_struct):
    link = linktext4

class READLINK4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = READLINK4resok

# REMOVE: Remove filesystem object
class REMOVE4args(xdr_struct):
    # CURRENT_FH: directory
    target = component4

class REMOVE4resok(xdr_struct):
    cinfo = change_info4

class REMOVE4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = REMOVE4resok

# RENAME: Rename directory entry
class RENAME4args(xdr_struct):
    # SAVED_FH: source directory
    oldname = component4
    # CURRENT_FH: target directory
    newname = component4

class RENAME4resok(xdr_struct):
    source_cinfo = change_info4
    target_cinfo = change_info4

class RENAME4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = RENAME4resok

# RENEW: Renew a Lease
class RENEW4args(xdr_struct):
    clientid = clientid4

class RENEW4res(xdr_struct):
    status = nfsstat4

# RESTOREFH: Restore saved filehandle
class RESTOREFH4res(xdr_struct):
    # CURRENT_FH: value of saved fh
    status = nfsstat4

# SAVEFH: Save current filehandle
class SAVEFH4res(xdr_struct):
    # SAVED_FH: value of current fh
    status = nfsstat4

# RPCSEC_GSS has a value of '6' - See RFC 2203
class secinfo4(xdr_union(flavor=uint32_t)):
    RPCSEC_GSS.flavor_info = rpcsec_gss_info

SECINFO4resok = xdr_array(secinfo4)

class SECINFO4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = SECINFO4resok

class SETATTR4args(xdr_struct):
    # CURRENT_FH: target object
    stateid = stateid4
    obj_attributes = fattr4

class SETATTR4res(xdr_struct):
    status = nfsstat4
    attrsset = bitmap4

class SETCLIENTID4args(xdr_struct):
    client = nfs_client_id4
    callback = cb_client4
    callback_ident = uint32_t

class SETCLIENTID4resok(xdr_struct):
    clientid = clientid4
    setclientid_confirm = verifier4

class SETCLIENTID4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = SETCLIENTID4resok
    NFS4ERR_CLID_INUSE.client_using = clientaddr4

class SETCLIENTID_CONFIRM4args(xdr_struct):
    clientid = clientid4
    setclientid_confirm = verifier4

class SETCLIENTID_CONFIRM4res(xdr_struct):
    status = nfsstat4

class VERIFY4args(xdr_struct):
    # CURRENT_FH: object
    obj_attributes = fattr4

class VERIFY4res(xdr_struct):
    status = nfsstat4

class stable_how4(xdr_enum):
    UNSTABLE4 = 0
    DATA_SYNC4 = 1
    FILE_SYNC4 = 2

class WRITE4args(xdr_struct):
    # CURRENT_FH: file
    stateid = stateid4
    offset = offset4
    stable = stable_how4
    data = xdr_opaque()

class WRITE4resok(xdr_struct):
    count = count4
    committed = stable_how4
    writeverf = verifier4

class WRITE4res(xdr_union(status=nfsstat4)):
    NFS4_OK.resok4 = WRITE4resok

class RELEASE_LOCKOWNER4args(xdr_struct):
    lock_owner = lock_owner4

class RELEASE_LOCKOWNER4res(xdr_struct):
    status = nfsstat4

class ILLEGAL4res(xdr_struct):
    status = nfsstat4

class nfs_opnum4(xdr_enum):
    OP_ACCESS = 3
    OP_CLOSE = 4
    OP_COMMIT = 5
    OP_CREATE = 6
    OP_DELEGPURGE = 7
    OP_DELEGRETURN = 8
    OP_GETATTR = 9
    OP_GETFH = 10
    OP_LINK = 11
    OP_LOCK = 12
    OP_LOCKT = 13
    OP_LOCKU = 14
    OP_LOOKUP = 15
    OP_LOOKUPP = 16
    OP_NVERIFY = 17
    OP_OPEN = 18
    OP_OPENATTR = 19
    OP_OPEN_CONFIRM = 20
    OP_OPEN_DOWNGRADE = 21
    OP_PUTFH = 22
    OP_PUTPUBFH = 23
    OP_PUTROOTFH = 24
    OP_READ = 25
    OP_READDIR = 26
    OP_READLINK = 27
    OP_REMOVE = 28
    OP_RENAME = 29
    OP_RENEW = 30
    OP_RESTOREFH = 31
    OP_SAVEFH = 32
    OP_SECINFO = 33
    OP_SETATTR = 34
    OP_SETCLIENTID = 35
    OP_SETCLIENTID_CONFIRM = 36
    OP_VERIFY = 37
    OP_WRITE = 38
    OP_RELEASE_LOCKOWNER = 39
    OP_ILLEGAL = 10044

class nfs_argop4(xdr_union(argop=nfs_opnum4)):
    OP_ACCESS.opaccess = ACCESS4args
    OP_CLOSE.opclose = CLOSE4args
    OP_COMMIT.opcommit = COMMIT4args
    OP_CREATE.opcreate = CREATE4args
    OP_DELEGPURGE.opdelegpurge = DELEGPURGE4args
    OP_DELEGRETURN.opdelegreturn = DELEGRETURN4args
    OP_GETATTR.opgetattr = GETATTR4args
    # OP_GETFH.blah = rpc_void
    OP_LINK.oplink = LINK4args
    OP_LOCK.oplock = LOCK4args
    OP_LOCKT.oplockt = LOCKT4args
    OP_LOCKU.oplocku = LOCKU4args
    OP_LOOKUP.oplookup = LOOKUP4args
    # OP_LOOKUPP.blah = rpc_void
    OP_NVERIFY.opnverify = NVERIFY4args
    OP_OPEN.opopen = OPEN4args
    OP_OPENATTR.opopenattr = OPENATTR4args
    OP_OPEN_CONFIRM.opopen_confirm = OPEN_CONFIRM4args
    OP_OPEN_DOWNGRADE.opopen_downgrade = OPEN_DOWNGRADE4args
    OP_PUTFH.opputfh = PUTFH4args
    # OP_PUTPUBFH.blah = rpc_void
    # OP_PUTROOTFH.blah = rpc_void
    OP_READ.opread = READ4args
    OP_READDIR.opreaddir = READDIR4args
    # OP_READLINK.blah = rpc_void
    OP_REMOVE.opremove = REMOVE4args
    OP_RENAME.oprename = RENAME4args
    OP_RENEW.oprenew = RENEW4args
    # OP_RESTOREFH.blah = rpc_void
    # OP_SAVEFH.blah = rpc_void
    OP_SECINFO.opsecinfo = SECINFO4args
    OP_SETATTR.opsetattr = SETATTR4args
    OP_SETCLIENTID.opsetclientid = SETCLIENTID4args
    OP_SETCLIENTID_CONFIRM.opsetclientid_confirm = SETCLIENTID_CONFIRM4args
    OP_VERIFY.opverify = VERIFY4args
    OP_WRITE.opwrite = WRITE4args
    OP_RELEASE_LOCKOWNER.oprelease_lockowner = RELEASE_LOCKOWNER4args
    # OP_ILLEGAL.blah = rpc_void

class nfs_resop4(xdr_union(resop=nfs_opnum4)):
    OP_ACCESS.opaccess = ACCESS4res
    OP_CLOSE.opclose = CLOSE4res
    OP_COMMIT.opcommit = COMMIT4res
    OP_CREATE.opcreate = CREATE4res
    OP_DELEGPURGE.opdelegpurge = DELEGPURGE4res
    OP_DELEGRETURN.opdelegreturn = DELEGRETURN4res
    OP_GETATTR.opgetattr = GETATTR4res
    OP_GETFH.opgetfh = GETFH4res
    OP_LINK.oplink = LINK4res
    OP_LOCK.oplock = LOCK4res
    OP_LOCKT.oplockt = LOCKT4res
    OP_LOCKU.oplocku = LOCKU4res
    OP_LOOKUP.oplookup = LOOKUP4res
    OP_LOOKUPP.oplookupp = LOOKUPP4res
    OP_NVERIFY.opnverify = NVERIFY4res
    OP_OPEN.opopen = OPEN4res
    OP_OPENATTR.opopenattr = OPENATTR4res
    OP_OPEN_CONFIRM.opopen_confirm = OPEN_CONFIRM4res
    OP_OPEN_DOWNGRADE.opopen_downgrade = OPEN_DOWNGRADE4res
    OP_PUTFH.opputfh = PUTFH4res
    OP_PUTPUBFH.opputpubfh = PUTPUBFH4res
    OP_PUTROOTFH.opputrootfh = PUTROOTFH4res
    OP_READ.opread = READ4res
    OP_READDIR.opreaddir = READDIR4res
    OP_READLINK.opreadlink = READLINK4res
    OP_REMOVE.opremove = REMOVE4res
    OP_RENAME.oprename = RENAME4res
    OP_RENEW.oprenew = RENEW4res
    OP_RESTOREFH.oprestorefh = RESTOREFH4res
    OP_SAVEFH.opsavefh = SAVEFH4res
    OP_SECINFO.opsecinfo = SECINFO4res
    OP_SETATTR.opsetattr = SETATTR4res
    OP_SETCLIENTID.opsetclientid = SETCLIENTID4res
    OP_SETCLIENTID_CONFIRM.opsetclientid_confirm = SETCLIENTID_CONFIRM4res
    OP_VERIFY.opverify = VERIFY4res
    OP_WRITE.opwrite = WRITE4res
    OP_RELEASE_LOCKOWNER.oprelease_lockowner =  RELEASE_LOCKOWNER4res
    OP_ILLEGAL.opillegal = ILLEGAL4res

class COMPOUND4args(xdr_struct):
    tag = utf8str_cs
    minorversion = uint32_t
    argarray = xdr_array(nfs_argop4)

class COMPOUND4res(xdr_struct):
    status = nfsstat4
    tag = utf8str_cs
    resarray = xdr_array(nfs_resop4)

class NFS4_PROGRAM(rpc_program(prog=10003)):
    NFS_V4 = rpc_version(vers=4)
    NFS_V4.NFSPROC4_NULL = rpc_procedure(proc=0,
                                         args=rpc_void,
                                         ret=rpc_void)
    NFS_V4.NFSPROC4_COMPOUND = rpc_procedure(proc=1,
                                             args=COMPOUND4args,
                                             ret=COMPOUND4res)

