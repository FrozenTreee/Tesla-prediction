"""
测试多语言功能
用于验证所有模块在中英文环境下都能正常工作
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.locales.i18n import I18n, get_metric_names, LANGUAGES


def test_i18n():
    """测试国际化模块"""
    print("=" * 60)
    print("测试国际化模块 / Testing I18n Module")
    print("=" * 60)

    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n测试语言 / Testing Language: {lang_name} ({lang_code})")
        print("-" * 60)

        i18n = I18n(lang_code)

        # 测试基本翻译
        print(f"应用标题 / App Title: {i18n.t('app_title')}")
        print(f"控制面板 / Control Panel: {i18n.t('control_panel')}")
        print(f"数据来源 / Data Source: {i18n.t('data_source')}")

        # 测试财务指标名称
        metric_names = get_metric_names(lang_code)
        print(f"\n财务指标 / Financial Metrics:")
        for key, value in metric_names.items():
            print(f"  {key}: {value}")


def test_analyzer_initialization():
    """测试分析器初始化"""
    print("\n" + "=" * 60)
    print("测试分析器初始化 / Testing Analyzer Initialization")
    print("=" * 60)

    from src.analysis.financial_analyzer import FinancialAnalyzer

    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n语言 / Language: {lang_name} ({lang_code})")
        print("-" * 60)

        try:
            analyzer = FinancialAnalyzer(language=lang_code)
            print(f"[OK] Analyzer initialized successfully")
            print(f"  Language: {analyzer.language}")
            print(f"  I18n instance: {analyzer.i18n.get_language_name()}")
        except Exception as e:
            print(f"[ERROR] Initialization failed: {str(e)}")


def test_method_calls():
    """测试方法调用"""
    print("\n" + "=" * 60)
    print("测试方法调用 / Testing Method Calls")
    print("=" * 60)

    from src.analysis.financial_analyzer import FinancialAnalyzer

    # 检查是否有测试数据
    for lang_code, lang_name in LANGUAGES.items():
        data_file = f"static/data/tesla_financials_{lang_code}.json"

        print(f"\n语言 / Language: {lang_name} ({lang_code})")
        print(f"数据文件 / Data file: {data_file}")
        print("-" * 60)

        if not os.path.exists(data_file):
            print(f"[WARNING] Data file not found, skipping tests")
            print(f"  Please run the web app first to generate data")
            continue

        try:
            analyzer = FinancialAnalyzer(data_file, language=lang_code)

            # 测试获取指标趋势
            metric_names = get_metric_names(lang_code)
            revenue_name = metric_names["Revenues"]

            trend = analyzer.get_metric_trend(revenue_name)
            print(f"[OK] get_metric_trend('{revenue_name}'): {len(trend)} records")

            # 测试计算利润率
            margins = analyzer.calculate_profit_margins()
            print(f"[OK] calculate_profit_margins(): {len(margins)} records")

            # 测试计算财务比率
            ratios = analyzer.calculate_financial_ratios()
            print(f"[OK] calculate_financial_ratios(): {len(ratios)} records")

            # 测试获取最新季度摘要
            summary = analyzer.get_latest_quarter_summary()
            print(f"[OK] get_latest_quarter_summary(): {len(summary)} metrics")

            if summary:
                print(f"\n  Summary content:")
                for key in list(summary.keys())[:3]:  # 只显示前3个
                    print(f"    - {key}")

        except Exception as e:
            print(f"[ERROR] Test failed: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("Tesla 财务分析系统 - 多语言功能测试")
    print("Tesla Financial Analysis - Multi-language Feature Test")
    print("=" * 60)

    # 运行测试
    test_i18n()
    test_analyzer_initialization()
    test_method_calls()

    print("\n" + "=" * 60)
    print("测试完成 / Testing Complete")
    print("=" * 60)
    print("\n建议 / Recommendations:")
    print("1. 如果数据文件不存在，请运行: streamlit run src/web/app.py")
    print("   If data files don't exist, run: streamlit run src/web/app.py")
    print("2. 在 Web 界面中切换语言以生��对应的数据文件")
    print("   Switch languages in the web interface to generate data files")


if __name__ == "__main__":
    main()
