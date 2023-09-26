from sanic import Sanic
from textwrap import dedent


def create_app():
    """
    创建APP例子，并且初始化APP
    :return: APP的实例
    """
    # 创建一个新的sanic应用
    app = Sanic("backend-for-pain-system")
    # 应用的健康检查配置
    app.config.HEALTH = True
    # 注册路由
    from view.user import user_blueprint
    from view.feedback import feedback_blueprint
    from view.storage import storage_blueprint
    from view.pain_data import pain_blueprint
    from view.hospital import hospital_blueprint

    app.blueprint(user_blueprint)
    app.blueprint(feedback_blueprint)
    app.blueprint(storage_blueprint)
    app.blueprint(pain_blueprint)
    app.blueprint(hospital_blueprint)

    # 修改apidoc的定义
    app.ext.openapi.describe(
        "疼痛分析系统的后端服务",
        version="0.0.1",
        description=(
            """
            # 疼痛分析系统
            """
        )
    )

    return app
