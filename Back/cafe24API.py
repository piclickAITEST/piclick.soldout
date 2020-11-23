## 품절 대체 솔루션
## Author : Hyun Jin Woo

import requests
import json

class SoldoutSolution():
  
  def __init__(self, mallID):
    self.mallID = mallID
    self.version = ''
    self.AUTH = {
      "access_token": "H1FfQKZLekldyHSJbxbWeF", 
      "refresh_token": "fJRpzL19DaxElOvU3PiFLB", 
      "clientId": "L7ivavLkPdkreV7dh8njEG", 
      "secretKey": "SIQTJUyRK5tgNlQJHpg3VC", 
      "servicekey": "svUHcF838zGmJkOXL50aT5TM2d9GOpsywYYTwI2EPEA=", 
    } 
    self.HEADERS = {
      "Authorization": f"Bearer {self.AUTH['access_token']}" ,
      "Content-Type" : "application/json",
      "X-Cafe24-Api-Version": f"{self.version}",
    }
    
  def getAccess_token(self):
    
    
  def refreshAccessToken(self):
    print('')
    
  def getSoldoutProducts(self):
    
      jsonData = self.getListAllProducts()
      
      print("PRODUCTS : ", len(jsonData))
      print("SOLDOUT PRODUCTS : ", len([d for d in jsonData['products'] if d['sold_out'] == 'T']))
      
      
  def getListAllProducts(self):
    # https://developers.cafe24.com/docs/api/admin/#products-properties
    # Embed Params
    # discountprice, decorationimages, benefits, options, variants, additionalimages
    
    # Required Params
    # 
    getListAllProductsURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/products'
    res = requests.get(getListAllProductsURL, headers = self.HEADERS)
    return res.json()
    
  def getListAllOrders(self):
    # https://developers.cafe24.com/docs/api/admin/#list-all-orders
    # Embed Params
    # items, receivers, buyer, return, cancellation, exchange
    
    # Required Params
    # start_date, end_date
    getListAllOrdersURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/orders?start_date=2020-09-01&end_date=2020-11-23'
    
    res = requests.get(getListAllOrdersURL, headers = self.HEADERS)
    return res.json()

soldOut = SoldoutSolution(mallID = 'wlsdn2215')
soldOut.ListAllProducts()
