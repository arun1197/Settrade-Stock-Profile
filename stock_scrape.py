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
# scraper("AMARIN",0,12,0)


def scraper_v2_fix_error(stock_quote,company_percentage, num_of_years, capital):
	settrade_url_company_profile = "http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol="+stock_quote+"&ssoPageId=12&selectPage=3"

	page = requests.get(settrade_url_company_profile)
	tree = html.fromstring(page.content)

	company_info = tree.xpath('//div[@class="col-xs-8 col-md-6 text-left"]/text()')

	authorized_capital = tree.xpath('//div[@class="col-xs-6"]/text()')


	# print "Info: ", company_info

	initial_authorized_capital = "NA"
	# initial_authorized_capital = authorized_capital[0][:-3]
	# authorized_capital_in_baht = float(''.join(authorized_capital[0][:-3].split(",")))
	# print "Capital: ", authorized_capital_in_baht
	percent = company_info[-3]

	# first_trade_date_slice = company_info[2].split(" ")
	# num_of_years_trading = 2561 - int(first_trade_date_slice[-1])
	num_of_years_trading = "ab"

	free_float_percent = percent[:-1]
	company_holds = 100-float(free_float_percent)

	if (int(company_holds) >= company_percentage) and num_of_years_trading >= num_of_years:
		print "Stock: ", stock_quote.rjust(8), " | ", "Company-Holds: ", "%.2f" % company_holds,'%'.rjust(2), " | ", 'Years: ', str(num_of_years_trading).rjust(3), ' | ', 'Capital: ', initial_authorized_capital

# scraper_v2_fix_error("TFG",0,12,0)

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

	# quotes_to_remove = ["BTC", "CSL", "HOTPOT", "LHBANK", "NPP", "TFD", "TGCI", "TUCC", "VTE"]
	# final_stock_quotes = list(set(stock_list).difference(set(quotes_to_remove)))

# companies that no longer exist in the market
	stock_list.remove("BTC")
	stock_list.remove("CSL")
	stock_list.remove("HOTPOT")
	stock_list.remove("LHBANK")
	stock_list.remove("NPP")
	stock_list.remove("TFD")
	stock_list.remove("TGCI")
	stock_list.remove("TUCC")
	stock_list.remove("VTE")
# company that no longer exist in the market

	# final_stock_quotes[stock_list.index('F&D')] = 'F%26D'
	# final_stock_quotes[stock_list.index('FER')] = 'RP'
	# final_stock_quotes[stock_list.index('L&E')] = 'L%26E'
	stock_list[stock_list.index('F&D')] = 'F%26D'
	stock_list[stock_list.index('FER')] = 'RP'
	stock_list[stock_list.index('L&E')] = 'L%26E'

	for i in stock_list:
		try:
			scraper(i,company_percentage, num_of_years, capital)
		except Exception:
			scraper_v2_fix_error(i, company_percentage, num_of_years, capital)

	print "Total stock:", len(stock_list)
url = "http://siamchart.com/stock/"
scrape_stock_quote(url, 0, 0, 10000000000.0)
