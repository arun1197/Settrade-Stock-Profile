from lxml import html
import requests

def scraper(stock_quote,company_percentage, num_of_years, capital):
	settrade_url_company_profile = "http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol="+stock_quote+"&ssoPageId=12&selectPage=3"

	page = requests.get(settrade_url_company_profile)
	tree = html.fromstring(page.content)

	company_info = tree.xpath('//div[@class="col-xs-8 col-md-6 text-left"]/text()')
	authorized_capital = tree.xpath('//div[@class="col-xs-6"]/text()')
	initial_authorized_capital = authorized_capital[0][:-3]
	authorized_capital_in_baht = float(''.join(authorized_capital[0][:-3].split(",")))

	percent = company_info[-3]

	first_trade_date_slice = company_info[4].split(" ")
	num_of_years_trading = 2561 - int(first_trade_date_slice[-1])

	free_float_percent = percent[:-1]
	company_holds = 100-float(free_float_percent)

	# print "Authorized capital: ", authorized_capital_in_baht and authorized_capital_in_baht >= capital:
	if (int(company_holds) >= company_percentage) and num_of_years_trading >= num_of_years: 
		print "Stock: ", stock_quote.rjust(8), " | ", "Company-Holds: ", "%.2f" % company_holds,'%'.rjust(2), " | ", 'Years: ', str(num_of_years_trading).rjust(3), ' | ', 'Capital: ', initial_authorized_capital
# scraper("HMPRO",0,12)

def scrape_stock_quote(url,company_percentage, num_of_years, capital):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	# stock_quotes = tree.xpath('//a[@href="/stock-chart/HMPRO/"]/text()')
	stock_quotes_all = tree.xpath('//a/text()')[19:]
	stock_list = []
	count = 0

	for i in stock_quotes_all:
		str_quote = i[:i.find('(')]
		stock_list.append(str_quote)

	for i in stock_list:
		try:
			scraper(i,company_percentage, num_of_years, capital)
		except Exception:
			count = count + 1
			print "Stock: ", i

	print "Failed: ", count
	print "Passed: ", len(stock_list) - count
	print "Total stock:", len(stock_list)
url = "http://siamchart.com/stock/"
scrape_stock_quote(url, 0, 0, 10000000000.0)
