# 多语言功能使用指南 / Multi-language Feature Guide

## 问题修复总结 / Summary of Fixes

### 已修复的问题 / Fixed Issues

1. **英文版 Profit Margins 表格无法生成**
   - 问题：`calculate_profit_margins()` 方法使用硬编码的中文指标名称
   - 修复：使用 `get_metric_names(language)` 动态获取对应语言的指标名称

2. **英文版 Financial Structure 表格无法生成**
   - 问题：`calculate_financial_ratios()` 方法使用硬编码的中文指标名称
   - 修复：使用 `get_metric_names(language)` 动态获取对应语言的指标名称

3. **侧边栏 Markdown 内容未正确解析**
   - 问题：`st.info()` 不支持 Markdown 格式化
   - 修复：改用 `st.markdown()` 并使用引用块样式

4. **最新季度摘要在英文版无法显示**
   - 问题：`get_latest_quarter_summary()` 使用硬编码的中文指标名称
   - 修复：使用多语言的指标名称映射

## 如何使用多语言功能 / How to Use Multi-language Feature

### 启动应用 / Start Application

```bash
streamlit run src/web/app.py
```

### 切换语言 / Switch Language

1. 在左侧边栏找到 "语言 / Language" 选择器
2. 选择你想要的语言：
   - 简体中文 (Simplified Chinese)
   - English
3. 界面会自动刷新并显示对应语言

### 语言切换效果 / Language Switch Effects

切换语言后，以下内容会自动更新：

**简体中文**:
- 页面标题：Tesla 财务月报分析系统
- 所有菜单和按钮：控制面板、刷新数据等
- 财务指标：营业收入、毛利润、净利润等
- 图表标题和坐标轴标签
- 所有提示信息

**English**:
- Page Title: Tesla Financial Analysis System
- All menus and buttons: Control Panel, Refresh Data, etc.
- Financial Metrics: Revenue, Gross Profit, Net Profit, etc.
- Chart titles and axis labels
- All notification messages

## 技术实现 / Technical Implementation

### 1. 国际化模块 (`src/locales/i18n.py`)

```python
from src.locales.i18n import I18n, get_metric_names

# 创建 i18n 实例
i18n = I18n("zh_CN")  # or "en_US"

# 获取翻译文本
title = i18n.t("app_title")

# 获取财务指标名称
metrics = get_metric_names("zh_CN")
revenue_name = metrics["Revenues"]  # "营业收入"
```

### 2. 数据获取模块更新

```python
from src.data.sec_fetcher import SECFetcher

fetcher = SECFetcher()
facts = fetcher.get_company_facts()

# 指定语言提取数据
metrics_zh = fetcher.extract_financial_metrics(facts, "zh_CN")
metrics_en = fetcher.extract_financial_metrics(facts, "en_US")
```

### 3. 分析模块更新

```python
from src.analysis.financial_analyzer import FinancialAnalyzer

# 指定语言创建分析器
analyzer = FinancialAnalyzer("data.json", language="en_US")

# 所有方法都会使用指定语言的指标名称
margins = analyzer.calculate_profit_margins()
ratios = analyzer.calculate_financial_ratios()
summary = analyzer.get_latest_quarter_summary()
```

### 4. Web 界面集成

```python
# 使用 session state 管理语言
if 'language' not in st.session_state:
    st.session_state.language = 'zh_CN'

# 创建 i18n 实例
i18n = I18n(st.session_state.language)

# 使用翻译
st.title(i18n.t("app_title"))
st.button(i18n.t("refresh_data"))
```

## 数据文件管理 / Data File Management

### 数据文件存储位置

```
static/data/
├── tesla_financials_zh_CN.json  # 中文版数据
└── tesla_financials_en_US.json  # 英文版数据
```

### 数据文件生成

- 首次切换到某个语言时，系统会自动从 SEC 获取数据
- 数据按语言分别缓存，避免重复请求
- 点击"刷新数据"可以清除缓存并重新获取

## 添加新语言 / Adding New Languages

如需添加新语言（如日语、韩语等），只需在 `src/locales/i18n.py` 中：

1. 在 `LANGUAGES` 字典中添加语言代码和名称：
```python
LANGUAGES = {
    "zh_CN": "简体中文",
    "en_US": "English",
    "ja_JP": "日本語",  # 新增
}
```

2. 在 `TRANSLATIONS` 字典中添加翻译：
```python
TRANSLATIONS = {
    # ... existing translations ...
    "ja_JP": {
        "app_title": "Tesla財務月次分析システム",
        # ... more translations
    }
}
```

3. 在 `METRIC_NAMES` 中添加财务指标翻译：
```python
METRIC_NAMES = {
    # ... existing metrics ...
    "ja_JP": {
        "Revenues": "営業収入",
        # ... more metrics
    }
}
```

## 测试 / Testing

运行测试脚本验证多语言功能：

```bash
python test_i18n.py
```

测试内容包括：
- 国际化模块初始化
- 分析器多语言支持
- 所有分析方法在不同语言下的正确性

## 常见问题 / FAQ

### Q: 切换语言后为什么没有数据？
A: 首次切换到某个语言时，需要从 SEC 获取数据。请等待数据加载完成。

### Q: 如何强制刷新数据？
A: 点击侧边栏的"🔄 刷新数据 / 🔄 Refresh Data"按钮。

### Q: 数据文件可以共享吗？
A: 不同语言的数据文件独立存储，内容相同但指标名称不同，不建议共享。

### Q: 支持繁体中文吗？
A: 目前仅支持简体中文和英语，如需添加繁体中文，参考"添加新语言"部分。

## 更新日志 / Changelog

### v1.1.0 - 2026-01-07
- ✅ 修复英文版 profit margins 表格生成问题
- ✅ 修复英文版 financial structure 表格生成问题
- ✅ 修复侧边栏 markdown 内容解析问题
- ✅ 完善最新季度摘要的多语言支持
- ✅ 添加完整的测试脚本

### v1.0.0 - 2026-01-07
- 🎉 初始版本，支持简体中文
- 🌐 添加多语言支持（简体中文/English）
- 📊 完整的财务分析功能
- 🎨 交互式 Web 界面
