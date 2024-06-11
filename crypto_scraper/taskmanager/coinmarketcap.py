from selenium import webdriver
from selenium.webdriver.common.by import By

class CoinMarketCap:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def scrape_coin_data(self, coin):
        url = f"https://coinmarketcap.com/currencies/{coin.lower()}/"
        self.driver.get(url)
        
        data = {}
        data['price'] = self._get_text(By.CSS_SELECTOR, '.priceValue')
        data['price_change'] = self._get_text(By.CSS_SELECTOR, '.sc-15yy2pl-0.kAXKAX')
        data['market_cap'] = self._get_text(By.CSS_SELECTOR, '.statsValue')
        data['market_cap_rank'] = self._get_text(By.CSS_SELECTOR, '.sc-16r8icm-0.kjciSH')
        data['volume'] = self._get_text(By.CSS_SELECTOR, '.statsValue')
        data['volume_rank'] = self._get_text(By.CSS_SELECTOR, '.sc-16r8icm-0.kjciSH')
        data['volume_change'] = self._get_text(By.CSS_SELECTOR, '.sc-15yy2pl-0.kAXKAX')
        data['circulating_supply'] = self._get_text(By.CSS_SELECTOR, '.statsValue')
        data['total_supply'] = self._get_text(By.CSS_SELECTOR, '.statsValue')
        data['diluted_market_cap'] = self._get_text(By.CSS_SELECTOR, '.statsValue')
        
        contracts = self._get_elements(By.CSS_SELECTOR, '.sc-1ow4cwt-0.clTRXi')
        data['contracts'] = [{'name': contract.find_element(By.CSS_SELECTOR, 'span').text, 'address': contract.find_element(By.CSS_SELECTOR, 'p').text} for contract in contracts]
        
        links = self._get_elements(By.CSS_SELECTOR, '.link-button')
        data['official_links'] = [{'name': link.text.lower(), 'link': link.get_attribute('href')} for link in links]
        
        socials = self._get_elements(By.CSS_SELECTOR, '.link-button')
        data['socials'] = [{'name': social.text.lower(), 'url': social.get_attribute('href')} for social in socials]
        
        self.driver.quit()
        return data

    def _get_text(self, by, value):
        try:
            return self.driver.find_element(by, value).text
        except:
            return None

    def _get_elements(self, by, value):
        try:
            return self.driver.find_elements(by, value)
        except:
            return []
