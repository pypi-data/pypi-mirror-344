vplog 是一个轻量级 Python 库，导入后自动将所有 print() 调用的内容：

输出至终端（保留原有行为）

写入带时间戳的日志文件，文件名格式为 logs/log_YYYYMMDD_HHMMSS.log

无需额外初始化，只需在脚本开头 import vplog 即可。

特性

零配置：导入即生效，无需额外初始化

线程/进程安全：基于 loguru 的 enqueue=True

日志文件自动管理：按启动时刻生成独立日志

兼容性：支持 Python 3.8+

安装

pip install vplog

快速开始

import vplog        # 导入即自动重定向 print

print("Hello, vplog!")
# 终端输出: Hello, vplog!
# 同时写入 logs/log_20250502_153045.log，内容：
# 2025-05-02 15:30:45 | Hello, vplog!

配置

日志目录：默认在当前工作目录下的 logs/ 子目录

修改位置：如需定制，可在源码 __init__.py 中修改 _log_root 路径

