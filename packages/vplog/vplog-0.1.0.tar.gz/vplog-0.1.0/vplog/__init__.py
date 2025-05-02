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
def _print_and_log(*args, **kw):
    _builtin_print(*args, **kw)
    logger.info(" ".join(str(a) for a in args))

builtins.print = _print_and_log

__all__ = []   # 无需向用户暴露对象