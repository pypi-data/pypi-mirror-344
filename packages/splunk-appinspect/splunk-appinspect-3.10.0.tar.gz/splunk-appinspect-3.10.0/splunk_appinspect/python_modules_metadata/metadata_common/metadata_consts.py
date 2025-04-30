from __future__ import annotations

from enum import Enum
from typing import List

from splunk_appinspect.python_modules_metadata.metadata_common.metadata_types import FunctionMetadata


class ModuleNameConsts(Enum):
    """Module name consts."""

    OS = "os"
    DIRCACHE = "dircache"
    LINECACHE = "linecache"
    SHUTIL = "shutil"
    TEMPFILE = "tempfile"
    MACPATH = "macpath"
    CSV = "csv"
    CONFIG_PARSER = "ConfigParser"
    CONFIG_PARSER_PY3 = "configparser"
    PLISTLIB = "plistlib"
    HTTPLIB = "httplib"
    HTTPLIB2 = "httplib2"
    URLLIB = "urllib"
    URLLIB2 = "urllib2"
    REQUESTS = "requests"
    XML = "xml"
    XMLRPCLIB = "xmlrpclib"
    SUBPROCESS = "subprocess"

    # pertain to threading
    THREAD = "thread"
    _THREAD = "_thread"
    THREADING = "threading"
    MULTIPROCESSING = "multiprocessing"

    POSIX = "posix"
    CRYPT = "crypt"
    DL = "dl"
    TERMIOS = "termios"
    TTY = "tty"
    PTY = "pty"
    PIPES = "pipes"
    POSIXFILE = "posixfile"
    SYSLOG = "syslog"
    BASE64 = "base64"
    BINHEX = "binhex"
    EMAIL = "email"
    JSON = "json"
    MIMETOOLS = "mimetools"
    MIMETYPES = "mimetypes"
    MIMEWRITER = "MimeWriter"
    MIMIFY = "mimify"
    MULTIFILE = "mulfile"
    QUOPRI = "quopri"
    UU = "uu"
    ASYNCHAT = "asynchat"
    IO = "io"
    CODE = "code"
    # multimedia module usage
    AIFC = "aifc"
    SUNAU = "sunau"
    WAVE = "wave"
    CHUNK = "chunk"
    GZIP = "gzip"
    BZ2 = "bz2"
    TARFILE = "tarfile"
    ZIPFILE = "zipfile"

    # memory-mapped
    MMAP = "mmap"
    COMMANDS = "commands"
    TRACE = "trace"
    CMD = "cmd"


class TagConsts(Enum):
    """Tag consts."""

    FILE_READ_AND_WRITE = "file_read_and_write"
    HTTP_CONNECTION = "http_connection"
    CRITICAL_SYSTEM_MODULE = "critical_system_module"
    PATH_MANIPULATION = "path_manipulation"
    XML_RPC_CONNECTION = "xml_rpc_connection"
    APPLICATION_LAYER_PROTOCOL_CONNECTION = "application_layer_protocol_connection"
    THREAD_SECURITY = "thread_security"
    DATA_PERSISTENCE = "data_persistence"
    UNIX_SPECIFIC_SERVICES = "unix_specific_service"
    INET_DATA_HANDLING = "internet_data_handling"
    NETWORK_CONNECTION = "network_connection"
    GENERIC_OPERATING_SYSTEM_SERVICES = "generic_operating_system_services"
    MEMORY_OBJECT_MANIPULATION = "memory_object_manipulation"
    STRING_EXECUTION = "string_execution"
    DATA_COMPRESSION = "data_compression"
    MEMORY_MAPPING = "memory_mapping"
    WEB_SERVER = "web_server"
    EXTERNAL_COMMAND_EXECUTION = "external_command_execution"
    MODULE_IMPORTING = "module_importing"

    PY2_ONLY = "py2_only"
    PY3_ONLY = "py3_only"


def file_manipulation_functions() -> List[FunctionMetadata]:
    return [
        FunctionMetadata("open", "__builtin__.open", "manipulate files"),
        FunctionMetadata("file", "__builtin__.file", "manipulate files"),
        FunctionMetadata("execfile", "__builtin__.execfile", "execute python file"),
    ]


def built_in_eval_function() -> FunctionMetadata:
    return FunctionMetadata("eval", "__builtin__.eval", "")
