from flask import Flask, Blueprint, request, redirect, render_template

from utils.cafe24API import SoldoutSolution

ss = SoldoutSolution()

soldOut = Blueprint(
    name="soldOut",
    import_name=__name__)

@soldOut.route('/refundOrder')
def refund():
  try:
    product_no = request.args['product_no']
    order_id = request.args['order_id']
  except:
    pass

  msg = ss.refundOrder(order_id, product_no)
  return jsonify({
      'msg': msg
  })


@soldOut.route('/saveOrder')
def refund():
  try:
    product_no = request.args['product_no']
    order_id = request.args['order_id']
  except:
    pass

  msg = ss.saveOrder(order_id, product_no)
  return jsonify({
      'msg': msg
  })


@soldOut.route('/exchangeOrder')
def refund():
  try:
    product_no = request.args['product_no']
    order_id = request.args['order_id']
  except:
    pass

  msg = ss.exchangeOrder(order_id, product_no)
  return jsonify({
      'msg': msg
  })
  
@soldOut.route('/')
def index():
  try:
    product_no = request.args['product_no']
    order_id = request.args['order_id']
  except:
    pass

  return render_template('recoform_m.html', product_no=product_no, order_id=order_id)
