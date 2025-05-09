import time
import httpx
import sys
import winreg
import json
from pathlib import Path

# 默认配置包含仓库列表
DEFAULT_CONFIG = {
    "Github_Personal_Token": "",
    "Custom_Steam_Path": "",
    "Debug_Mode": False,
    "Logging_Files": True,
    "Help": "Github Personal Token可在GitHub设置的Developer settings中生成",
    "REPO_LIST": [
		"3circledesign/BruhHub",
		"sojorepo/sojogames",
		"sunyufan000/ManifestHub",
		"SteamAutoCracks/ManifestHub",
		"ikun0014/ManifestHub",
		"Auiowu/ManifestAutoUpdate",
		"tymolu233/ManifestAutoUpdate-fix"
    ],
}

def generate_config() -> None:
    """生成包含默认仓库列表的配置文件"""
    try:
        with open(Path("./config.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False))
        print("配置文件已生成")
    except IOError as e:
        print(f"配置文件创建失败: {str(e)}")
        sys.exit(1)

def load_config() -> dict:
    """加载并合并配置文件"""
    if not Path("./config.json").exists():
        generate_config()
        print("请填写配置文件后重新运行程序，5秒后退出")
        time.sleep(5)
        sys.exit(1)

    try:
        with open(Path("./config.json"), "r", encoding="utf-8") as f:
            user_config = json.loads(f.read())
    except json.JSONDecodeError:
        print("配置文件损坏，正在重新生成...")
        generate_config()
        sys.exit(1)
    except Exception as e:
        print(f"配置加载失败: {str(e)}")
        sys.exit(1)

    # 合并默认配置和用户配置
    config = DEFAULT_CONFIG.copy()
    config.update(user_config)
    return config

def get_steam_path(config: dict) -> Path:
    """获取Steam安装路径"""
    try:
        if custom_path := config.get("Custom_Steam_Path"):
            return Path(custom_path)

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
            return Path(winreg.QueryValueEx(key, "SteamPath")[0])
    except Exception as e:
        print(f"Steam路径获取失败: {str(e)}")
        sys.exit(1)

# 初始化配置和全局变量
CONFIG = load_config()
STEAM_PATH = get_steam_path(CONFIG)
DEBUG_MODE = CONFIG.get("Debug_Mode", False)
LOG_FILE = CONFIG.get("Logging_Files", True)
GITHUB_TOKEN = str(CONFIG.get("Github_Personal_Token", ""))
HEADER = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else None
REPO_LIST = CONFIG["REPO_LIST"]  # 从配置读取仓库列表
IS_CN = True
CLIENT = httpx.AsyncClient(verify=False)

async def main():
    """主函数示例"""
    print("当前配置的仓库列表:")
    for repo in REPO_LIST:
        print(f"- {repo}")
    
    # 这里可以添加实际的业务逻辑
    # 例如使用 CLIENT 和 HEADER 访问 GitHub API

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
