from fpdf import FPDF
from datetime import datetime
import re

class EquityResearchReport(FPDF):
    def header(self):
        self.image('static/logo.jpg', 10, 8, 20)  
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Equity Research Report', 0, 1, 'C')
        self.ln(10) 


    def footer(self):
        self.set_y(-5)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, 'Disclaimer: The insights in this report are AI-generated and should not be considered as financial advice.', 0, 1, 'C')
        self.cell(0, 5, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, "AI Insights:", 0, 1)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

    def ai_signal(self, signal):
        self.ln(2)
        self.set_font('Arial', 'B', 10)
        if signal == 1:
            self.set_text_color(0, 128, 0)  # Green for positive
            signal_text = "[POSITIVE]"
        elif signal == 0:
            self.set_text_color(128, 128, 0)  # Yellow for neutral
            signal_text = "[NEUTRAL]"
        else:
            self.set_text_color(128, 0, 0)  # Red for negative
            signal_text = "[NEGATIVE]"
        self.cell(0, 5, f"AI Signal: {signal_text}", 0, 1, 'L')
        self.set_text_color(0, 0, 0)  # Reset text color
        self.ln(4)

    def financial_metric(self, label, value):
        self.set_font('Arial', '', 10)
        self.cell(60, 5, label, 0, 0)
        self.cell(0, 5, str(value), 0, 1)

def format_currency(value):
    if isinstance(value, str) and value.startswith('$'):
        return value
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)

def format_percentage(value):
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return str(value)

def save_report_to_pdf(data, ticker_symbol):
    pdf = EquityResearchReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f"{data['sections'][0]['data']['name']} ({ticker_symbol})", 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f"Report Date: {data['report_date']}", 0, 1, 'C')
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, "This report contains AI-generated insights and signals", 0, 1, 'C')
    pdf.ln(10)

    overview_section = next(s for s in data['sections'] if s['name'] == 'Company Overview')
    pdf.chapter_title('Company Overview')
    pdf.chapter_body(overview_section['insight'])
    pdf.ai_signal(overview_section['signal'])

    market_section = next(s for s in data['sections'] if s['name'] == 'Market Performance')
    pdf.chapter_title('Market Performance')
    market_data = market_section['data']
    pdf.financial_metric('Current Price:', format_currency(market_data['current_price']))
    pdf.financial_metric('52-Week Range:', f"{format_currency(market_data['52_week_low'])} - {format_currency(market_data['52_week_high'])}")
    pdf.financial_metric('Price Change:', market_data['price_change'])
    pdf.financial_metric('Market Cap:', format_currency(data['sections'][0]['data']['market_cap']))
    pdf.financial_metric('Beta:', market_data['beta'])
    pdf.ln(5)
    pdf.chapter_body(market_section['insight'])
    pdf.ai_signal(market_section['signal'])

    financial_section = next(s for s in data['sections'] if s['name'] == 'Financial Performance')
    pdf.chapter_title('Financial Performance')
    fin_data = financial_section['data']
    
    key_metrics = [
        ('Revenue', 'revenue'),
        ('Net Income', 'net_income'),
        ('Operating Cash Flow', 'operating_cash_flow'),
        ('Profit Margins', 'profit_margins'),
        ('Return on Equity', 'return_on_equity'),
        ('Current Ratio', 'current_ratio')
    ]
    
    for label, key in key_metrics:
        if key in fin_data:
            value = fin_data[key]
            if isinstance(value, float) and 'ratio' not in key.lower():
                value = format_percentage(value * 100)
            elif isinstance(value, str) and value.startswith('$'):
                value = format_currency(value.replace('$', '').replace(',', ''))
            pdf.financial_metric(label + ':', value)
    
    pdf.ln(5)
    pdf.chapter_body(financial_section['insight'])
    pdf.ai_signal(financial_section['signal'])

    analyst_section = next(s for s in data['sections'] if s['name'] == 'Analyst Recommendations')
    pdf.chapter_title('Analyst Recommendations')
    analyst_data = analyst_section['data']
    pdf.financial_metric('Target Price Range:', f"{format_currency(analyst_data['target_low_price'])} - {format_currency(analyst_data['target_high_price'])}")
    pdf.financial_metric('Strong Buy/Buy/Hold:', f"{analyst_data['strong_buy']}/{analyst_data['buy']}/{analyst_data['hold']}")
    pdf.financial_metric('Sell/Strong Sell:', f"{analyst_data['sell']}/{analyst_data['strong_sell']}")
    pdf.ln(5)
    pdf.chapter_body(analyst_section['insight'])
    pdf.ai_signal(analyst_section['signal'])

    # Recent News
    news_section = next(s for s in data['sections'] if s['name'] == 'Recent News')
    pdf.chapter_title('Recent News Highlights')
    for news in news_section['data'][:3]:
        pdf.set_font('Arial', 'B', 10)
        
        sanitized_title = re.sub(r'[^a-zA-Z0-9 ]', '', news['title'])  
        pdf.multi_cell(0, 5, sanitized_title)

        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 5, f"Source: {news['publisher']}", 0, 1)
        pdf.ln(2)
    
    sanitized_insight = re.sub(r'[^a-zA-Z0-9 ]', '', news_section['insight'])
    pdf.chapter_body(sanitized_insight)
    pdf.ai_signal(news_section['signal'])

    pdf.add_page()
    pdf.chapter_title('Important Disclaimers')
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 5, """This report contains AI-generated insights and signals that are based on historical data and current market information. Each section contains insights prefixed with "AI Insights:" which are generated through artificial intelligence analysis of various data points. These insights should not be considered as financial advice or recommendations to buy, sell, or hold any securities. The AI signals (Positive, Neutral, Negative) are algorithmic interpretations of data patterns and should be used as one of many tools in your investment research process.

Always conduct your own due diligence and consult with a qualified financial advisor before making any investment decisions. Past performance is not indicative of future results. Market conditions can change rapidly, and the information contained in this report may quickly become outdated.

The creator of this report make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability of the information contained within.""")

    # Save the report
    reports_dir = "reports/"
    # Construct the filename
    filename = f"{reports_dir}EquityResearch_{ticker_symbol}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    pdf.output(filename)
    return filename

