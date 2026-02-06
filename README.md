# Tesla Financial Analysis System / Tesla 财务月报分析系统

English | 简体中文

---

## English

A Python-based Tesla financial data analysis system that fetches real-time financial data from SEC EDGAR and displays analysis results through a web interface.

### Features

- Automatically fetch latest Tesla financial data from SEC EDGAR
- Financial metrics analysis (revenue, profit margins, assets/liabilities, etc.)
- Year-over-year growth rate calculation
- Interactive chart visualization
- Real-time web interface
- **Multi-language support (Simplified Chinese / English)**
- **🤖 AI-Powered Analysis (OpenAI GPT-4)**
  - Financial health assessment
  - Investment advice generation
  - Intelligent Q&A assistant

### Project Structure

```
tesla-predition/
├── src/
│   ├── data/
│   │   └── sec_fetcher.py          # SEC data fetcher module
│   ├── analysis/
│   │   └── financial_analyzer.py   # Financial analysis module
│   ├── locales/
│   │   └── i18n.py                 # Internationalization module
│   └── web/
│       └── app.py                  # Streamlit web application
├── static/data/                    # Financial data storage
├── main.py                         # Original test script
├── run.py                          # Quick start script
├── pyproject.toml                  # Project configuration
└── README.md                       # Documentation
```

### Installation

Using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

### Usage

#### 1. Quick Start (Recommended)

```bash
python run.py
```

This script will automatically:
- Check dependencies
- Fetch Tesla financial data
- Start the web application

#### 2. Manual Start

For step-by-step operation:

```bash
# Fetch data
python -m src.data.sec_fetcher

# Start web interface
streamlit run src/web/app.py
```

Then open http://localhost:8501 in your browser

#### 3. Language Switching

Select language in the sidebar:
- 简体中文 (Simplified Chinese)
- English

#### 4. Enable AI Analysis (Optional)

1. Get OpenAI API Key: Visit [OpenAI Platform](https://platform.openai.com/api-keys)

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Edit `.env` file and add your API Key:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

4. Restart the application to use AI analysis features

For detailed instructions, see [AI Analysis Guide](AI_ANALYSIS_GUIDE.md)

### Analysis Content

- Revenue trend analysis
- Multi-dimensional profit margin analysis (gross margin, operating margin, net margin)
- Financial structure analysis (asset-liability structure)
- Year-over-year growth rate analysis

### Main Modules

#### Data Fetcher (src/data/sec_fetcher.py)

- Fetch Tesla financial data from SEC EDGAR API
- Extract key financial metrics (revenue, profit, assets, etc.)
- Multi-language data output support
- Automatic local data storage

#### Financial Analyzer (src/analysis/financial_analyzer.py)

- Calculate revenue trends
- Calculate year-over-year growth rates
- Analyze profit margins (gross, operating, net)
- Calculate financial ratios (debt-to-asset, equity ratio, etc.)
- Multi-language analysis results support

#### Internationalization (src/locales/i18n.py)

- Simplified Chinese and English support
- Unified translation management
- Localized financial metric names

#### Web Interface (src/web/app.py)

- Interactive dashboard
- Multi-dimensional charts
- Real-time data refresh
- Detailed data tables
- Language switching functionality

### Analysis Metrics

#### Revenue Metrics
- Revenue trends
- Year-over-year growth rate

#### Profit Metrics
- Gross profit, operating profit, net profit
- Gross margin, operating margin, net margin

#### Asset/Liability Metrics
- Total assets, total liabilities, stockholders' equity
- Debt-to-asset ratio, equity ratio, debt-to-equity ratio

#### Other Metrics
- Basic earnings per share (EPS)
- Cash and cash equivalents

### Data Source

Data sourced from the U.S. Securities and Exchange Commission (SEC) EDGAR database:
- Company CIK: 0001318605 (Tesla, Inc.)
- API Documentation: https://www.sec.gov/edgar/sec-api-documentation

### Notes

1. Please comply with SEC API rate limits (no more than 10 requests per second)
2. Data may be delayed; regular refresh recommended
3. Financial data is for reference only and does not constitute investment advice

### Tech Stack

- Python 3.13+
- Streamlit - Web framework
- Plotly - Data visualization
- Requests - HTTP requests
- Pandas - Data processing
- OpenAI - AI-powered analysis
- Python-dotenv - Environment management


---

## 简体中文

这是一个基于 Python 的 Tesla 财务数据分析系统，从 SEC EDGAR 获取实时财务数据，并通过 Web 界面展示分析结果。

### 功能特性

- 从 SEC EDGAR 自动获取 Tesla 最新财务数据
- 财务指标分析（营业收入、利润率、资产负债等）
- 同比增长率计算
- 交互式图表展示
- Web 界面实时查看
- **多语言支持（简体中文 / English）**
- **🤖 AI 智能分析（基于 OpenAI GPT-4）**
  - 财务健康状况评估
  - 投资建议生成
  - 智能问答助手

### 项目结构

```
tesla-predition/
├── src/
│   ├── data/
│   │   └── sec_fetcher.py          # SEC 数据获取模块
│   ├── analysis/
│   │   └── financial_analyzer.py   # 财务分析模块
│   ├── locales/
│   │   └── i18n.py                 # 国际化模块
│   └── web/
│       └── app.py                  # Streamlit Web 应用
├── static/data/                    # 存储财务数据
├── main.py                         # 原始测试脚本
├── run.py                          # 快速启动脚本
├── pyproject.toml                  # 项目配置和依赖
└── README.md                       # 项目说明
```

### 安装依赖

使用 uv 安装依赖：

```bash
uv sync
```

或使用 pip：

```bash
pip install -e .
```

### 使用方法

#### 1. 快速启动（推荐）

```bash
python run.py
```

这个脚本会自动：
- 检查依赖
- 获取 Tesla 财务数据
- 启动 Web 应用

#### 2. 手动启动

如果想分步操作：

```bash
# 获取数据
python -m src.data.sec_fetcher

# 启动 Web 界面
streamlit run src/web/app.py
```

然后在浏览器中打开 http://localhost:8501

#### 3. 语言切换

在 Web 界面左侧边栏选择语言：
- 简体中文
- English

#### 4. 启用 AI 智能分析（可选）

1. 获取 OpenAI API Key：访问 [OpenAI Platform](https://platform.openai.com/api-keys)

2. 创建 `.env` 文件：
```bash
cp .env.example .env
```

3. 编辑 `.env` 文件，填入你的 API Key：
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

4. 重启应用即可使用 AI 分析功能

详细说明请查看 [AI 分析功能指南](AI_ANALYSIS_GUIDE.md)

### 分析内容

- 营业收入趋势分析
- 利润率多维分析（毛利率、营业利润率、净利率）
- 财务结构分析（资产负债结构）
- 同比增长率分析

### 主要功能模块

#### 数据获取 (src/data/sec_fetcher.py)

- 从 SEC EDGAR API 获取 Tesla 财务数据
- 提取关键财务指标（收入、利润、资产等）
- 支持多语言数据输出
- 自动保存数据到本地

#### 财务分析 (src/analysis/financial_analyzer.py)

- 计算营业收入趋势
- 计算同比增长率
- 分析利润率（毛利率、营业利润率、净利率）
- 计算财务比率（资产负债率、权益比率等）
- 支持多语言分析结果

#### 国际化 (src/locales/i18n.py)

- 支持简体中文和英语
- 统一的翻译管理
- 财务指标名称本地化

#### Web 展示 (src/web/app.py)

- 交互式仪表板
- 多维度图表展示
- 实时数据刷新
- 详细数据表格
- 语言切换功能

### 分析指标

#### 收入指标
- 营业收入趋势
- 同比增长率

#### 利润指标
- 毛利润、营业利润、净利润
- 毛利率、营业利润率、净利率

#### 资产负债指标
- 总资产、总负债、股东权益
- 资产负债率、权益比率、负债权益比

#### 其他指标
- 基本每股收益 (EPS)
- 现金及现金等价物

### 数据来源

数据来源于美国证券交易委员会 (SEC) 的 EDGAR 数据库：
- 公司 CIK: 0001318605 (Tesla, Inc.)
- API 文档: https://www.sec.gov/edgar/sec-api-documentation

### 注意事项

1. 请遵守 SEC API 的访问限制（每秒不超过 10 个请求）
2. 数据可能存在延迟，建议定期刷新
3. 财务数据仅供参考，不构成投资建议

### 技术栈

- Python 3.13+
- Streamlit - Web 框架
- Plotly - 数据可视化
- Requests - HTTP 请求
- Pandas - 数据处理
- OpenAI - AI 智能分析
- Python-dotenv - 环境变量管理

### License
