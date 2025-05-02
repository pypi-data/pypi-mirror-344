"""Logging module of FIAT."""

import atexit
import io
import os
import queue
import re
import sys
import threading
import time
import traceback
import weakref
from enum import Enum
from string import Formatter as StrFormatter
from warnings import warn

from fiat.util import NOT_IMPLEMENTED

DEFAULT_FMT = "{asctime:20s}{levelname:8s}{message}"
DEFAULT_TIME_FMT = "%Y-%m-%d %H:%M:%S"
RECEIVER_COUNT = 1
STREAM_COUNT = 1

_Global_and_Destruct_Lock = threading.RLock()
_handlers = weakref.WeakValueDictionary()
_loggers = weakref.WeakValueDictionary()
_receivers = weakref.WeakValueDictionary()

_str_formatter = StrFormatter()
del StrFormatter


def global_acquire():
    """Global method for acquiring global lock."""
    if _Global_and_Destruct_Lock:
        _Global_and_Destruct_Lock.acquire()


def global_release():
    """Global method for releasing global lock."""
    if _Global_and_Destruct_Lock:
        _Global_and_Destruct_Lock.release()


def _Destruction():
    """Clean up at interpreter exit."""
    items = list(_handlers.items())
    for _, handler in items:
        handler.acquire()
        if not handler.stream.closed:
            handler.flush()
        handler.close()
        handler.release()
    items = list(_receivers.items())
    for _, receiver in items:
        receiver.close()


atexit.register(_Destruction)


def check_loglevel(level):
    """Check if level can be used."""
    if isinstance(level, int) and level not in LogLevels._value2member_map_:
        raise ValueError(f"Level ({level}) is not a valid log level.")
    elif isinstance(level, str):
        level = level.upper()
        if level not in LogLevels._member_map_:
            raise ValueError(f"Level ({level}) is not a valid log level.")
        else:
            level = LogLevels[level].value
    elif not isinstance(level, (int, str)):
        raise TypeError(f"Level ({level}) of incorrect type -> type: {type(level)}")
    return level


class LogLevels(Enum):
    """Dumb c-like thing."""

    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    DEAD = 5


class LogItem:
    """A logging item.

    Parameters
    ----------
    level : str
        Logging level.
    msg : str
        The message.
    """

    def __init__(
        self,
        level: str,
        msg: str,
    ):
        self.ct = time.time()
        self.level = level
        self.levelname = LogLevels(level).name
        self.msg = msg

    def get_message(
        self,
    ):
        """Return the message."""
        return str(self.msg)


class FormatStyler:
    """The underlying engine of the formatter.

    Parameters
    ----------
    fmt : str
        The format of the message.
    defaults : dict, optional
        Default values, by default None
    """

    default_format = "{message}"
    asctime_format = "{asctime}"
    asctime_search = "{asctime"

    fmt_spec = re.compile(
        r"^(.?[<>=^])?[+ -]?#?0?(\d+|{\w+})?[,_]?(\.(\d+|{\w+}))?[bcdefgnosx%]?$", re.I
    )
    field_spec = re.compile(r"^(\d+|\w+)(\.\w+|\[[^]]+\])*$")

    def __init__(self, fmt: str, *, defaults: dict = None):
        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def uses_time(self):
        """Check if time is used in the formatter."""
        return self._fmt.find(self.asctime_search) >= 0

    def validate(self):
        """Validate the input format, ensure correct string formatting style."""
        fields = set()
        try:
            for _, fieldname, spec, conversion in _str_formatter.parse(self._fmt):
                if fieldname:
                    if not self.field_spec.match(fieldname):
                        raise ValueError(
                            "invalid field name/expression: %r" % fieldname
                        )
                    fields.add(fieldname)
                if conversion and conversion not in "rsa":
                    raise ValueError("invalid conversion: %r" % conversion)
                if spec and not self.fmt_spec.match(spec):
                    raise ValueError("bad specifier: %r" % spec)
        except ValueError as e:
            raise ValueError("invalid format: %s" % e)
        if not fields:
            raise ValueError("invalid format: no fields")

    def _format(self, record):
        if defaults := self._defaults:
            values = defaults | record.__dict__
        else:
            values = record.__dict__
        return self._fmt.format(**values)

    def format(self, record):
        """Format the record."""
        try:
            return self._format(record)
        except KeyError as e:
            raise ValueError("Formatting field not found in record: %s" % e)


class MessageFormatter(object):
    """Format logging items.

    Parameters
    ----------
    fmt : str, optional
        The format, by default None
    datefmt : str, optional
        The date(time) format, by default None
    validate : bool, optional
        Validate the supplied formats, by default True
    defaults : dict, optional
        Default values, by default None
    """

    _conv = time.localtime

    def __init__(
        self,
        fmt: str = None,
        datefmt: str = None,
        validate: bool = True,
        *,
        defaults: dict = None,
    ):
        self._style = FormatStyler(fmt, defaults=defaults)
        if validate:
            self._style.validate()

        self._fmt = self._style._fmt
        self.datefmt = datefmt

    def format_time(self, record):
        """Format the time."""
        ct = self._conv(record.ct)
        if datefmt := self.datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = time.strftime(DEFAULT_TIME_FMT, ct)
        return s

    def format_exception(self, ei):
        """Format an exception."""
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s

    def uses_time(self):
        """Check if the format uses the creation time of the record."""
        return self._style.uses_time()

    def format_message(self, record):
        """Format the message."""
        return self._style.format(record)

    def format(self, record: LogItem):
        """Format a record.

        Parameters
        ----------
        record : LogItem
            The record to be formatted.

        Returns
        -------
        str
            Formatted record/ message.
        """
        record.message = record.get_message()
        if self.uses_time():
            record.asctime = self.format_time(record)
        s = self.format_message(record)
        if s[-1:] != "\n":
            s = s + "\n"
        return s


_default_formatter = MessageFormatter(DEFAULT_FMT, DEFAULT_TIME_FMT)


class BaseHandler:
    """Create base class for all stream handlers.

    Parameters
    ----------
    level : int, optional
        Logging level, by default 2 (INFO)
    """

    def __init__(
        self,
        level: int = 2,
    ):
        self.level = check_loglevel(level)
        self.msg_formatter = None
        self._name = None
        self._closed = False

        self._make_lock()

    def __repr__(self):
        _mem_loc = f"{id(self):#018x}".upper()
        return f"<{self.__class__.__name__} object at {_mem_loc}>"

    def _add_global_stream_ref(
        self,
    ):
        """Add a global reference for this handler."""
        global_acquire()
        _handlers[self._name] = self
        global_release()

    def _make_lock(self):
        """Create a lock."""
        self._lock = threading.RLock()

    def acquire(self):
        """Acquire the lock."""
        self._lock.acquire()

    def release(self):
        """Release the lock."""
        self._lock.release()

    def close(self):
        """Close and clean up."""
        global_acquire()
        self._closed = True
        del _handlers[self._name]
        global_release()

    def emit(self):
        """Emit a message."""
        raise NotImplementedError(NOT_IMPLEMENTED)

    def flush(self):
        """Flush."""
        raise NotImplementedError(NOT_IMPLEMENTED)

    def format(
        self,
        record: LogItem,
    ):
        """Format a record.

        Parameters
        ----------
        record : LogItem
            The records.

        Returns
        -------
        str
            Formatted record (message)
        """
        if self.msg_formatter:
            msg_fmt = self.msg_formatter
        else:
            msg_fmt = _default_formatter
        return msg_fmt.format(record)

    def set_formatter(
        self,
        formatter: MessageFormatter,
    ):
        """Set the message formatter.

        Parameters
        ----------
        formatter : MessageFormatter
            The formatter.
        """
        self.msg_formatter = formatter


class Sender(BaseHandler):
    """Sender object for records.

    Parameters
    ----------
    queue : object
        The queue for the records. Specifically designed for use in multiprocessing.
    """

    def __init__(self, queue: object):
        BaseHandler.__init__(self)
        self.q = queue

    def put(self, record):
        """Put a record in the queue."""
        self.q.put_nowait(record)

    def emit(self, record):
        """Emit a record."""
        try:
            self.put(record)
        except Exception:
            self.handleError(record)


class CHandler(BaseHandler):
    """Output text to the console.

    Parameters
    ----------
    level : int, optional
        Logging level, by default 2 (INFO)
    stream : type, optional
        Stream to which to send the logging messages.
        If none is provided, stdout is chosen. By default None
    name : str, optional
        Name of the added handler, by default None
    """

    def __init__(
        self,
        level: int = 2,
        stream: type = None,
        name: str = None,
    ):
        BaseHandler.__init__(self, level=level)

        if stream is None:
            stream = sys.stdout
        self.stream = stream

        if name is None:
            if hasattr(self.stream, "name"):
                self._name = self.stream.name
            else:
                global STREAM_COUNT
                self._name = f"Stream{STREAM_COUNT}"
                STREAM_COUNT += 1
        else:
            self._name = name

        self._add_global_stream_ref()

    def emit(self, record):
        """Emit a certain message."""
        msg = self.format(record)
        self.stream.write(msg)
        self.flush()

    def flush(self):
        """Dump cache to desired destination."""
        self.acquire()
        self.stream.flush()
        self.release()


class FileHandler(CHandler):
    """Output text to a file.

    Parameters
    ----------
    level : int
        Logging level.
    dst : str
        The destination of the logging (text) file.
    name : str, optional
        The name of the file handler, by default None
    mode : str, optional
        Mode in which to open the log file, by default 'w'
    """

    def __init__(
        self,
        level: int,
        dst: str,
        name: str = None,
        mode: str = "w",
    ):
        if name is None:
            name = "log_default"
        self._filename = os.path.join(dst, f"{name}.log")
        CHandler.__init__(self, level, self._open(mode), name)

    def _open(
        self,
        mode: str = "w",
    ):
        """Open a txt file and return the handler."""
        return open(self._filename, mode)

    def close(self):
        """Close and clean up."""
        self.acquire()
        self.flush()

        stream = self.stream
        self.stream = None

        stream.close()
        CHandler.close(self)
        self.release()


class DummyLog:
    """Create dummy class for tracking children.

    (actually funny..).
    """

    def __init__(
        self,
        obj,
    ):
        self.child_tree = {obj: None}

    def __repr__(self):
        _mem_loc = f"{id(self):#018x}".upper()
        return f"<{self.__class__.__name__} object at {_mem_loc}>"

    def _check_succession(
        self,
        obj,
    ):
        """Remove child if older one is present."""
        _disinherit = [
            child for child in self.child_tree if child.name.startswith(obj.name)
        ]

        for child in _disinherit:
            del self.child_tree[child]

    def add_to_chain(self, obj):
        """Add object to the tree."""
        self._check_succession(obj)
        self.child_tree[obj] = None


class LogManager:
    """The manager of all the loggers."""

    def __init__(
        self,
    ):
        self.logger_tree = {}

    def _check_children(
        self,
        obj: DummyLog,
        logger: "Logger",
    ):
        """Ensure the hierarchy is corrected downwards."""
        name = logger.name

        for child in obj.child_tree.keys():
            if child.parent is None:
                child.parent = logger
            elif not child.parent.name.startswith(name):
                if logger.parent is not child.parent:
                    logger.parent = child.parent
                child.parent = logger

    def _check_parents(self, logger: "Logger"):
        """Ensure the hierarchy is corrected upwards."""
        name = logger.name
        parent = None
        parts = name.split(".")

        if len(parts) == 1:
            return
        _l = len(parts) - 1

        for idx in range(_l):
            sub = parts[0 : _l - idx]
            substr = ".".join(sub)

            if substr not in self.logger_tree:
                self.logger_tree[substr] = DummyLog(logger)
            else:
                obj = self.logger_tree[substr]
                if isinstance(obj, Logger):
                    parent = obj
                    break
                else:
                    obj.add_to_chain(logger)

        logger.parent = parent
        if parent is not None:
            logger.level = parent.level

    def resolve_logger_tree(
        self,
        logger: "Logger",
    ):
        """Solve the logger family tree."""
        obj = None
        name = logger.name

        global_acquire()
        if name in self.logger_tree:
            obj = self.logger_tree[name]
            if isinstance(obj, DummyLog):
                self.logger_tree[name] = logger
                self._check_children(obj, logger)
                self._check_parents(logger)
                obj = None
        else:
            self.logger_tree[name] = logger
            self._check_parents(logger)
        global_release()

        return obj


class Logmeta(type):
    """Meta class for logging."""

    def __call__(
        cls,
        name: str,
        level: int = 2,
    ):
        """Override default calling behaviour.

        To accommodate the check in the logger tree.
        """
        obj = cls.__new__(cls, name, level)
        cls.__init__(obj, name, level)

        res = Logger.manager.resolve_logger_tree(obj)
        if res is not None:
            warn(
                f"{name} is already in use -> returning currently known object",
                UserWarning,
            )
            obj = res

        return obj


class Receiver:
    """Create a receiver for multiprocessing logging.

    Essentially a listener.

    Parameters
    ----------
    queue : object
        A queue for putting the messages in. This has to be a designated
        multiprocessing object.
    """

    _sentinel = None

    def __init__(
        self,
        queue: object,
    ):
        self._closed = False
        self._t = None
        self._handlers = []
        self.count = 0
        self.q = queue

        global RECEIVER_COUNT
        self._name = f"Receiver{RECEIVER_COUNT}"
        RECEIVER_COUNT += 1

        self._add_global_receiver_ref()

    def _add_global_receiver_ref(
        self,
    ):
        """Add a global reference for the reciever."""
        global_acquire()
        _receivers[self._name] = self
        global_release()

    def _log(
        self,
        record: LogItem,
    ):
        """Log an item."""
        for handler in self._handlers:
            if record.level >= handler.level:
                handler.emit(record)

    def _waiting(self):
        """Wait for the next item/ record to be received."""
        while True:
            try:
                record = self.get(True)
                if record is self._sentinel:
                    break
                self._log(record)
                self.count += 1
            except queue.Empty:
                break

    def close(self):
        """Close the receiver."""
        if not self._closed:
            self.q.put_nowait(self._sentinel)
            self._t.join()
            self._t = None
            self._closed = True
        global_acquire()
        del _receivers[self._name]
        global_release()

    def close_handlers(self):
        """Close all associated handlers."""
        for handler in self._handlers:
            handler.close()
            handler = None

    def get(
        self,
        block: bool = True,
    ):
        """Get something from the pipeline.

        Parameters
        ----------
        block : bool, optional
            If set to `True`, it will wait until it receives something.
        """
        return self.q.get(block=block)

    def add_handler(
        self,
        handler: object,
    ):
        """Add a handler to the receiver.

        Parameters
        ----------
        handler : object
            A stream of some sorts.
        """
        self._handlers.append(handler)

    def start(self):
        """Start the receiver.

        This will spawn a thread that manages the receiver.
        """
        self._t = t = threading.Thread(
            target=self._waiting,
            name="mp_logging_thread",
            daemon=True,
        )
        t.start()


class Logger(metaclass=Logmeta):
    """Generate a logger.

    The list of available logging levels:\n
    - 1: debug
    - 2: info
    - 3: warning
    - 4: error
    - 5: dead

    Parameters
    ----------
    name : str
        Logger identifier
    level : int, optional
        Level of the logger. Anything below this level will not be logged.
        For instance, a logging level of `2` (info) will result in all debug messages
        being muted.
    """

    manager = LogManager()

    # def __new__(
    #     cls,
    #     name: str,
    #     level: int = 2,
    # ):

    #     obj = object.__new__(cls)
    #     obj.__init__(name, level)

    #     res = Log.manager.fit_external_logger(obj)
    #     if res is not None:
    #         warn(f"{name} is already in use -> \
    # returning currently known object", UserWarning)
    #         obj = res

    #     return obj

    def __init__(
        self,
        name: str,
        level: int = 2,
    ):
        self._level = check_loglevel(level)
        self.name = name
        self.bubble_up = True
        self.parent = None
        self._handlers = []

        _loggers[self.name] = self

    def __del__(self):
        pass

    def __repr__(self):
        _lvl_str = str(LogLevels(self.level)).split(".")[1]
        return f"<Logger {self.name} level={_lvl_str}>"

    def __str__(self):
        _mem_loc = f"{id(self):#018x}".upper()
        return f"<{self.__class__.__name__} object at {_mem_loc}>"

    def _log(self, record):
        """Handle logging."""
        obj = self
        while obj:
            for handler in obj._handlers:
                if record.level < handler.level:
                    continue
                else:
                    handler.emit(record)
            if not obj.bubble_up:
                obj = None
            else:
                obj = obj.parent

    def _handle_log(log_m):
        """Wrap logging messages."""

        def handle(self, *args, **kwargs):
            lvl, msg = log_m(self, *args, **kwargs)
            self._log(LogItem(level=lvl, msg=msg))

        return handle

    def add_handler(
        self,
        level: int = 2,
        name: str = None,
        stream: type = None,
    ):
        """Add an outlet to the logging object.

        Parameters
        ----------
        level : int, optional
            Logging level, by default 2 (INFO)
        name : str, optional
            Name of the added handler, by default None
        stream : type, optional
            Stream to which to send the logging messages.
            If none is provided, stdout is chosen. By default None
        """
        self._handlers.append(CHandler(level=level, name=name, stream=stream))

    def add_file_handler(
        self,
        dst: str,
        level: int = 2,
        filename: str = None,
    ):
        """Add an outlet directed to a file.

        Parameters
        ----------
        dst : str
            The destination of the file, i.e. the path.
        level : int, optional
            Logging level.
        filename : str, optional
            The name of the file, also the identifier for the stream handler.
        """
        self._handlers.append(FileHandler(dst=dst, level=level, name=filename))

    @property
    def level(self):
        """Return the current logging level."""
        return self._level

    @level.setter
    def level(
        self,
        val: int,
    ):
        self._level = check_loglevel(val)
        for h in self._handlers:
            h.level = val

    def _direct(self, msg):
        """Log something directly."""
        raise NotImplementedError(NOT_IMPLEMENTED)

    @_handle_log
    def debug(self, msg: str):
        """Create a debug message."""
        return 1, msg

    @_handle_log
    def info(self, msg: str):
        """Create an info message."""
        return 2, msg

    @_handle_log
    def warning(self, msg: str):
        """Create a warning message."""
        return 3, msg

    @_handle_log
    def error(self, msg: str):
        """Create an error message."""
        return 4, msg

    @_handle_log
    def dead(self, msg: str):
        """Create a kernel-deceased message."""
        return 5, msg


def spawn_logger(
    name: str,
) -> Logger:
    """Spawn a logger within a hierarchy.

    Parameters
    ----------
    name : str
        The identifier of the logger.

    Returns
    -------
    Logger
        A Logger object (for logging).
    """
    return Logger(name)


def setup_default_log(
    name: str,
    level: int,
    dst: str | None = None,
) -> Logger:
    """Set up the base logger of a hierarchy.

    It's advisable to make this a single string that is not concatenated by period.
    E.g. 'fiat' is correct, 'fiat.logging' is not.

    Parameters
    ----------
    name : str
        Identifier of the logger.
    level : int
        Logging level.
    dst : str | None, optional
        The path to where the logging file will be located.

    Returns
    -------
    Logger
        A Logger object (for logging, no really..)
    """
    if len(name.split(".")) > 1:
        raise ValueError("Only root names (without a period) are allowed.")

    obj = Logger(name, level=level)

    obj.add_handler(level=level)
    if dst is not None:
        obj.add_file_handler(
            dst,
            level=level,
            filename=name,
        )

    return obj


def setup_mp_log(
    queue: object,
    name: str,
    level: int,
    dst: str = None,
):
    """Set up logging for multiprocessing.

    This essentially is a pipe back to the main Python process.

    Parameters
    ----------
    queue : queue.Queue
        A queue where the messages will be put in.
        N.B. this must be a multiprocessing queue, a normal queue.Queue \
will not suffice.
    name : str
        Identifier of the logger.
    level : int
        Logging level.
    dst : str, optional
        Destination of the logging. I.e. the path to the logging file.

    Returns
    -------
    Receiver
        A receiver object. This is the receiver of the pipeline.
    """
    obj = Receiver(queue)
    h = FileHandler(level=level, dst=dst, name=name)
    h.set_formatter(MessageFormatter("{asctime:20s}{message}"))
    obj.add_handler(h)
    return obj
