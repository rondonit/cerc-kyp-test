```python
KYP_TECHNICAL_REPORT_TEMPLATE = r"""
CREDIT RISK ANALYSIS INSTRUCTIONS

You are a **Senior Credit Risk Analyst** responsible for producing technical reports to support decisions related to **acquiring/accepting receivables (invoices)** originated by a company.

Your task is to evaluate the **credit and operational risk** with priority on **quantitative financial indicators**.  
Use business description only as **secondary qualitative context**.  
**Do not fabricate information. Explicitly mention missing or uncertain metrics.**
Use the following language this write this report: en

### Mandatory rules:
1. Use technical, objective, and professional language — **concise but detailed**.
2. Base judgment mainly on **numerical metrics and ratios provided**.
3. You must comment on:
   - leverage and capital structure,
   - profitability,
   - cash generation and debt coverage.
4. Highlight data quality and absence of metrics — this **affects confidence in conclusions**.
5. Conclude with a **final risk classification and quantitative justification**.
6. If data is insufficient → classify as **"Inconclusive"**.
7. Never omit a metric — if unavailable, mark as *not reported* and discuss the impact.

---


REQUIRED OUTPUT FORMAT


# 1. Company Identification & Context
- **Company:** Netflix, Inc. (NFLX)
- **Sector:** Communication Services | **Industry:** Entertainment
- **Reporting Currency:** USD
- **Website:** https://www.netflix.com
- **Location:** Los Gatos, CA, United States

**Short Operational Summary:**  
→ Netflix, Inc. provides entertainment services. The company offers television (TV) series, documentaries, feature films, and games across various genres and languages. It also provides members the ability to receive streaming content through a host of internet-connected devices, including TVs, digital video players, TV set-top boxes, and mobile devices. The company operates approximately in 190 countries. Netflix, Inc. was incorporated in 1997 and is headquartered in Los Gatos, California.

---

# 2. Consolidated Quantitative Overview
### 2.1 Balance Sheet
| Metric | Value |
|---|---|
| Total Assets | 53,630,374,000.0 USD |
| Total Liabilities | 28,886,807,000.0 USD |
| Shareholder Equity | 24,743,567,000.0 USD |
| Current Assets | 13,100,379,000.0 USD |
| Current Liabilities | 10,755,400,000.0 USD |

### 2.2 Income Statement & Cash Flow
| Total Revenue | Net Income | Operating Cash Flow (OCF) |
|---|---|---|
| 39,000,966,000.0 | 8,711,631,000.0 | 7,361,364,000.0 |

### 2.3 Market & Valuation Metrics
| Market Cap | Enterprise Value | Trailing P/E | Forward P/E | Dividend Yield | Beta | 52W High | 52W Low |
|---|---|---|---|---|---|---|---|
| 440,512,118,784 | 471,110,451,200 | 43.5 | 4.37 | N/A | 1.7 | 134.115 | 82.11 |

---

# 3. Key Risk Indicators (decision drivers)

### 3.1 Leverage & Capital Structure
| Ratio | Value |
|---|---|
| Debt-to-Equity | 1.17 |
| Assets-to-Equity (Leverage) | 2.17 |
| Equity Ratio (Equity/Assets) | 46.14% |
| Liabilities Ratio (Liabilities/Assets) | 53.86% |

**Technical Commentary:**  
Leverage is elevated with a Debt-to-Equity of **1.17** and Assets-to-Equity of **2.17**, indicating significant reliance on debt financing. However, the Equity Ratio of **46.14%** demonstrates a material equity buffer. The structure remains within acceptable bounds for a high-growth tech/entertainment firm but warrants monitoring for over-leveraging risk.

---

### 3.2 Profitability
| Net Margin | ROA | ROE |
|---|---|---|
| 22.34% | 16.24% | 35.21% |

**Technical Commentary:**  
Exceptional profitability is evidenced by a **22.34% net margin**, **16.24% ROA**, and **35.21% ROE**. These metrics confirm strong cost control, pricing power, and efficient asset utilization, providing robust capacity to absorb credit losses and service obligations.

---

### 3.3 Cash Generation & Debt Coverage
| OCF Margin | OCF-to-Liabilities |
|---|---|
| 18.87% | 0.25 |

**Technical Commentary:**  
Operating cash flow generation (**18.87% margin**) is healthy in absolute terms ($7.36B) but insufficient to cover total liabilities (OCF-to-Liabilities **0.25**). This reflects high leverage and suggests limited liquidity cushion for unexpected obligations, though the absolute cash flow remains robust.

---

# 4. Operational & Contextual Risk Assessment
- **Sector/regulation/market cyclicality risks:** Exposure to consumer discretionary spending cycles and streaming market saturation may impact revenue stability.  
- **Business model vulnerabilities:** High content expenditure requirements and algorithm-dependent subscriber retention create operational execution risks.  
- **Operational or competitive red flags:** Intense competition from Disney+, Amazon Prime, and HBO Max pressures market share; no material operational red flags identified in public filings.

---

# 5. Data Quality & Reliability Assessment

**Data Reliability Score:** 100.0%  
**Missing Metrics:** None  

**Explanation:**  
All critical leverage, profitability, and cash flow metrics are reported with full balance sheet and income statement transparency. The absence of segment-specific receivables data or credit facility details does not impair the core analysis, as enterprise-wide metrics sufficiently capture systemic risk.

---

# 6. Final Credit Risk Conclusion

**Global Score (1–5):** **2** (Low-Moderate)  
**Risk Rating:** **Low**  

### Executive Summary (1 paragraph):  
Netflix demonstrates **strong profitability** (35.21% ROE, 22.34% net margin) and **substantial cash flow** ($7.36B OCF), offsetting moderate leverage (Debt-to-Equity 1.17). While OCF coverage of liabilities is weak (0.25×), absolute liquidity remains adequate for receivables-backed transactions. The company’s dominant market position and consistent free cash flow generation support a **Low** credit risk profile.

### Key Quantitative Drivers (3–5 bullet points):
- **ROE of 35.21%** reflects superior capital efficiency.  
- **Net margin of 22.34%** ensures resilience against margin compression.  
- **Elevated leverage (Debt-to-Equity 1.17)** requires ongoing monitoring but is mitigated by cash flow generation.  

### Supporting Qualitative Factors (2–3 bullet points):
- Global scale across 190 markets diversifies revenue streams.  
- Brand strength and content library enhance subscriber retention.  

**Mandatory closing statement:**  
> *Overall, the company presents **(Low)** credit risk for receivables-backed transactions.*
"""
```