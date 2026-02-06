# AI 智能分析功能使用指南

## 功能概述

Tesla 财务分析系统现已集成 OpenAI GPT-4 模型，提供智能财务分析功能：

### 主要功能

1. **📊 财务健康分析**
   - 盈利能力分析
   - 财务结构评估
   - 增长性分析
   - 风险评估
   - 综合评级

2. **💡 投资建议**
   - 投资价值分析
   - 关键指标解读
   - 买入/持有/卖出建议
   - 风险提示

3. **💬 问答助手**
   - 自由提问财务相关问题
   - 基于实际数据回答
   - 专业且客观的分析

## 配置步骤

### 1. 获取 OpenAI API Key

访问 [OpenAI Platform](https://platform.openai.com/api-keys) 获取 API Key

### 2. 配置环境变量

**方法一：使用 .env 文件（推荐）**

1. 复制示例配置文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 API Key：
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**方法二：设置系统环境变量**

Windows:
```bash
set OPENAI_API_KEY=sk-your-actual-api-key-here
```

Linux/Mac:
```bash
export OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. 安装依赖

```bash
uv sync
# 或
pip install openai python-dotenv
```

### 4. 启动应用

```bash
streamlit run src/web/app.py
```

## 使用方法

### 财务健康分析

1. 在主界面找到 "🤖 AI 智能分析" 展开面板
2. 点击 "📊 财务健康分析" 按钮
3. 等待 AI 分析完成（通常需要 5-10 秒）
4. 查看详细的分析报告

**分析内容包括：**
- 盈利能力趋势分析
- 资产负债结构健康度
- 营业收入增长可持续性
- 潜在财务风险识别
- 整体财务健康评级

### 投资建议

1. 点击 "💡 投资建议" 按钮
2. 等待 AI 生成建议
3. 查看投资价值分析和建议

**建议内容包括：**
- 从财务角度的投资价值评估
- 关键财务指标解读
- 明确的投资建议（买入/持有/卖出）
- 投资风险警示
- 免责声明

### 问答助手

1. 在文本框中输入你的问题
2. 点击 "🔍 获取答案" 按钮
3. 查看 AI 的专业回答

**示例问题：**
- Tesla 的盈利能力如何？
- 最近几个季度的利润率趋势是什么？
- Tesla 的财务风险主要在哪些方面？
- 与去年同期相比，营业收入增长如何？

## 技术细节

### 使用的模型

- **模型**: GPT-4o-mini
- **优势**: 成本低、速度快、质量高
- **适用场景**: 财务数据分析、投资建议生成

### API 调用参数

```python
{
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 2000
}
```

### 数据准备

AI 分析基于以下数据：
- 最新季度财务摘要
- 最近 4 个季度的利润率趋势
- 最近 4 个季度的财务比率
- 最近 4 个季度的增长率

### 多语言支持

AI 分析完全支持中英文：
- 简体中文：使用中文提示词，返回中文分析
- English：使用英文提示词，返回英文分析

## 成本估算

基于 GPT-4o-mini 的定价（2026年1月）：

- **输入**: $0.150 / 1M tokens
- **输出**: $0.600 / 1M tokens

**单次分析成本估算：**
- 财务健康分析: ~$0.01-0.02
- 投资建议: ~$0.01-0.02
- 问答助手: ~$0.005-0.01

**月度使用成本估算：**
- 轻度使用（10次/天）: ~$3-6/月
- 中度使用（30次/天）: ~$9-18/月
- 重度使用（100次/天）: ~$30-60/月

## 注意事项

### 免责声明

⚠️ **重要提示**：
1. AI 生成的分析和建议仅供参考，不构成投资建议
2. 投资决策应基于多方面信息和专业咨询
3. 财务市场存在风险，投资需谨慎
4. 本系统不对投资损失承担任何责任

### 数据准确性

- AI 分析基于 SEC EDGAR 的公开数据
- 数据可能存在延迟
- 建议定期刷新数据以获取最新信息

### API 使用限制

- OpenAI API 有速率限制
- 建议合理使用，避免频繁调用
- 如遇到速率限制错误，请稍后重试

### 隐私和安全

- API Key 存储在本地 `.env` 文件中
- 不要将 `.env` 文件提交到版本控制系统
- 不要分享你的 API Key

## 故障排除

### 问题：提示 "OpenAI API key is required"

**解决方案：**
1. 确认已创建 `.env` 文件
2. 检查 API Key 是否正确填写
3. 重启应用以加载环境变量

### 问题：API 调用失败

**可能原因：**
1. API Key 无效或过期
2. 账户余额不足
3. 网络连接问题
4. 超过速率限制

**解决方案：**
1. 检查 API Key 是否有效
2. 登录 OpenAI 平台查看账户状态
3. 检查网络连接
4. 等待一段时间后重试

### 问题：分析结果不准确

**建议：**
1. 确保财务数据是最新的（点击刷新数据）
2. 尝试重新生成分析
3. 使用问答助手针对性提问

## 代码示例

### 直接使用 AI 分析模块

```python
from src.analysis.ai_analyst import AIFinancialAnalyst
from src.analysis.financial_analyzer import FinancialAnalyzer

# 初始化分析器
analyzer = FinancialAnalyzer("data.json", language="zh_CN")
ai_analyst = AIFinancialAnalyst(language="zh_CN")

# 获取数据
summary = analyzer.get_latest_quarter_summary()
margins = analyzer.calculate_profit_margins()
ratios = analyzer.calculate_financial_ratios()
growth = analyzer.calculate_growth_rate("营业收入")

# 生成分析
health_analysis = ai_analyst.analyze_financial_health(
    summary, margins, ratios, growth
)
print(health_analysis)

# 生成投资建议
investment_advice = ai_analyst.generate_investment_advice(
    summary, margins, ratios, growth
)
print(investment_advice)

# 问答
financial_data = ai_analyst._prepare_financial_data(
    summary, margins, ratios, growth
)
answer = ai_analyst.answer_question(
    "Tesla 的盈利能力如何？",
    financial_data
)
print(answer)
```

## 未来计划

- [ ] 支持更多 AI 模型（Claude, Gemini 等）
- [ ] 添加历史分析对比功能
- [ ] 支持自定义分析模板
- [ ] 添加分析报告导出功能
- [ ] 支持批量分析多家公司

## 反馈和支持

如有问题或建议，请在 GitHub Issues 中反馈。
