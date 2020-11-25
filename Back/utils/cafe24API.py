## 품절 대체 솔루션
## Author : Hyun Jin Woo

import requests
import json
import datetime
import base64

# from db_utils import *

class SoldoutSolution():
  
  def __init__(self, mallID):
    self.mallID = mallID
    self.version = ''
    
    # appAuth = base64.b64encode(f"{self.AUTH['clientId']}:{self.AUTH['secretKey']}".encode('utf-8'))
    appAuth = 'TDdpdmF2TGtQZGtyZVY3ZGg4bmpFRzpTSVFUSlV5Uks1dGdObFFKSHBnM1ZD'
    self.OAUTH = {
      "Authorization": f"Basic {appAuth}",
      "Content-Type": "application/x-www-form-urlencoded",
    }
    
    with open('../config/auth.json', 'r') as f:
      self.AUTH = json.load(f)[self.mallID]
      
    self.refreshAccessToken()
    
    self.HEADERS = {
      "Authorization": f"Bearer {self.AUTH['access_token']}" ,
      "Content-Type" : "application/json",
      "X-Cafe24-Api-Version": f"{self.version}",
    }
  
  ### AUTH
  ##
  #
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
    payload = f'''grant_type=refresh_token&refresh_token={self.AUTH['refresh_token']}'''

    res = requests.post(postAccessTokenUsingRefreshTokenURL, headers= self.OAUTH, data=payload)
    
    print(res.json())
    
    if res.status_code == 200:
      access_token = res.json()['access_token']
      refresh_token = res.json()['refresh_token']
      
      self.AUTH['access_token'] = access_token
      self.AUTH['refresh_token'] = refresh_token
      
      # 파일로 재저장
      with open('../config/auth.json', 'r') as f:
        auth = json.load(f)
      
      auth[self.mallID] = res.json()
      
      with open('../config/auth.json', 'w') as f:
        json.dump(auth, f, ensure_ascii=False)
        
        
  ### PRODUCT
  ##
  #
  def getProduct(self, product_no):
    # Required Params
    # product_no
    
    getProductURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/products/{product_no}?embed=options'
    res = requests.get(getProductURL, headers=self.HEADERS)
    
    with open("product.json", 'w') as f:
      json.dump(res.json(), f, ensure_ascii=False)
    return res.json()
  
  def countAllProducts(self):
    
    countAllProductsURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/products/count'
    res = requests.get(countAllProductsURL, headers = self.HEADERS)
    print("TOTAL PRODUCT COUNT :", res.json()['count'])
    if res.status_code == 200:
      return res.json()
    else:
      print(res.json())
      raise Exception
  
  # https://developers.cafe24.com/docs/api/admin/#products-properties    
  def getListAllProducts(self):
    # Embed Params
    # discountprice, decorationimages, benefits, options, variants, additionalimages
    
    # Required Params
    # 
    
    count = self.countAllProducts()['count']
    limit = 100
    page = int(count / limit)
    offset = 0 
    
    products = []
    print("Get All Products ... ", end='')
    while(True):
      try:
        getListAllProductsURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/products?embed=options&limit={limit}&offset={offset * limit}'
        res = requests.get(getListAllProductsURL, headers = self.HEADERS)
        offset += 1
        if res.status_code == 200 and len(res.json()['products']):
          products += res.json()['products']
        else:
          break
        
      except:
        break
    
    print("END")
    return products

  ### ORDER
  ##
  #
  def getOrder(self, order_id):
    # Embed Params
    # items, receivers, buyer, benefits, coupons, return, cancellation, exchange, refunds
    
    # Required Params
    # order_id
    getOrderURL = f'https://{self.mallID}.cafe24api.com/api/v2/admin/orders/{order_id}?embed=items'
    res= requests.get(getOrderURL, headers=self.HEADERS)
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
  
  # https://developers.cafe24.com/docs/api/admin/#get-a-cancellation  
  def postCreateCancellation(self, order_id, data, refund_method_code):
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
            "payment_gateway_cancel": "T",
            "refund_method_code": refund_method_code if refund_method_code else 'F',
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
    
    products = self.getListAllProducts()
    print(products)
    soldOutProducts = [d for d in products if d['sold_out'] == 'T']
    
    print("TOTAL PRODUCTS : ", len(products))
    print("SOLDOUT PRODUCTS : ", len(soldOutProducts))
    
    debug = False
    # 솔드아웃 상품이 생겼을 때, 해당 상품을 샀던 유저들을 조회
    if len(soldOutProducts) and debug:
      cancleOrders = {}
      
      # 모든 솔드아웃 제품 조회
      for sp in soldOutProducts:
        product_no = sp['product_no']
        product_code = sp['product_code']
        
        allOrders = self.getListAllOrders(product_code)['orders']
            
        if len(allOrders):
          print(product_no, "Cancle Orders")
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
        self.postCreateCancellation(order_id, data, refund_method_code = None)
    
  # 교환하기
  def exchangeOrder(self, order_id, product_no):
    
    msg = '준비중입니다.'
    return msg
  
  # 환불하기
  def refundOrder(self, order_id, product_no):
    data = self.getOrder(order_id)['order']
    self.postCreateCancellation(order_id, order_id, data, refund_method_code = None)
    
    msg = ''
    return msg
  
  # 적립하기
  def saveOrder(self, order_id, product_no):
    data = self.getOrder(order_id)['order']
    self.postCreateCancellation(order_id, order_id, data, refund_method_code = 'M')
    
    msg = ''
    return msg
    

if __name__ == "__main__":
  # rlackdals1
  soldOut = SoldoutSolution(mallID = 'wlsdn2215')
  soldOut.getSoldoutProducts()
  
  


  # soldOut.getProduct(11)

