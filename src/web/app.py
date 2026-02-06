"""
Tesla 财务月报分析 - Web 展示界面
使用 Streamlit 创建交互式财务报表，支持多语言
"""
import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data.sec_fetcher import SECFetcher
from src.analysis.financial_analyzer import FinancialAnalyzer
from src.analysis.ai_analyst import AIFinancialAnalyst
from src.locales.i18n import I18n, LANGUAGES, get_metric_names


# 初始化语言设置
if 'language' not in st.session_state:
    st.session_state.language = 'zh_CN'

# 创建 i18n 实例
i18n = I18n(st.session_state.language)

# 页面配置
st.set_page_config(
    page_title=i18n.t("app_title"),
    page_icon=i18n.t("page_icon"),
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_financial_data(language: str):
    """加载财务数据（带缓存）"""
    data_file = f"static/data/tesla_financials_{language}.json"

    if not os.path.exists(data_file):
        st.info(i18n.t("loading_data"))
        fetcher = SECFetcher()
        facts = fetcher.get_company_facts()
        metrics = fetcher.extract_financial_metrics(facts, language)

        os.makedirs("static/data", exist_ok=True)
        fetcher.save_data(metrics, data_file)

    analyzer = FinancialAnalyzer(data_file, language)
    return analyzer


def format_currency(value):
    """格式化货币显示"""
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    else:
        return f"${value:,.2f}"


def plot_revenue_trend(analyzer, i18n):
    """绘制营业收入趋势图"""
    metric_name = get_metric_names(i18n.language)["Revenues"]
    trend = analyzer.get_metric_trend(metric_name)

    if not trend:
        st.warning(i18n.t("no_data"))
        return

    dates = [t["date"] for t in trend]
    values = [t["value"] / 1_000_000_000 for t in trend]  # 转换为十亿美元

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name=i18n.t("revenue"),
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=i18n.t("revenue_trend_title"),
        xaxis_title=i18n.t("date"),
        yaxis_title=i18n.t("revenue_billion"),
        hovermode='x unified',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_profit_margins(analyzer, i18n):
    """绘制利润率趋势图"""
    margins = analyzer.calculate_profit_margins()

    if not margins:
        st.warning(i18n.t("no_data"))
        return

    dates = [m["date"] for m in margins]
    gross_margins = [m["gross_margin"] for m in margins]
    operating_margins = [m["operating_margin"] for m in margins]
    net_margins = [m["net_margin"] for m in margins]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates, y=gross_margins,
        mode='lines+markers', name=i18n.t("gross_margin"),
        line=dict(color='#2ca02c', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=dates, y=operating_margins,
        mode='lines+markers', name=i18n.t("operating_margin"),
        line=dict(color='#ff7f0e', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=dates, y=net_margins,
        mode='lines+markers', name=i18n.t("net_margin"),
        line=dict(color='#d62728', width=2)
    ))

    fig.update_layout(
        title=i18n.t("profit_margins_title"),
        xaxis_title=i18n.t("date"),
        yaxis_title=i18n.t("margin_percent"),
        hovermode='x unified',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_financial_structure(analyzer, i18n):
    """绘制财务结构图"""
    ratios = analyzer.calculate_financial_ratios()

    if not ratios:
        st.warning(i18n.t("no_data"))
        return

    latest = ratios[-1]

    # 创建资产负债结构饼图
    labels = [i18n.t("stockholders_equity"), i18n.t("total_liabilities")]
    values = [latest['equity'], latest['liabilities']]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=['#2ca02c', '#d62728']
    )])

    fig.update_layout(
        title=f"{i18n.t('financial_structure_title')} ({latest['date']})",
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_growth_rate(analyzer, i18n):
    """绘制同比增长率"""
    metric_name = get_metric_names(i18n.language)["Revenues"]
    growth = analyzer.calculate_growth_rate(metric_name)

    if not growth:
        st.warning(i18n.t("no_data"))
        return

    dates = [g["date"] for g in growth]
    rates = [g["growth_rate"] for g in growth]

    # 创建颜色列表（正增长为绿色，负增长为红色）
    colors = ['#2ca02c' if r >= 0 else '#d62728' for r in rates]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dates,
        y=rates,
        marker_color=colors,
        name=i18n.t("growth_rate_percent")
    ))

    fig.update_layout(
        title=i18n.t("growth_rate_title"),
        xaxis_title=i18n.t("date"),
        yaxis_title=i18n.t("growth_rate_percent"),
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    """主函数"""

    # 标题
    st.title(i18n.t("app_title"))
    st.markdown("---")

    # 侧边栏
    with st.sidebar:
        st.header(i18n.t("control_panel"))

        # 语言选择
        st.subheader(i18n.t("language"))
        language_options = {code: name for code, name in LANGUAGES.items()}
        selected_language = st.selectbox(
            "",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(st.session_state.language),
            key="language_selector"
        )

        # 如果语言改变，更新 session state 并重新运行
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()

        st.markdown("---")

        if st.button(i18n.t("refresh_data"), use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.markdown("---")

        # 构建分析项列表
        analysis_items = "\n".join([f"- {item}" for item in i18n.t("analysis_items")])

        st.markdown(f"""
> **{i18n.t("data_source")}**: {i18n.t("data_source_value")}
>
> **{i18n.t("update_frequency")}**: {i18n.t("update_frequency_value")}
>
> **{i18n.t("analysis_content")}**:
> {analysis_items.replace(chr(10), chr(10) + '> ')}
        """)

    # 加载数据
    try:
        analyzer = load_financial_data(st.session_state.language)
    except Exception as e:
        st.error(f"{i18n.t('data_load_error')}: {str(e)}")
        return

    # 获取指标名称
    metric_names = get_metric_names(st.session_state.language)

    # 获取最新季度摘要
    summary = analyzer.get_latest_quarter_summary()

    if summary:
        st.header(i18n.t("latest_quarter_summary"))

        # 显示关键指标
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if metric_names["Revenues"] in summary:
                revenue = summary[metric_names["Revenues"]]["value"]
                st.metric(
                    i18n.t("revenue"),
                    format_currency(revenue),
                    delta=summary[metric_names["Revenues"]]["period"]
                )

        with col2:
            if metric_names["NetIncomeLoss"] in summary:
                net_profit = summary[metric_names["NetIncomeLoss"]]["value"]
                st.metric(
                    i18n.t("net_profit"),
                    format_currency(net_profit),
                    delta=summary[metric_names["NetIncomeLoss"]]["period"]
                )

        with col3:
            profit_ratio_key = i18n.t("net_margin") if st.session_state.language == "zh_CN" else "Profit Margin"
            if profit_ratio_key in summary or "利润率" in summary:
                margin_data = summary.get(profit_ratio_key, summary.get("利润率", {}))
                net_margin = margin_data.get("net_margin", 0)
                gross_margin = margin_data.get("gross_margin", 0)
                st.metric(
                    i18n.t("net_margin"),
                    f"{net_margin}%",
                    delta=f"{i18n.t('gross_margin')} {gross_margin}%"
                )

        with col4:
            if metric_names["Assets"] in summary:
                assets = summary[metric_names["Assets"]]["value"]
                st.metric(
                    i18n.t("total_assets"),
                    format_currency(assets),
                    delta=summary[metric_names["Assets"]]["period"]
                )

        st.markdown("---")

    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        i18n.t("tab_revenue"),
        i18n.t("tab_margins"),
        i18n.t("tab_structure"),
        i18n.t("tab_growth")
    ])

    with tab1:
        st.subheader(i18n.t("revenue_analysis"))
        plot_revenue_trend(analyzer, i18n)

        with st.expander(i18n.t("view_details")):
            trend = analyzer.get_metric_trend(metric_names["Revenues"])
            if trend:
                st.dataframe(trend, use_container_width=True)

    with tab2:
        st.subheader(i18n.t("margins_analysis"))
        plot_profit_margins(analyzer, i18n)

        with st.expander(i18n.t("view_details")):
            margins = analyzer.calculate_profit_margins()
            if margins:
                st.dataframe(margins, use_container_width=True)

    with tab3:
        st.subheader(i18n.t("structure_analysis"))

        col1, col2 = st.columns(2)

        with col1:
            plot_financial_structure(analyzer, i18n)

        with col2:
            ratios = analyzer.calculate_financial_ratios()
            if ratios:
                latest_ratio = ratios[-1]
                st.markdown(f"### {i18n.t('latest_financial_ratios')}")
                st.metric(i18n.t("debt_to_asset_ratio"), f"{latest_ratio['debt_to_asset_ratio']}%")
                st.metric(i18n.t("equity_ratio"), f"{latest_ratio['equity_ratio']}%")
                st.metric(i18n.t("debt_to_equity_ratio"), f"{latest_ratio['debt_to_equity_ratio']}%")

        with st.expander(i18n.t("historical_data")):
            if ratios:
                st.dataframe(ratios, use_container_width=True)

    with tab4:
        st.subheader(i18n.t("growth_analysis"))
        plot_growth_rate(analyzer, i18n)

        with st.expander(i18n.t("view_details")):
            growth = analyzer.calculate_growth_rate(metric_names["Revenues"])
            if growth:
                st.dataframe(growth, use_container_width=True)

    # 添加 AI 分析标签页
    if os.getenv("OPENAI_API_KEY"):
        with st.expander("🤖 AI 智能分析 / AI Analysis" if st.session_state.language == "zh_CN" else "🤖 AI Analysis"):
            st.markdown("---")

            # 获取分析数据
            margins = analyzer.calculate_profit_margins()
            ratios = analyzer.calculate_financial_ratios()
            growth = analyzer.calculate_growth_rate(metric_names["Revenues"])

            # 创建 AI 分析器
            try:
                ai_analyst = AIFinancialAnalyst(language=st.session_state.language)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("📊 " + ("财务健康分析" if st.session_state.language == "zh_CN" else "Financial Health Analysis"),
                                use_container_width=True):
                        with st.spinner("AI 分析中..." if st.session_state.language == "zh_CN" else "AI analyzing..."):
                            analysis = ai_analyst.analyze_financial_health(summary, margins, ratios, growth)
                            st.session_state['ai_health_analysis'] = analysis

                with col2:
                    if st.button("💡 " + ("投资建议" if st.session_state.language == "zh_CN" else "Investment Advice"),
                                use_container_width=True):
                        with st.spinner("AI 分析中..." if st.session_state.language == "zh_CN" else "AI analyzing..."):
                            advice = ai_analyst.generate_investment_advice(summary, margins, ratios, growth)
                            st.session_state['ai_investment_advice'] = advice

                # 显示分析结果
                if 'ai_health_analysis' in st.session_state:
                    st.markdown("### 📊 " + ("财务健康分析" if st.session_state.language == "zh_CN" else "Financial Health Analysis"))
                    st.markdown(st.session_state['ai_health_analysis'])
                    st.markdown("---")

                if 'ai_investment_advice' in st.session_state:
                    st.markdown("### 💡 " + ("投资建议" if st.session_state.language == "zh_CN" else "Investment Advice"))
                    st.markdown(st.session_state['ai_investment_advice'])
                    st.markdown("---")

                # 问答功能
                st.markdown("### 💬 " + ("问答助手" if st.session_state.language == "zh_CN" else "Q&A Assistant"))
                question = st.text_input(
                    "提问关于财务数据的问题" if st.session_state.language == "zh_CN" else "Ask a question about the financial data",
                    placeholder="例如：Tesla 的盈利能力如何？" if st.session_state.language == "zh_CN" else "e.g., How is Tesla's profitability?"
                )

                if st.button("🔍 " + ("获取答案" if st.session_state.language == "zh_CN" else "Get Answer")):
                    if question:
                        with st.spinner("AI 思考中..." if st.session_state.language == "zh_CN" else "AI thinking..."):
                            financial_data = ai_analyst._prepare_financial_data(summary, margins, ratios, growth)
                            answer = ai_analyst.answer_question(question, financial_data)
                            st.markdown(answer)
                    else:
                        st.warning("请输入问题" if st.session_state.language == "zh_CN" else "Please enter a question")

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"AI 分析出错 / AI analysis error: {str(e)}")
    else:
        st.info("💡 " + ("提示：设置 OPENAI_API_KEY 环境变量以启用 AI 智能分析功能" if st.session_state.language == "zh_CN"
                        else "Tip: Set OPENAI_API_KEY environment variable to enable AI analysis features"))


if __name__ == "__main__":
    main()
