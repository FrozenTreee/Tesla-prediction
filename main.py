import requests, time


CIK = "0001318605"
headers = {
    "User-Agent": "YourName your_email@example.com",
    "Accept-Encoding": "gzip, deflate",
}

sub_url = f"https://data.sec.gov/submissions/CIK{CIK}.json"
sub = requests.get(sub_url, headers=headers, timeout=30).json()
time.sleep(0.2)  # 保守一点，别刷太快

# 最近的 filing 列表（最近1000左右会在这里）
recent = sub["filings"]["recent"]

# 找最新的 10-K / 10-Q accession number（后续如果你要下载具体 filing 用得到）
forms = recent["form"]
accs  = recent["accessionNumber"]
dates = recent["filingDate"]

latest_10k = next((a for f,a,d in zip(forms, accs, dates) if f == "10-K"), None)
latest_10q = next((a for f,a,d in zip(forms, accs, dates) if f == "10-Q"), None)

print("latest 10-K accession:", latest_10k)
print("latest 10-Q accession:", latest_10q)

