"""
财务分析模块
对 Tesla 的财务数据进行分析和计算
"""
from typing import Dict, List, Tuple
import json
from datetime import datetime
from src.locales.i18n import I18n, get_metric_names


class FinancialAnalyzer:
    """财务分析器"""

    def __init__(self, data_file: str = None, language: str = "zh_CN"):
        """
        初始化财务分析器

        Args:
            data_file: 财务数据文件路径
            language: 语言代码 (zh_CN 或 en_US)
        """
        self.data = None
        self.language = language
        self.i18n = I18n(language)
        if data_file:
            self.load_data(data_file)

    def load_data(self, data_file: str):
        """加载财务数据"""
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_metric_trend(self, metric_name: str) -> List[Dict]:
        """
        获取某个指标的趋势数据

        Args:
            metric_name: 指标名称

        Returns:
            包含时间序列数据的列表
        """
        if not self.data or metric_name not in self.data:
            return []

        metric_data = self.data[metric_name]

        # 提取值和日期
        trend = []
        for point in metric_data:
            trend.append({
                "date": point.get("end", ""),
                "value": point.get("val", 0),
                "period": point.get("fp", ""),
                "form": point.get("form", "")
            })

        return sorted(trend, key=lambda x: x["date"])

    def calculate_growth_rate(self, metric_name: str) -> List[Dict]:
        """
        计算同比增长率

        Args:
            metric_name: 指标名称

        Returns:
            包含增长率数据的列表
        """
        trend = self.get_metric_trend(metric_name)

        if len(trend) < 2:
            return []

        growth_rates = []
        for i in range(len(trend) - 4):  # 同比需要至少4个季度的数据
            current = trend[i + 4]
            previous = trend[i]

            if previous["value"] != 0:
                growth_rate = ((current["value"] - previous["value"]) / abs(previous["value"])) * 100
                growth_rates.append({
                    "date": current["date"],
                    "period": current["period"],
                    "current_value": current["value"],
                    "previous_value": previous["value"],
                    "growth_rate": round(growth_rate, 2)
                })

        return growth_rates

    def calculate_profit_margins(self) -> List[Dict]:
        """
        计算利润率指标

        Returns:
            包含利润率数据的列表
        """
        # 使用当前语言的指标名称
        metric_names = get_metric_names(self.language)

        revenue_trend = self.get_metric_trend(metric_names["Revenues"])
        gross_profit_trend = self.get_metric_trend(metric_names["GrossProfit"])
        operating_profit_trend = self.get_metric_trend(metric_names["OperatingIncomeLoss"])
        net_profit_trend = self.get_metric_trend(metric_names["NetIncomeLoss"])

        margins = []

        for i in range(min(len(revenue_trend), len(gross_profit_trend),
                          len(operating_profit_trend), len(net_profit_trend))):

            revenue = revenue_trend[i]["value"]
            if revenue == 0:
                continue

            margin_data = {
                "date": revenue_trend[i]["date"],
                "period": revenue_trend[i]["period"],
                "revenue": revenue,
                "gross_margin": round((gross_profit_trend[i]["value"] / revenue) * 100, 2),
                "operating_margin": round((operating_profit_trend[i]["value"] / revenue) * 100, 2),
                "net_margin": round((net_profit_trend[i]["value"] / revenue) * 100, 2)
            }

            margins.append(margin_data)

        return margins

    def calculate_financial_ratios(self) -> List[Dict]:
        """
        计算财务比率

        Returns:
            包含财务比率的列表
        """
        # 使用当前语言的指标名称
        metric_names = get_metric_names(self.language)

        assets_trend = self.get_metric_trend(metric_names["Assets"])
        liabilities_trend = self.get_metric_trend(metric_names["Liabilities"])
        equity_trend = self.get_metric_trend(metric_names["StockholdersEquity"])

        ratios = []

        for i in range(min(len(assets_trend), len(liabilities_trend), len(equity_trend))):
            assets = assets_trend[i]["value"]
            liabilities = liabilities_trend[i]["value"]
            equity = equity_trend[i]["value"]

            if assets == 0:
                continue

            ratio_data = {
                "date": assets_trend[i]["date"],
                "period": assets_trend[i]["period"],
                "assets": assets,
                "liabilities": liabilities,
                "equity": equity,
                "debt_to_asset_ratio": round((liabilities / assets) * 100, 2),
                "equity_ratio": round((equity / assets) * 100, 2),
                "debt_to_equity_ratio": round((liabilities / equity) * 100, 2) if equity != 0 else 0
            }

            ratios.append(ratio_data)

        return ratios

    def get_latest_quarter_summary(self) -> Dict:
        """
        获取最新季度的财务摘要

        Returns:
            最新季度的财务摘要
        """
        if not self.data:
            return {}

        summary = {}

        # 使用当前语言的指标名称
        metric_names = get_metric_names(self.language)

        # 获取各指标的最新值
        metrics_to_fetch = [
            "Revenues", "GrossProfit", "OperatingIncomeLoss", "NetIncomeLoss",
            "Assets", "Liabilities", "StockholdersEquity", "EarningsPerShareBasic"
        ]

        for metric_key in metrics_to_fetch:
            metric_name = metric_names.get(metric_key)
            if metric_name:
                trend = self.get_metric_trend(metric_name)
                if trend:
                    latest = trend[-1]
                    summary[metric_name] = {
                        "value": latest["value"],
                        "date": latest["date"],
                        "period": latest["period"]
                    }

        # 计算最新的利润率
        margins = self.calculate_profit_margins()
        if margins:
            # 使用多语言的 key
            margin_key = self.i18n.t("net_margin") if self.language == "zh_CN" else "Profit Margin"
            summary[margin_key] = margins[-1]

        # 计算最新的财务比率
        ratios = self.calculate_financial_ratios()
        if ratios:
            # 使用多语言的 key
            ratio_key = self.i18n.t("latest_financial_ratios") if self.language == "zh_CN" else "Financial Ratios"
            summary[ratio_key] = ratios[-1]

        return summary

    def format_currency(self, value: float) -> str:
        """
        格式化货币显示

        Args:
            value: 数值

        Returns:
            格式化后的字符串
        """
        if abs(value) >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"
        elif abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"
        else:
            return f"${value:,.2f}"


if __name__ == "__main__":
    # 测试代码
    analyzer = FinancialAnalyzer("static/data/tesla_financials.json")

    print("最新季度财务摘要:")
    summary = analyzer.get_latest_quarter_summary()
    for key, value in summary.items():
        print(f"\n{key}:")
        print(f"  {value}")

    print("\n营业收入增长率:")
    growth = analyzer.calculate_growth_rate("营业收入")
    for g in growth[-4:]:
        print(f"  {g['date']} ({g['period']}): {g['growth_rate']}%")

    print("\n利润率分析:")
    margins = analyzer.calculate_profit_margins()
    for m in margins[-4:]:
        print(f"  {m['date']} ({m['period']}):")
        print(f"    毛利率: {m['gross_margin']}%")
        print(f"    营业利润率: {m['operating_margin']}%")
        print(f"    净利率: {m['net_margin']}%")
