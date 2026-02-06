"""
SEC 数据获取模块
从 SEC EDGAR 获取 Tesla 的财务报告数据
"""
import requests
import time
import json
from typing import Dict, List, Optional
from datetime import datetime
from src.locales.i18n import get_metric_names


class SECFetcher:
    """SEC 数据获取器"""

    def __init__(self, cik: str = "0001318605"):
        """
        初始化 SEC 数据获取器

        Args:
            cik: 公司的 CIK 代码，默认为 Tesla 的 CIK
        """
        self.cik = cik
        self.headers = {
            "User-Agent": "TeslaFinancialAnalysis contact@example.com",
            "Accept-Encoding": "gzip, deflate",
        }
        self.base_url = "https://data.sec.gov"

    def get_company_facts(self) -> Dict:
        """
        获取公司的财务事实数据

        Returns:
            包含公司财务数据的字典
        """
        url = f"{self.base_url}/api/xbrl/companyfacts/CIK{self.cik}.json"
        response = requests.get(url, headers=self.headers, timeout=30)
        time.sleep(0.2)  # 遵守 SEC 的速率限制

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def get_submissions(self) -> Dict:
        """
        获取公司的提交记录

        Returns:
            包含提交记录的字典
        """
        url = f"{self.base_url}/submissions/CIK{self.cik}.json"
        response = requests.get(url, headers=self.headers, timeout=30)
        time.sleep(0.2)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch submissions: {response.status_code}")

    def get_latest_filings(self, form_type: str = "10-Q", count: int = 4) -> List[Dict]:
        """
        获取最新的财务报告

        Args:
            form_type: 报告类型 (10-Q 季报, 10-K 年报)
            count: 获取的报告数量

        Returns:
            包含最新报告信息的列表
        """
        submissions = self.get_submissions()
        recent = submissions["filings"]["recent"]

        forms = recent["form"]
        accs = recent["accessionNumber"]
        dates = recent["filingDate"]

        filings = []
        for form, acc, date in zip(forms, accs, dates):
            if form == form_type and len(filings) < count:
                filings.append({
                    "form": form,
                    "accessionNumber": acc,
                    "filingDate": date
                })

        return filings

    def extract_financial_metrics(self, facts: Dict, language: str = "zh_CN") -> Dict:
        """
        从公司事实数据中提取关键财务指标

        Args:
            facts: 公司事实数据字典
            language: 语言代码 (zh_CN 或 en_US)

        Returns:
            包含财务指标的字典
        """
        metrics = {}

        # 获取 US-GAAP 数据
        us_gaap = facts.get("facts", {}).get("us-gaap", {})

        # 获取语言对应的指标名称
        key_metrics = get_metric_names(language)

        for metric_key, metric_name in key_metrics.items():
            if metric_key in us_gaap:
                # 获取最近的季度数据
                units = us_gaap[metric_key].get("units", {})

                # 尝试获取 USD 单位的数据
                if "USD" in units:
                    data_points = units["USD"]
                    # 过滤季度数据
                    quarterly_data = [
                        dp for dp in data_points
                        if dp.get("form") in ["10-Q", "10-K"] and dp.get("fp") in ["Q1", "Q2", "Q3", "Q4", "FY"]
                    ]
                    # 按日期排序
                    quarterly_data.sort(key=lambda x: x.get("end", ""), reverse=True)

                    metrics[metric_name] = quarterly_data[:8]  # 获取最近8个季度
                elif "USD/shares" in units:
                    data_points = units["USD/shares"]
                    quarterly_data = [
                        dp for dp in data_points
                        if dp.get("form") in ["10-Q", "10-K"] and dp.get("fp") in ["Q1", "Q2", "Q3", "Q4", "FY"]
                    ]
                    quarterly_data.sort(key=lambda x: x.get("end", ""), reverse=True)

                    metrics[metric_name] = quarterly_data[:8]

        return metrics

    def save_data(self, data: Dict, filename: str):
        """
        保存数据到 JSON 文件

        Args:
            data: 要保存的数据
            filename: 文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filename}")


if __name__ == "__main__":
    # 测试代码
    fetcher = SECFetcher()

    print("获取 Tesla 财务数据...")
    facts = fetcher.get_company_facts()

    print("提取财务指标...")
    metrics = fetcher.extract_financial_metrics(facts)

    print("保存数据...")
    fetcher.save_data(metrics, "static/data/tesla_financials.json")

    print("\n获取最新的季报...")
    latest_10q = fetcher.get_latest_filings("10-Q", 4)
    for filing in latest_10q:
        print(f"  {filing['filingDate']}: {filing['form']} - {filing['accessionNumber']}")

    print("\n数据获取完成！")
