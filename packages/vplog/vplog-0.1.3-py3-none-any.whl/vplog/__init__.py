"""
vplog - 使用 loguru 实现对 print() 的增强，使打印内容既输出到终端又写入日志文件。
导入本模块后，将全局替换 print 函数，自动记录所有打印输出。
"""
import builtins
import sys
from loguru import logger
import threading

# 保存原始的 print 函数，供内部调用终端输出
_original_print = builtins.print

# 移除 loguru 默认的处理器（避免重复输出到控制台）
logger.remove()

# 添加日志文件记录（异步、线程安全写入），级别为 INFO，使用默认格式（含时间戳、级别等）
_log_file_path = "vplog.log"
logger.add(_log_file_path, level="INFO", enqueue=True, encoding="utf-8")

# 锁用于保证多线程下控制台输出的原子性，避免交错混乱
_console_lock = threading.Lock()

def new_print(*objects, sep=' ', end='\n', file=None, flush=False):
    """
    替换内置的 print() 实现，输出内容同时打印到终端和写入日志文件。
    支持常见参数 sep, end, flush，行为与原始 print 相同。
    """
    # 确定输出目标文件，默认为标准输出
    target = file if file is not None else sys.stdout

    # 如果输出定向到非终端的自定义文件，直接调用原始 print，并跳过日志记录
    if target not in (sys.stdout, sys.stderr):
        with _console_lock:
            _original_print(*objects, sep=sep, end=end, file=file, flush=flush)
        return

    # 将所有对象转换为字符串，模拟原始 print 的拼接行为
    if objects:
        try:
            # 首选使用 str() 转换
            message = sep.join(str(obj) for obj in objects)
        except Exception:
            try:
                # 若对象的 __str__ 失败，退而使用 repr()
                message = sep.join(repr(obj) for obj in objects)
            except Exception:
                # 万一仍失败，用对象类型名称标记不可打印内容
                message = sep.join(f"<Unprintable {type(obj).__name__}>" for obj in objects)
    else:
        # 无对象时，message 为空字符串（仅用于打印换行）
        message = ""

    # 如输出字符串超过阈值，进行截断并加标记
    max_length = 2000
    if len(message) > max_length:
        message_to_log = message[:max_length] + "[已截断]"
    else:
        message_to_log = message

    # 写入日志文件（INFO 级别），使用占位符以原样记录特殊符号内容
    try:
        logger.opt(depth=1).info("{}", message_to_log)
    except Exception as log_exc:
        # 若日志记录异常，记录错误信息和原始消息（确保不丢失内容）
        logger.opt(depth=1).info("[Logging Error: {}] {}", log_exc, message_to_log)

    # 输出到终端（stdout/stderr），保持与原始 print 行为一致
    with _console_lock:
        _original_print(*objects, sep=sep, end=end, file=file, flush=flush)

# 全局替换 print 函数为 new_print
builtins.print = new_print
