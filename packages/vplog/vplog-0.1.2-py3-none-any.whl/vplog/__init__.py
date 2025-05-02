"""
plog 0.1
导入即自动把所有 print 同步写入 logs/log_YYYYMMDD_HHMMSS.log
依赖: loguru>=0.7
"""

from loguru import logger
import builtins, datetime as _dt, pathlib as _pl

_log_root = _pl.Path.cwd() / "logs"          # 用户主目录下，避免 site-packages 只读
_log_root.mkdir(exist_ok=True)
_log_file  = _log_root / f"log_{_dt.datetime.now():%Y%m%d_%H%M%S}.log"

logger.add(
    _log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    enqueue=True,
    encoding="utf-8",
)

_builtin_print = builtins.print

def _print_and_log(*args, **kwargs):
    # 1) 保留原 print 行为
    _builtin_print(*args, **kwargs)

    # 2) 复刻与终端一致的文本（含 sep / end），但仅当有真正内容时才写日志
    sep  = kwargs.get("sep", " ")
    end  = kwargs.get("end", "\n")

    msg_body = sep.join(str(a) for a in args)
    msg_full = msg_body + ("" if end == "" else end.rstrip("\n"))

    if msg_body.strip():                      # ← 空串就不写日志
        logger.info("{}", msg_full)           # '{}' 把整行当参数，避免花括号解析



__all__ = []   # 无需向用户暴露对象