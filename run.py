"""
快速启动脚本
一键启动 Tesla 财务分析系统
"""
import subprocess
import sys
import os


def check_dependencies():
    """检查依赖是否安装"""
    try:
        import streamlit
        import plotly
        import requests
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("\n请运行以下命令安装依赖:")
        print("  uv sync")
        print("或")
        print("  pip install -e .")
        return False


def fetch_data():
    """获取财务数据"""
    print("\n正在获取 Tesla 财务数据...")
    try:
        from src.data.sec_fetcher import SECFetcher

        fetcher = SECFetcher()
        facts = fetcher.get_company_facts()
        metrics = fetcher.extract_financial_metrics(facts)

        os.makedirs("static/data", exist_ok=True)
        fetcher.save_data(metrics, "static/data/tesla_financials.json")

        print("✓ 数据获取成功!")
        return True
    except Exception as e:
        print(f"✗ 数据获取失败: {e}")
        return False


def start_web_app():
    """启动 Web 应用"""
    print("\n正在启动 Web 应用...")
    print("请在浏览器中打开: http://localhost:8501")
    print("\n按 Ctrl+C 停止服务器\n")

    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "src/web/app.py",
        "--server.headless", "true"
    ])


def main():
    print("=" * 50)
    print("Tesla 财务月报分析系统")
    print("=" * 50)

    # 检查依赖
    if not check_dependencies():
        return

    # 询问是否获取新数据
    data_file = "static/data/tesla_financials.json"
    if os.path.exists(data_file):
        print(f"\n发现已有数据文件: {data_file}")
        response = input("是否重新获取数据? (y/N): ").strip().lower()
        if response == 'y':
            fetch_data()
    else:
        fetch_data()

    # 启动 Web 应用
    start_web_app()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已停止")
    except Exception as e:
        print(f"\n错误: {e}")
