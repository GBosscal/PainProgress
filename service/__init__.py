from sanic import Sanic, Blueprint
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
    # 修改docs的配置
    app.config.OAS_URL_PREFIX = "/v1/pain/docs"
    # 注册路由
    from view.user import user_blueprint
    from view.feedback import feedback_blueprint
    from view.storage import storage_blueprint
    from view.pain_data import pain_blueprint
    from view.hospital import hospital_blueprint
    from view.login import login_blueprint
    from view.pain_data import pain_with_image_blueprint

    all_blueprint = Blueprint.group(
        user_blueprint, feedback_blueprint,
        storage_blueprint, login_blueprint, hospital_blueprint,
        url_prefix="/pain"
    )
    app.blueprint(all_blueprint)
    # app.blueprint(user_blueprint)
    # app.blueprint(feedback_blueprint)
    # app.blueprint(storage_blueprint)
    app.blueprint(pain_blueprint)
    # app.blueprint(hospital_blueprint)
    # app.blueprint(login_blueprint)
    app.blueprint(pain_with_image_blueprint)

    # 修改apidoc的定义
    app.ext.openapi.describe(
        "疼痛分析系统的后端服务",
        version="1.0.0",
        description=(
            """
            # 疼痛分析系统
            """
        )
    )

    return app
