"""
国际化 (i18n) 模块
支持简体中文和英语
"""

# 语言配置
LANGUAGES = {
    "zh_CN": "简体中文",
    "en_US": "English"
}

# 翻译字典
TRANSLATIONS = {
    "zh_CN": {
        # 页面标题和基础信息
        "app_title": "Tesla 财务月报分析系统",
        "page_icon": "📊",
        "control_panel": "控制面板",
        "refresh_data": "🔄 刷新数据",
        "language": "语言 / Language",

        # 数据源信息
        "data_source": "数据来源",
        "data_source_value": "SEC EDGAR",
        "update_frequency": "更新频率",
        "update_frequency_value": "实时获取",
        "analysis_content": "分析内容",
        "analysis_items": [
            "营业收入趋势",
            "利润率分析",
            "财务结构分析",
            "同比增长率"
        ],

        # 财务指标
        "latest_quarter_summary": "最新季度财务摘要",
        "revenue": "营业收入",
        "net_profit": "净利润",
        "net_margin": "净利率",
        "gross_margin": "毛利率",
        "total_assets": "总资产",
        "gross_profit": "毛利润",
        "operating_profit": "营业利润",
        "total_liabilities": "总负债",
        "stockholders_equity": "股东权益",
        "cash_equivalents": "现金及现金等价物",
        "eps": "基本每股收益",
        "operating_margin": "营业利润率",

        # 标签页
        "tab_revenue": "📈 营业收入分析",
        "tab_margins": "💰 利润率分析",
        "tab_structure": "🏦 财务结构分析",
        "tab_growth": "📊 增长率分析",

        # 图表标题
        "revenue_trend_title": "Tesla 营业收入趋势",
        "profit_margins_title": "Tesla 利润率趋势",
        "financial_structure_title": "Tesla 资产负债结构",
        "growth_rate_title": "Tesla 营业收入同比增长率",

        # 坐标轴标签
        "date": "日期",
        "revenue_billion": "营业收入 (十亿美元)",
        "margin_percent": "利润率 (%)",
        "growth_rate_percent": "增长率 (%)",

        # 按钮和操作
        "view_details": "查看详细数据",
        "loading_data": "正在从 SEC 获取最新财务数据...",
        "data_load_error": "数据加载失败",

        # 财务比率
        "latest_financial_ratios": "最新财务比率",
        "debt_to_asset_ratio": "资产负债率",
        "equity_ratio": "权益比率",
        "debt_to_equity_ratio": "负债权益比",

        # 其他
        "period": "期间",
        "value": "数值",
        "no_data": "暂无数据",
        "historical_data": "查看历史数据",

        # 图表说明
        "revenue_analysis": "营业收入趋势分析",
        "margins_analysis": "利润率趋势分析",
        "structure_analysis": "财务结构分析",
        "growth_analysis": "营业收入同比增长率",
    },

    "en_US": {
        # Page title and basic info
        "app_title": "Tesla Financial Analysis System",
        "page_icon": "📊",
        "control_panel": "Control Panel",
        "refresh_data": "🔄 Refresh Data",
        "language": "Language / 语言",

        # Data source info
        "data_source": "Data Source",
        "data_source_value": "SEC EDGAR",
        "update_frequency": "Update Frequency",
        "update_frequency_value": "Real-time",
        "analysis_content": "Analysis Content",
        "analysis_items": [
            "Revenue Trends",
            "Profit Margin Analysis",
            "Financial Structure Analysis",
            "Year-over-Year Growth Rate"
        ],

        # Financial metrics
        "latest_quarter_summary": "Latest Quarter Financial Summary",
        "revenue": "Revenue",
        "net_profit": "Net Profit",
        "net_margin": "Net Margin",
        "gross_margin": "Gross Margin",
        "total_assets": "Total Assets",
        "gross_profit": "Gross Profit",
        "operating_profit": "Operating Profit",
        "total_liabilities": "Total Liabilities",
        "stockholders_equity": "Stockholders' Equity",
        "cash_equivalents": "Cash & Cash Equivalents",
        "eps": "Basic EPS",
        "operating_margin": "Operating Margin",

        # Tabs
        "tab_revenue": "📈 Revenue Analysis",
        "tab_margins": "💰 Profit Margins",
        "tab_structure": "🏦 Financial Structure",
        "tab_growth": "📊 Growth Rate",

        # Chart titles
        "revenue_trend_title": "Tesla Revenue Trend",
        "profit_margins_title": "Tesla Profit Margins Trend",
        "financial_structure_title": "Tesla Asset-Liability Structure",
        "growth_rate_title": "Tesla Revenue YoY Growth Rate",

        # Axis labels
        "date": "Date",
        "revenue_billion": "Revenue (Billion USD)",
        "margin_percent": "Margin (%)",
        "growth_rate_percent": "Growth Rate (%)",

        # Buttons and actions
        "view_details": "View Detailed Data",
        "loading_data": "Fetching latest financial data from SEC...",
        "data_load_error": "Failed to load data",

        # Financial ratios
        "latest_financial_ratios": "Latest Financial Ratios",
        "debt_to_asset_ratio": "Debt-to-Asset Ratio",
        "equity_ratio": "Equity Ratio",
        "debt_to_equity_ratio": "Debt-to-Equity Ratio",

        # Others
        "period": "Period",
        "value": "Value",
        "no_data": "No data available",
        "historical_data": "View Historical Data",

        # Chart descriptions
        "revenue_analysis": "Revenue Trend Analysis",
        "margins_analysis": "Profit Margins Trend Analysis",
        "structure_analysis": "Financial Structure Analysis",
        "growth_analysis": "Revenue Year-over-Year Growth Rate",
    }
}


class I18n:
    """国际化工具类"""

    def __init__(self, language: str = "zh_CN"):
        """
        初始化国际化工具

        Args:
            language: 语言代码 (zh_CN 或 en_US)
        """
        self.language = language if language in LANGUAGES else "zh_CN"

    def t(self, key: str, default: str = None) -> str:
        """
        获取翻译文本

        Args:
            key: 翻译键
            default: 默认值

        Returns:
            翻译后的文本
        """
        return TRANSLATIONS.get(self.language, {}).get(key, default or key)

    def set_language(self, language: str):
        """设置语言"""
        if language in LANGUAGES:
            self.language = language

    def get_language(self) -> str:
        """获取当前语言"""
        return self.language

    def get_language_name(self) -> str:
        """获取当前语言名称"""
        return LANGUAGES.get(self.language, "简体中文")

    @staticmethod
    def get_available_languages() -> dict:
        """获取所有可用语言"""
        return LANGUAGES


# 财务指标映射（用于数据分析模块）
METRIC_NAMES = {
    "zh_CN": {
        "Revenues": "营业收入",
        "GrossProfit": "毛利润",
        "OperatingIncomeLoss": "营业利润",
        "NetIncomeLoss": "净利润",
        "Assets": "总资产",
        "Liabilities": "总负债",
        "StockholdersEquity": "股东权益",
        "CashAndCashEquivalentsAtCarryingValue": "现金及现金等价物",
        "EarningsPerShareBasic": "基本每股收益",
    },
    "en_US": {
        "Revenues": "Revenue",
        "GrossProfit": "Gross Profit",
        "OperatingIncomeLoss": "Operating Profit",
        "NetIncomeLoss": "Net Profit",
        "Assets": "Total Assets",
        "Liabilities": "Total Liabilities",
        "StockholdersEquity": "Stockholders' Equity",
        "CashAndCashEquivalentsAtCarryingValue": "Cash & Cash Equivalents",
        "EarningsPerShareBasic": "Basic EPS",
    }
}


def get_metric_names(language: str = "zh_CN") -> dict:
    """
    获取财务指标名称映射

    Args:
        language: 语言代码

    Returns:
        指标名称映射字典
    """
    return METRIC_NAMES.get(language, METRIC_NAMES["zh_CN"])
