from lxml import html
import requests

def scraper(stock_quote,company_percentage, num_of_years):
	settrade_url_company_profile = "http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol="+stock_quote+"&ssoPageId=12&selectPage=3" 
	
	page = requests.get(settrade_url_company_profile)
	tree = html.fromstring(page.content)

	buyers = tree.xpath('//div[@class="col-xs-8 col-md-6 text-left"]/text()')
	
	percent = buyers[-3]
	
	first_trade_date_slice = buyers[4].split(" ")
	num_of_years_trading = 2561 - int(first_trade_date_slice[-1])
	
	free_float_percent = percent[:-1]
	company_holds = 100-float(free_float_percent)

	if (int(company_holds) >= company_percentage) and num_of_years_trading >= num_of_years:
		print "Stock: ", stock_quote.rjust(8), " | ", "Company-Holds: ", "%.2f" % company_holds,'%', " | ", 'Years: ', num_of_years_trading 
# scraper("AMARIN")

def scrape_stock_quote(url,company_percentage, num_of_years):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	# stock_quotes = tree.xpath('//a[@href="/stock-chart/HMPRO/"]/text()')
	stock_quotes_all = tree.xpath('//a/text()')[19:]
	stock_list = []
	
	for i in stock_quotes_all:
		str_quote = i[:i.find('(')]
		stock_list.append(str_quote)	

	for i in stock_list:
		try:
			scraper(i,company_percentage, num_of_years)
		except Exception:
			pass

url = "http://siamchart.com/stock/"
scrape_stock_quote(url, 56, 11)