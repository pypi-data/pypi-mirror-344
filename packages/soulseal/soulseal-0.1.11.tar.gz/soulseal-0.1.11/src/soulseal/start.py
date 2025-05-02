from voidring import IndexedRocksDB
from .tokens import TokenSDK
from .users import UsersManager
from .endpoints import create_auth_endpoints
from .__version__ import __version__

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

def mount_auth_api(app: FastAPI, prefix: str, token_sdk: TokenSDK, users_manager: UsersManager):
    # 用户管理和认证路由
    auth_handlers = create_auth_endpoints(
        app=app,
        token_sdk=token_sdk,
        users_manager=users_manager,
        prefix=prefix
    )
    for (method, path, handler) in auth_handlers:
        app.add_api_route(
            path=path,
            endpoint=handler,
            methods=[method],
            response_model=getattr(handler, "__annotations__", {}).get("return"),
            summary=getattr(handler, "__doc__", "").split("\n")[0] if handler.__doc__ else None,
            description=getattr(handler, "__doc__", None),
            tags=["Illufly Backend - Auth"])

def create_app(
    db_path: str,
    title: str,
    description: str,
    cors_origins: list[str],
    static_dir: str,
    prefix: str = ""
):
    """启动soulseal
    
    Args:
        db_path: 数据库路径
        title: API标题
        description: API描述
        cors_origins: CORS允许的源
        static_dir: 静态文件目录
        prefix: API路由前缀
    """
    # 创建 FastAPI 应用实例
    version = __version__
    app = FastAPI(
        title=title,
        description=description,
        version=version
    )

    # 配置 CORS
    origins = cors_origins or [
        # Next.js 开发服务器默认端口
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 不再使用 ["*"]
        allow_credentials=True,  # 允许携带凭证
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Set-Cookie"]  # 暴露 Set-Cookie 头
    )

    # 初始化数据库
    db_path = Path(db_path)
    db_path.mkdir(parents=True, exist_ok=True)  # 创建db目录本身，而不仅是父目录
    db = IndexedRocksDB(str(db_path))

    # 创建令牌管理器，传入黑名单和JWT配置
    token_sdk = TokenSDK(db=db)    
    users_manager = UsersManager(db)
    
    # 在挂载API时同样传递黑名单
    mount_auth_api(app, prefix, token_sdk, users_manager)

    return app
