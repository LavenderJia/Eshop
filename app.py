from flask import Flask, redirect,flash, render_template, session, url_for, request,jsonify
import pymysql
import time
import os

app = Flask(__name__)
#app.jinja_env.variable_start_string = '{{ '
#app.jinja_env.variable_end_string = ' }}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/goods', methods=['GET'])
def index_page():
    cate_type = request.args.to_dict().get('type')
    print(cate_type)
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju', charset='utf8')
    cur = conn.cursor()
    goods_list = []
    if cate_type == 'all':
        sql = "select id, name, place, price from goods"
        cur.execute(sql)
        goods = cur.fetchall()
        goods = list(goods)
        print(goods)
        for i in range(0, len(goods)):
            temp = {}
            temp['id'] = goods[i][0]
            temp['name'] = goods[i][1]
            temp['place'] = goods[i][2]
            temp['price'] =goods[i][3]
            goods_list.append(temp)
            #print(goods_list)
        return jsonify(goods_list)
    else:
        sql = "select id, name, place, price from goods where category='"+cate_type+"'"
        cur.execute(sql)
        goods = cur.fetchall()
        goods = list(goods)
        print(goods)
        for i in range(0, len(goods)):
            temp = {}
            temp['id'] = goods[i][0]
            temp['name'] = goods[i][1]
            temp['place'] = goods[i][2]
            temp['price'] =goods[i][3]
            goods_list.append(temp)
            #print(goods_list)
        return jsonify(goods_list)


@app.route('/registerPurchaser', methods=['POST'])
def register_pur():
    register_data = request.get_json()
    print(register_data)
    register_res ={}
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    cur = conn.cursor()
    sql = "select id from purchasers where name='" + register_data['name'] +"'"
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    if res !=None:
        register_res['result'] = '用户名重复，请更改！'
        return jsonify(register_res)
    else:
        cur = conn.cursor()
        sql = "insert into purchasers(name, password, birth, sex, phone, email, address, balance) values('" + register_data['name'] + "', '"+register_data[
            'key']+"', '"+ register_data['birth'] + "', '" + register_data['sex'] + "', '" + register_data['phone'] + "', '" + register_data[
            'email'] + "', '"+ register_data['address'] +"', '"+ str(0) +"')"
        print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()
        register_res['result'] = 'success'
        return jsonify(register_res)


@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    print(login_data)
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    cur = conn.cursor()
    sql = "select id, name, password from purchasers where name='" + login_data['name'] +"'"
    cur.execute(sql)
    res = cur.fetchone()
    #res = list(res)
    print(res)
    if res == None:
        login_res = {'result': '该用户名不存在'}
        return jsonify(login_res)
    else:
        res = list(res)
        print(res)
        if res[2] != login_data['key']:
            login_res = {'result': '密码错误'}
            return jsonify(login_res)
        else:
            login_res ={}
            login_res['id'] = res[0]
            login_res['name'] = res[1]
            login_res['type'] = 'purchaser'
            login_res['result'] = 'success'
            return jsonify(login_res)


@app.route('/goodsInfo/<string:id>', methods=['GET'])
def goods_info(id):
    print(id)
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    cur = conn.cursor()
    sql = "select  name, description, price, stock, shop, place from goods where id='" + id +"'"
    cur.execute(sql)
    res = cur.fetchone()
    res = list(res)
    print(res)
    goods ={}
    goods['id'] = id
    goods['name'] = res[0]
    goods['description'] = res[1]
    goods['price'] = res[2]
    goods['stock'] = res[3]
    goods['shop'] = res[4]
    goods['place'] = res[5]
    return jsonify(goods)


@app.route('/purchaserInfo/<string:id>', methods=['GET'])
def purchaser_info(id):
    print(id)
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    cur = conn.cursor()
    sql = "select  name, password, sex, birth, phone, email, address, balance from purchasers where id='" + id +"'"
    cur.execute(sql)
    res = cur.fetchone()
    res = list(res)
    print(res)
    purchaser={}
    purchaser['id'] = id
    purchaser['name'] = res[0]
    purchaser['password'] = res[1]
    purchaser['sex'] = res[2]
    purchaser['birth'] = res[3]
    purchaser['phone'] = res[4]
    purchaser['email'] = res[5]
    purchaser['address'] = res[6]
    purchaser['balance'] = res[7]
    return jsonify(purchaser)


@app.route('/buy', methods=['POST'])
def buy():
    buy_data = request.get_json()
    print(buy_data)
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    sum = 0
    for i in range(0, len(buy_data)):
        cur = conn.cursor()
        sql = "insert into sale_record (purchaserId, goodsId, price, num, time) values ('" + str(buy_data[i][
            'purchaserId']) + "', '" + str(buy_data[i]['goodsId']) + "', '" + str(buy_data[i]['price']) + "', '" + str(buy_data[i][
                  'num']) + "', '" + str(now_time) + "')"
        #print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()

        cur = conn.cursor()
        sql = "update goods set stock=stock-" + str(buy_data[i]['num']) + " where id='" + str(buy_data[i]['goodsId']) +"'"
        #print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()

        cur = conn.cursor()
        sql = "delete from basket where purchaserId='" + str(buy_data[i]['purchaserId']) + "' and goodsId='" + str(buy_data[i][
            'goodsId']) + "'"
        cur.execute(sql)
        conn.commit()
        cur.close()

        sum = sum + float(buy_data[i]['price'])*int(buy_data[i]['num'])

    cur = conn.cursor()
    sql = "select balance from purchasers where id='" + str(buy_data[0]['purchaserId']) + "'"
    cur.execute(sql)
    balance = cur.fetchone()
    cur.close()
    changed_balance = balance[0] - sum

    cur = conn.cursor()
    sql = "update purchasers set balance='" + str(changed_balance) + "' where id='" + str(buy_data[0]['purchaserId']) + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()

    conn.close()
    buy_res={}
    buy_res['result'] = '下单成功，账户余额还剩' + str(changed_balance) + '元'
    return jsonify(buy_res)


@app.route('/basket', methods=['POST'])
def basket():
    basket_data = request.get_json()
    print(basket_data)
    basket_res={}
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    cur = conn.cursor()
    sql = "select id from basket where purchaserId='" + str(basket_data['purchaserId']) +"' and goodsId ='"+ str(basket_data['goodsId']) +"'"
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    if res != None:
        basket_res['result'] = '该商品已被添加过，请勿重复添加哦~'
        return jsonify(basket_res)
    else:
        cur = conn.cursor()
        sql = "insert into basket(purchaserId, goodsId, num) values ('" + str(basket_data['purchaserId']) + "', '" + str(basket_data['goodsId']) +"', '"+ str(basket_data['num'])+"')"
        print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        basket_res['result'] = '添加成功，可至个人中心查看哦~'
        return jsonify(basket_res)


@app.route('/collect', methods=['POST'])
def collect():
    collect_data=request.get_json()
    print(collect_data)
    collect_res ={}
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    cur = conn.cursor()
    sql = "select id from collection where purchaserId='" + str(collect_data['purchaserId']) +"' and goodsId ='"+ str(collect_data['goodsId'])+"'"
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    if res != None:
        collect_res['result'] = '该商品已被收藏过，请勿重复收藏哦~'
        return jsonify(collect_res)
    else:
        cur = conn.cursor()
        sql = "insert into collection(purchaserId, goodsId) values ('" + str(collect_data['purchaserId']) + "', '" + str(collect_data['goodsId']) +"')"
        print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        collect_res['result'] = '添加成功，可至个人中心查看哦~'
        return jsonify(collect_res)


@app.route('/basket', methods=['GET'])
def get_basket():
    purId = request.args.to_dict().get('id')
    print(purId)
    goods_list = []
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju', charset='utf8')
    cur = conn.cursor()
    sql = "select goodsId, num from basket where purchaserId='" + purId + "'"
    cur.execute(sql)
    goods_id_list = cur.fetchall()
    cur.close()
    if goods_id_list == None:
        return jsonify(goods_list)
    else:
        goods_id_list = list(goods_id_list)
        print(goods_id_list)

        for i in range(0, len(goods_id_list)):
            cur = conn.cursor()
            print(goods_id_list[i][0])
            sql = "select name, place, price, stock from goods where id='" + str(goods_id_list[i][0]) + "'"
            cur.execute(sql)
            goods = cur.fetchone()
            goods = list(goods)
            temp = {}
            temp['goodsId'] = goods_id_list[i][0]
            temp['name'] = goods[0]
            temp['place'] = goods[1]
            temp['price'] = goods[2]
            temp['stock'] = goods[3]
            temp['num'] = goods_id_list[i][1]
            goods_list.append(temp)
            # print(goods_list)
        return jsonify(goods_list)


@app.route('/collect', methods=['GET'])
def get_collect():
    purId = request.args.to_dict().get('id')
    print(purId)
    goods_list = []
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju', charset='utf8')
    cur = conn.cursor()
    sql = "select goodsId from collection where purchaserId='" + str(purId) + "'"
    cur.execute(sql)
    goods_id_list = cur.fetchall()
    cur.close()
    if goods_id_list == None:
        return jsonify(goods_list)
    else:
        goods_id_list = list(goods_id_list)
        print(goods_id_list)

        for i in range(0, len(goods_id_list)):
            cur = conn.cursor()
            print(goods_id_list[i][0])
            sql = "select name, place, price from goods where id='" + str(goods_id_list[i][0]) + "'"
            cur.execute(sql)
            goods = cur.fetchone()
            goods = list(goods)
            temp = {}
            temp['id'] = goods_id_list[i][0]
            temp['name'] = goods[0]
            temp['place'] = goods[1]
            temp['price'] = goods[2]
            goods_list.append(temp)
            # print(goods_list)
        return jsonify(goods_list)


@app.route('/bought', methods=['GET'])
def get_bought():
    purId = request.args.to_dict().get('id')
    print(purId)
    goods_list = []
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju', charset='utf8')
    cur = conn.cursor()
    sql = "select goodsId, price, num, time from sale_record where purchaserId='" + str(purId) + "'"
    cur.execute(sql)
    goods_id_list = cur.fetchall()
    cur.close()
    if goods_id_list == None:
        return jsonify(goods_list)
    else:
        goods_id_list = list(goods_id_list)
        print(goods_id_list)

        for i in range(0, len(goods_id_list)):
            cur = conn.cursor()
            print(goods_id_list[i][0])
            sql = "select name from goods where id='" + str(goods_id_list[i][0]) + "'"
            cur.execute(sql)
            goods = cur.fetchone()
            goods = list(goods)
            temp = {}
            temp['goodsId'] = goods_id_list[i][0]
            temp['name'] = goods[0]
            temp['price'] = goods_id_list[i][1]
            temp['num'] = goods_id_list[i][2]
            temp['time'] = goods_id_list[i][3]
            goods_list.append(temp)
            # print(goods_list)
        return jsonify(goods_list)


@app.route('/deleteBasket', methods=['POST'])
def delete_basket():
    delete_data = request.get_json()
    print(delete_data)
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju', charset='utf8')
    cur = conn.cursor()
    sql = "delete from basket where purchaserId='" + str(delete_data['purId']) + "' and goodsId='" + str(delete_data['goodsId']) + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify([])


@app.route('/deleteCollect', methods=['POST'])
def delete_collect():
    delete_data = request.get_json()
    print(delete_data)
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju', charset='utf8')
    cur = conn.cursor()
    sql = "delete from collection where purchaserId='" + str(delete_data['purId']) + "' and goodsId='" + str(delete_data['goodsId']) + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify([])


@app.route('/recharge', methods=['POST'])
def recharge():
    recharge_data=request.get_json()
    print(recharge_data)
    conn = pymysql.connect(host='120.79.145.97', user='Lavender', password='wjw151099124', db='erpnju',charset='utf8')
    cur = conn.cursor()
    sql = "select balance from purchasers where id='" + str(recharge_data['purId']) + "'"
    cur.execute(sql)
    balance = cur.fetchone()
    cur.close()
    changed_balance = balance[0] + float(recharge_data['money'])

    cur = conn.cursor()
    sql = "update purchasers set balance='" + str(changed_balance) + "' where id='" + str(recharge_data['purId']) + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

    recharge_res ={}
    recharge_res['result'] = '充值成功！'
    return jsonify(recharge_res)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
