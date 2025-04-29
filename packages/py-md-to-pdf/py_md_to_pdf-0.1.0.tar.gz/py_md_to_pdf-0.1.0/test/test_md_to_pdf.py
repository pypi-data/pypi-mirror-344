import pytest

from md_to_pdf import md_to_pdf


@pytest.mark.asyncio
async def test_md_to_pdf1():
    markdown_content = """# 测试
## 1. 文本
测试文本内容。
## 2.代码
```sql
-- SQL 示例：
SELECT SUM(Sales_Amount) AS Total_Sales
FROM Sales_Data
WHERE Order_Date BETWEEN "2023-01-01" AND "2023-02-01";
```
```python
from pathlib import Path

file_path = Path("...")
```
## 3. 表格
| 时间段             | 销售额（万元） | 变动原因推测         |
|-----------------|---------|----------------|
| 1月1日-1月7日       | 120万元   | 常规运营，元旦略有促销    |
| 1月8日-1月20日      | 250万元   | 节前购物潮，礼品销售增加   |
| 1月21日-1月28日（春节） | 80万元    | 春节假期，门店/线上活动减少 |
| 1月29日-2月1日      | 180万元   | 节后复工，消费逐步恢复    |"""
    await md_to_pdf(markdown_content)
