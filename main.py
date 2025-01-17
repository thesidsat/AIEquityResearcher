import pandas as pd
import datetime
from ai_equity_researcher.analyzer import StockAnalyzer
from ai_equity_researcher.llm import generate_insights_for_sections
from ai_equity_researcher.generate_report import save_report_to_pdf
def main():
    tickers = ["AAPL", "MSFT"]
    reports = []

    for ticker_symbol in tickers:
        analyzer = StockAnalyzer(ticker_symbol)
        report = analyzer.generate_report(year=2024, quarter="Q4")
        report = generate_insights_for_sections(report,model='phi4')

        save_report_to_pdf(report,ticker_symbol)
        data = report.copy()
        parsed_data = {}
        parsed_data['ticker'] = data['ticker']
        parsed_data['report_date'] = data['report_date']

        for section in data['sections']:
            section_name = section['name']
            for key, value in section['data'].items() if isinstance(section['data'], dict) else []:
                parsed_data[f"{section_name}_{key}"] = value

            # Add insights and signal separately
            parsed_data[f"{section_name}_insight"] = section['insight']
            parsed_data[f"{section_name}_signal"] = section['signal']

        # Convert the parsed data into a DataFrame
        parsed_df = pd.DataFrame([parsed_data])

        data_dir = "data/"
        filename = f"{data_dir}EquityResearch_{ticker_symbol}.csv"
        
        # Save the parsed DataFrame to a new CSV
        parsed_df.to_csv(filename, index=False)
        reports.append(data)
        print("CSV file parsed and saved as 'parsed_output.csv'")




if __name__ == "__main__":
    main()