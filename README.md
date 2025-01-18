# AI Equity Researcher

**AI Equity Researcher** uses local large language models (LLMs), to analyze financial and market data. The objective here is to create comprehensive, actionable equity reports and test the capabilities of local models.

---

## Features

### 1. **Data Collection**

- Fetches historical price, volume, and trading data using `yfinance`.
- Gathers company-specific information such as sector, industry, market cap, and financial ratios.

### 2. **Financial Analysis**

- Analyzes key financial metrics like revenue, net income, cash flow, capital expenditures, and profitability ratios.
- Evaluates liquidity, leverage, and valuation metrics (e.g., P/E ratios, Price-to-Book).

### 3. **Market Analysis**

- Provides an overview of stock price performance, volatility, trading volume, and beta.
- Includes 52-week high/low data to understand price trends.

### 4. **Industry and Sector Insights**

- Compares the company's performance against industry and sector benchmarks.

### 5. **AI-Driven Insights**

- Currently uses phi4 model to analyze financial and market data. This can be swapped by passing model name.
- Generates insights for each section, highlighting opportunities, risks, and actionable recommendations.
- Assigns buy, hold, or sell signals for each section based on AI analysis.

### 6. **Report Generation**

- Produces a comprehensive equity research report in PDF and csv format.
- Includes insights, recommendations, and key financial/market data in a structured layout.

### 7. **Analyst Recommendations**

- Aggregates analyst ratings and target price ranges.
- Summarizes strong buy, buy, hold, sell, and strong sell ratings.

### 8. **Recent News Highlights**

- Summarizes recent news related to the company for additional context.

---
## Key Classes and Functions

### StockAnalyzer

- **Methods:**
  - `get_ticker_history(start_date, end_date, interval)`: Fetches historical data.
  - `get_company_overview()`: Fetches company details like sector and market cap.
  - `fetch_financial_statements()`: Analyzes key financial metrics.
  - `get_market_performance_and_insight(start_date, end_date)`: Analyzes market trends and volatility.

---

## Installation

### Prerequisites
- Ollama
- Python 3.8 or higher
- Pip (Python package manager)

### Dependencies

Install the required Python libraries:

```bash
pip install -r requirements.txt
```
Run the researcher 
```bash
python main.py
```
Output should be in Reports dir

# Guidelines for Creating Pull Requests

## Fixing Bugs

1. **Describe the Bug:**
   - Clearly state the issue, including steps to reproduce it if applicable.
   - Link to any relevant issue in the repository.

2. **Propose a Solution:**
   - Provide a concise description of your fix.
   - Include comments in the code for clarity if necessary.

3. **Test Your Changes:**
   - Ensure your fix resolves the issue without breaking existing functionality.
   - Add test cases if applicable to validate the fix.

4. **Submit the PR:**
   - Use a descriptive title and include "Fixes #<issue-number>" if applicable.
   - Include a detailed explanation of the fix in the PR description.

---

## Adding Features

1. **Propose the Feature:**
   - Clearly describe the new feature and its purpose.
   - Link to any related issue or discussion.

2. **Implementation Plan:**
   - Outline the steps or modules that need changes or additions.
   - Consider potential impacts on existing functionality.

3. **Write Clear Code:**
   - Ensure code follows the project style and naming conventions.
   - Add comments where appropriate.

4. **Test Thoroughly:**
   - Verify the feature works as intended.
   - Add test cases to ensure future stability.

5. **Submit the PR:**
   - Use a descriptive title and explain the feature in the PR description.
   - Highlight any potential limitations or follow-up work.

6. **Documentation:**
   - Update relevant documentation (e.g., README, inline comments) to reflect the new feature.

---

## Contributing

1. **Fork the repository.**
2. **Create a new branch** for your feature or bug fix.
3. **Submit a pull request** with a detailed explanation of your changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Disclaimer

This tool generates AI-driven equity research reports based on historical and real-time data. These reports are for informational and research purposes only and should not be considered as financial advice. Always consult with a financial advisor before making investment decisions.