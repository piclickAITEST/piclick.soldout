## 품절 대체 솔루션
## Author : Hyun Jin Woo

import requests
import json
import datetime

from utils.db_utils import *

class SoldoutSolution():
  
  def __init__(self, mallID):
    self.mallID = mallID
    self.version = ''
    self.OAUTH = {
      # "Authorization": f"Basic {base64_encode({client_id}:{client_secret})}",
      "Content-Type": "application/x-www-form-urlencoded",
    }
    with open('./config/auth.json', 'r') as f:
      self.AUTH = json.load(f)[self.mallID]

    self.HEADERS = {
      "Authorization": f"Bearer {self.AUTH['access_token']}" ,
      "Content-Type" : "application/json",
      "X-Cafe24-Api-Version": f"{self.version}",
    }
    
  # https://developers.cafe24.com/docs/api/admin/#get-authentication-code  
  def getAccessToken(self):
    
    # {mallid} : 해당 쇼핑몰ID를 입력합니다.
    # {client_secret} : 개발자 센터에서 생성한 앱의 client_secret을 입력합니다.
    # {client_id} : 개발자 센터에서 생성한 앱의 client_id를 입력합니다.
    # {code} : 발급받은 코드를 입력합니다.
    # {redirect_uri} : 개발자 센터에서 생성한 앱의 Redirect URL을 입력합니다.
    print('')
    
  # https://developers.cafe24.com/docs/api/admin/#get-access-token  
  def refreshAccessToken(self):
    
    # {mallid} : 해당 쇼핑몰ID를 입력합니다.
    # {domain} : 해당 쇼핑몰의 도메인을 입력합니다.
    # {client_id} : 개발자 센터에서 생성한 앱의 client_id를 입력합니다.
    # {client_secret} : 개발자 센터에서 생성한 앱의 client_secret을 입력합니다.
    # {refresh_token} : 토큰 발급시 받은 refresh_token을 입력합니다.
    
    postAccessTokenUsingRefreshTokenURL = f'https://{self.mallID}.cafe24api.com/api/v2/oauth/token'
    payload = {
      "grant_type" : "refresh_token",
      "refresh_token" : self.AUTH["refresh_token"],
    }
    
    res = requests.post(postAccessTokenUsingRefreshTokenURL, headers= self.OAUTH, data=payload)
    
    if res.status_code == 200:
      return res.json()
  
  # https://developers.cafe24.com/docs/api/admin/#get-a-cancellation  
  def postCreateCancellation(self, order_id, data):
    # Required Params
    # order_id, status
    
    items = [{"order_item_code": d["order_item_code"], "quantity": d["quantity"]} 
             for d in data['items']]
    
    postCreateCancellationURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/cancellation'
    payload = {
    "shop_no": 1,
    "requests": [
        {
            "order_id": f"{order_id}",
            "status": "canceled",
            "reason": "품절처리",
            "claim_reason_type": "H", # 품절
            "add_memo_too": "T",
            "recover_coupon": "T",
            "recover_inventory": "T",
            "refund_method_code": "T",
            "refund_bank_code": data["bank_code"],
            "refund_bank_account_no": data["bank_account_no"],
            "refund_bank_account_holder": data["bank_account_owner_name"],
            # "combined_refund_method": "T",
            "items": items
        }
    ]
    }
    
    res = requests.post(postCreateCancellationURL, data=json.dumps(payload), headers=self.HEADERS)
    if res.status_code == 200:
      print(order_id, ' 취소가 완료되었습니다.')
    else:
      print(res.json())
      raise Exception
    
    
  def getSoldoutProducts(self):
    
    jsonData = self.getListAllProducts()
    soldOutProducts = [d for d in jsonData['products'] if d['sold_out'] == 'T']
    
    # print("TOTAL PRODUCTS : ", len(jsonData['products']))
    # print("SOLDOUT PRODUCTS : ", len(soldOutProducts))
    # 솔드아웃 상품이 생겼을 때, 해당 상품을 샀던 유저들을 조회
    cancleOrders = {}
    
    # 모든 솔드아웃 제품 조회
    for sp in soldOutProducts:
      product_no = sp['product_no']
      product_code = sp['product_code']
      
      allOrders = self.getListAllOrders(product_code)['orders']
          
      if len(allOrders):
        for o in allOrders:
          cancleOrders[o["order_id"]] = {
            "member_id": o["member_id"],
            "items" : o["items"],
            "buyer" : o["buyer"],
            "postpay" : o["postpay"],
            "bank_code": o["bank_code"],
            # "refund_bank_account_no" : o["refund_bank_account_no"],
            "bank_account_no" : o["bank_account_no"],
            "bank_account_owner_name": o["bank_account_owner_name"]
          }
    
    # 품목별 취소처리
    for order_id, data in cancleOrders.items():
      self.postCreateCancellation(order_id, data)
    

    
    # with open('cancleOrders.json', 'w') as f:
    #   json.dump(cancleOrders, f, ensure_ascii=False)

  # https://developers.cafe24.com/docs/api/admin/#products-properties    
  def getListAllProducts(self):
    # Embed Params
    # discountprice, decorationimages, benefits, options, variants, additionalimages
    
    # Required Params
    # 
    getListAllProductsURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/products'
    res = requests.get(getListAllProductsURL, headers = self.HEADERS)
    if res.status_code == 200:
      return res.json()
    else:
      print(res.json())
      raise Exception
  
  # https://developers.cafe24.com/docs/api/admin/#list-all-orders  
  def getListAllOrders(self, product_code):
    # Embed Params
    # items, receivers, buyer, return, cancellation, exchange
    
    # Required Params
    # start_date, end_date
    now = datetime.datetime.now()
    start_date = (now - datetime.timedelta(weeks=4)).strftime('%Y-%m-%d') # 기준날짜 (최대 3개월)
    end_date = now.strftime('%Y-%m-%d') # 현재날짜
    order_status = 'N10,N20,N21,N22' # N00 : 입금전, N10: 상품 준비중, N20: 배송준비중, N21 : 배송대기, N22 : 배송보류, N30 : 배송중
    getListAllOrdersURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/orders?start_date={start_date}&end_date={end_date}&product_code={product_code}&order_status={order_status}&embed=buyer,items'

    res = requests.get(getListAllOrdersURL, headers = self.HEADERS)
    
    if res.status_code == 200:  
      return res.json()
    else:
      print(res.json())
      raise Exception
    
  def getCurrentProductState(self):
    mysql = MySQLAD()
    conn = mysql.connectMainDB()
    print(conn)
    conn.close()
    # mysql.dbClose()


soldOut = SoldoutSolution(mallID = 'wlsdn2215')
# soldOut.getSoldoutProducts()
soldOut.getCurrentProductState()
