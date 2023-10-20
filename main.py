"""
@Project: BackendForPain
@File: main.py
@Auth: Bosscal
@Date: 2023/9/4
@Description:
    主启动函数。
"""

from config import Config
from service import create_app

application = create_app()

if __name__ == '__main__':
    application.run(
        host=Config.SysHost,
        port=Config.SysPort,
        workers=1
    )
