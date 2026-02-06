"""
AI 财务分析模块
使用 OpenAI API 对财务数据进行智能分析
"""
import json
from typing import Dict, List, Optional
from openai import OpenAI
import os


class AIFinancialAnalyst:
    """AI 财务分析师"""

    def __init__(self, api_key: Optional[str] = None, language: str = "zh_CN"):
        """
        初始化 AI 分析器

        Args:
            api_key: OpenAI API 密钥，如果不提供则从环境变量获取
            language: 语言代码 (zh_CN 或 en_US)
        """
        self.language = language
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it as parameter.")

        # 获取自定义 API 基础 URL（如果有）
        api_base = os.getenv("OPENAI_API_BASE")

        # 初始化 OpenAI 客户端
        if api_base:
            self.client = OpenAI(api_key=self.api_key, base_url=api_base)
        else:
            self.client = OpenAI(api_key=self.api_key)

        self.model = "claude-sonnet-4-5"

    def _prepare_financial_data(self, summary: Dict, margins: List[Dict],
                                ratios: List[Dict], growth: List[Dict]) -> str:
        """
        准备财务数据用于 AI 分析

        Args:
            summary: 最新季度摘要
            margins: 利润率数据
            ratios: 财务比率数据
            growth: 增长率数据

        Returns:
            格式化的财务数据文本
        """
        data_text = "# Tesla Financial Data Analysis\n\n"

        # 最新季度摘要
        data_text += "## Latest Quarter Summary\n"
        for key, value in summary.items():
            if isinstance(value, dict) and 'value' in value:
                data_text += f"- {key}: ${value['value']:,.0f} ({value.get('period', 'N/A')})\n"
        data_text += "\n"

        # 利润率趋势（最近4个季度）
        if margins:
            data_text += "## Profit Margins Trend (Recent 4 Quarters)\n"
            for margin in margins[-4:]:
                data_text += f"- {margin['date']} ({margin['period']}): "
                data_text += f"Gross Margin={margin['gross_margin']}%, "
                data_text += f"Operating Margin={margin['operating_margin']}%, "
                data_text += f"Net Margin={margin['net_margin']}%\n"
            data_text += "\n"

        # 财务比率（最近4个季度）
        if ratios:
            data_text += "## Financial Ratios (Recent 4 Quarters)\n"
            for ratio in ratios[-4:]:
                data_text += f"- {ratio['date']} ({ratio['period']}): "
                data_text += f"Debt-to-Asset={ratio['debt_to_asset_ratio']}%, "
                data_text += f"Equity Ratio={ratio['equity_ratio']}%\n"
            data_text += "\n"

        # 增长率（最近4个季度）
        if growth:
            data_text += "## Revenue Growth Rate (Recent 4 Quarters)\n"
            for g in growth[-4:]:
                data_text += f"- {g['date']} ({g['period']}): {g['growth_rate']}% YoY\n"
            data_text += "\n"

        return data_text

    def analyze_financial_health(self, summary: Dict, margins: List[Dict],
                                 ratios: List[Dict], growth: List[Dict]) -> str:
        """
        分析公司财务健康状况

        Args:
            summary: 最新季度摘要
            margins: 利润率数据
            ratios: 财务比率数据
            growth: 增长率数据

        Returns:
            AI 生成的分析报告
        """
        financial_data = self._prepare_financial_data(summary, margins, ratios, growth)

        system_prompt = """You are an expert financial analyst specializing in analyzing company financial statements.
Your task is to analyze the provided financial data and give professional insights."""

        if self.language == "zh_CN":
            user_prompt = f"""请分析以下 Tesla 的财务数据，并提供专业的财务健康状况评估：

{financial_data}

请从以下几个方面进行分析：
1. **盈利能力分析**：分析利润率趋势，评估盈利能力的变化
2. **财务结构分析**：评估资产负债结构的健康程度
3. **增长性分析**：分析营业收入增长趋势及其可持续性
4. **风险评估**：识别潜在的财务风险
5. **综合评价**：给出整体财务健康状况评级（优秀/良好/一般/较差）

请用中文回答，条理清晰，观点专业。"""
        else:
            user_prompt = f"""Please analyze the following Tesla financial data and provide a professional financial health assessment:

{financial_data}

Please analyze from the following aspects:
1. **Profitability Analysis**: Analyze profit margin trends and assess changes in profitability
2. **Financial Structure Analysis**: Evaluate the health of asset-liability structure
3. **Growth Analysis**: Analyze revenue growth trends and sustainability
4. **Risk Assessment**: Identify potential financial risks
5. **Overall Rating**: Provide an overall financial health rating (Excellent/Good/Fair/Poor)

Please respond in English with clear structure and professional insights."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000  # 增加 token 限制以支持更长的响应
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating analysis: {str(e)}"

    def generate_investment_advice(self, summary: Dict, margins: List[Dict],
                                   ratios: List[Dict], growth: List[Dict]) -> str:
        """
        生成投资建议

        Args:
            summary: 最新季度摘要
            margins: 利润率数据
            ratios: 财务比率数据
            growth: 增长率数据

        Returns:
            AI 生成的投资建议
        """
        financial_data = self._prepare_financial_data(summary, margins, ratios, growth)

        system_prompt = """You are an experienced investment advisor. Based on financial data analysis,
provide investment recommendations. Remember to include risk warnings and disclaimers."""

        if self.language == "zh_CN":
            user_prompt = f"""基于以下 Tesla 的财务数据，请提供投资建议：

{financial_data}

请提供：
1. **投资价值分析**：从财务角度评估投资价值
2. **关键指标解读**：解读最重要的财务指标
3. **投资建议**：建议买入/持有/卖出，并说明理由
4. **风险提示**：列出投资风险

**免责声明**：请在最后加上投资风险提示。

请用中文回答，专业且客观。"""
        else:
            user_prompt = f"""Based on the following Tesla financial data, please provide investment advice:

{financial_data}

Please provide:
1. **Investment Value Analysis**: Evaluate investment value from a financial perspective
2. **Key Metrics Interpretation**: Interpret the most important financial metrics
3. **Investment Recommendation**: Recommend buy/hold/sell with rationale
4. **Risk Warning**: List investment risks

**Disclaimer**: Please include investment risk disclaimer at the end.

Please respond in English professionally and objectively."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000  # 增加 token 限制以支持更长的响应
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating investment advice: {str(e)}"

    def answer_question(self, question: str, financial_data: str) -> str:
        """
        回答关于财务数据的问题

        Args:
            question: 用户问题
            financial_data: 财务数据文本

        Returns:
            AI 生成的答案
        """
        system_prompt = """You are a financial analyst assistant. Answer questions about the financial data
based on the provided information. Be professional, accurate, and concise."""

        if self.language == "zh_CN":
            prompt = f"""基于以下财务数据：

{financial_data}

用户问题：{question}

请用中文专业地回答这个问题。"""
        else:
            prompt = f"""Based on the following financial data:

{financial_data}

User question: {question}

Please answer this question professionally in English."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000  # 增加 token 限制
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error answering question: {str(e)}"


if __name__ == "__main__":
    # 测试代码
    print("AI 财务分析模块测试")
    print("=" * 60)
    print("请设置 OPENAI_API_KEY 环境变量后运行 Web 应用查看完整功能")
    print("=" * 60)
