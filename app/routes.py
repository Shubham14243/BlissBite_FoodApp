import os

from flask import Blueprint, render_template, redirect, request, session, url_for
from werkzeug.utils import secure_filename

from app import db


class Storage:
    def __init__(self):
        self.int_val = -1
        self.message = ''
        self.login_var = 0


routes = Blueprint('route', __name__)
user = db.User()
adminob = db.Admin()
obj = Storage()


@routes.route('/')
@routes.route('/home')
def home():
    offer_data = user.get_offer_data()
    menu_data = user.get_menu_data()
    review_data = user.get_review_data()
    return render_template("index.html", odata=offer_data, mdata=menu_data, rdata=review_data)


@routes.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'user' not in session:
        email = request.form.get('email')
        password = request.form.get('password')
        msg = user.auth_user(email, password)
        if msg[0] == 1:
            userdata = msg[2]
            session['user'] = userdata[0]
            msg.pop()
            return redirect(url_for('route.menu'))
        else:
            return render_template("login.html", message=msg)
    else:
        if request.method == 'GET' and 'user' in session:
            return redirect(url_for('route.profile'))
        else:
            return render_template('login.html')


@routes.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('route.login'))


@routes.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and 'user' not in session:
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        msg = user.add_user(name, phone, email, password)
        if msg[0] == 1:
            return render_template("login.html", message=msg)
        else:
            return render_template("register.html", message=msg)
    else:
        if request.method == 'GET' and 'user' in session:
            return redirect(url_for('route.profile'))
        else:
            return render_template('register.html')


@routes.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')


@routes.route('/menu', methods=['POST', 'GET'])
def menu():
    msg = None
    msg = user.get_menu()
    menu_data = msg[2]
    msg = user.get_category()
    cate_data = msg[2]
    return render_template('menu.html', mdata=menu_data, cdata=cate_data)


@routes.route('/profile', methods=['POST', 'GET'])
def profile():
    if 'user' in session:
        msg = user.get_user(session['user'])
        if msg[0] == 1:
            add_msg = user.get_address(session['user'])
            add_book = user.get_booking(session['user'])
            userdata = msg[2]
            session['user'] = userdata[0]
            msg.pop()
            abc = user.get_breiforder(session['user'])
            return render_template("profile.html", message=msg, udata=userdata, adata=add_msg[2], bdata=add_book[2], odata=abc[2])
        else:
            return redirect(url_for('route.login'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/addaddress', methods=['GET', 'POST'])
def addaddress():
    if 'user' in session:
        if request.method == 'POST':
            userid = request.form['userid']
            landmark = request.form['landmark']
            add1 = request.form['add1']
            add2 = request.form['add2']
            city = request.form['city']
            pincode = request.form['pincode']
            default_val = 0
            msg = user.add_address(userid, landmark, add1, add2, city, pincode, default_val)
            return redirect(url_for('route.profile'))
        else:
            usid = session['user']
            return render_template('add_address.html', uid=usid)
    else:
        return redirect(url_for('route.login'))


@routes.route('/deleteaddress/<int:addid>', methods=['GET'])
def deleteaddress(addid):
    if 'user' in session:
        msg = user.delete_address(addid)
        return redirect(url_for('route.profile'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/add_booking', methods=['POST'])
def add_booking():
    if 'user' in session:
        if request.method == 'POST':
            userid = request.form['userid']
            bookdate = request.form['bookdate']
            booktime = request.form['booktime']
            no_person = request.form['no_person']
            msg = user.add_booking(userid, bookdate, booktime, no_person)
            return redirect(url_for('route.profile'))
        else:
            usid = session['user']
            return render_template('add_address.html', uid=usid)
    else:
        return redirect(url_for('route.login'))


@routes.route('/deletebooking/<int:bookid>', methods=['GET'])
def deletebooking(bookid):
    if 'user' in session:
        msg = user.delete_booking(bookid)
        return redirect(url_for('route.profile'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/updatereview', methods=['POST'])
def updatereview():
    if 'user' in session:
        if request.method == 'POST':
            userid = session['user']
            ratings = request.form['ratings']
            message = request.form['message']
            msg = user.update_review(userid, ratings, message)
        return redirect(url_for('route.profile'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/updateprofile', methods=['POST'])
def updateprofile():
    if 'user' in session:
        if request.method == 'POST':
            uname = request.form['username']
            uphone = request.form['userphone']
            uemail = request.form['useremail']
            msg = user.update_profile(uname, uphone, uemail)
        return redirect(url_for('route.profile'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/updatepassword', methods=['POST'])
def updatepassword():
    if 'user' in session:
        pmsg = None
        if request.method == 'POST':
            old = request.form['old']
            new = request.form['new']
            conf = request.form['conf']
            pmsg = user.update_password(session['user'], old, new)
        return redirect(url_for('route.profile'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/cart', methods=['POST', 'GET'])
def cart():
    if 'user' in session:
        msg = user.get_cart(session['user'])
        cart_data = msg[2]
        total_data = msg[3]
        msg.pop()
        msg.pop()
        return render_template('cart.html', message=msg, cdata=cart_data, total=total_data)
    else:
        return redirect(url_for('route.login'))


@routes.route('/addtocart/<int:itemid>', methods=['GET'])
def addtocart(itemid):
    if 'user' in session:
        msg = user.addto_cart(session['user'], itemid)
        return redirect(url_for('route.cart'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/updatecart', methods=['GET', 'POST'])
def updatecart():
    if 'user' in session:
        if request.method == 'POST':
            cartid = request.form['cartid']
            itemid = request.form['itemid']
            quantity = request.form['quantity']
            msg = user.update_cart(cartid, itemid, quantity)
        return redirect(url_for('route.cart'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/removecart/<int:cartid>', methods=['GET'])
def removecart(cartid):
    if 'user' in session:
        msg = user.delete_cart(cartid)
        return redirect(url_for('route.cart'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' in session:
        if request.method == 'POST':
            pass
        else:
            userid = session['user']
            add_msg = user.get_address(userid)
            check_msg = user.ready_checkout(userid)
            sum_data = check_msg[2]
            tot_data = check_msg[3]
            odid = check_msg[4]
            return render_template('checkout.html', adata=add_msg[2], sdata=sum_data, tdata=tot_data, odata=odid)
    else:
        return redirect(url_for('route.login'))


@routes.route('/setaddress', methods=['POST'])
def setaddress():
    if 'user' in session:
        if request.method == 'POST':
            addressid = request.form['addressid']
            msg = user.set_address(session['user'], addressid)
        return redirect(url_for('route.checkout'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/setoffer', methods=['POST'])
def setoffer():
    if 'user' in session:
        if request.method == 'POST':
            offercode = request.form['offercode']
            orderid = request.form['odid']
            msg = user.set_offer(orderid, offercode)
        return redirect(url_for('route.checkout'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/order', methods=['GET', 'POST'])
def order():
    if 'user' in session:
        if obj.int_val > 0:
            orderdata = user.get_orderdata(obj.int_val)
            itemdata = user.get_itemdata(obj.int_val)
            paydata = user.get_paydata(obj.int_val)
            adddata = user.get_adddata(obj.int_val)
            return render_template('order.html', odata=orderdata[2], idata=itemdata[2], pdata=paydata[2], adata=adddata[2])
        else:
            return redirect(url_for('route.profile'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/orderdetail/<int:orderid>', methods=['GET'])
def orderdetail(orderid):
    if 'user' in session:
        obj.int_val = orderid
        return redirect(url_for('route.order'))
    else:
        return redirect(url_for('route.login'))


@routes.route('/placeorder', methods=['POST'])
def placeorder():
    if 'user' in session:
        orderid = 0
        if request.method == 'POST':
            pay = request.form['pay']
            orderid = request.form['odid']
            total = request.form['total']
            msg = user.place_order(session['user'], orderid, pay, total)
        return redirect(url_for('route.orderdetail', orderid=orderid))
    else:
        return redirect(url_for('route.login'))


@routes.route('/deleteorder/<int:odid>', methods=['GET'])
def deleteorder(odid):
    if 'user' in session:
        msg = user.delete_order(odid)
        return redirect(url_for('route.profile'))
    else:
        return redirect(url_for('route.login'))


# ############################################################    ADMIN    #################################################


@routes.route('/admin', methods=['POST', 'GET'])
def admin():
    if 'admin' not in session:
        return redirect(url_for('route.admin_login'))
    else:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            data = msg[2]
            msg.pop()
            if obj.login_var != 1:
                msg.clear()
                msg = [0, '']
                obj.login_var = 0
            orderdata = adminob.get_orders()
            dashdata = adminob.get_dash()
            return render_template('admin/index.html', message=msg, user=data, odata=orderdata[2], ddata=dashdata[2])


@routes.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST' and 'admin' not in session:
        email = request.form.get('email')
        password = request.form.get('password')
        msg = adminob.auth_admin(email, password)
        if msg[0] == 1:
            session['admin'] = msg[2]
            obj.login_var = 1
            return redirect(url_for('route.admin'))
        else:
            return render_template("admin/login.html", message=msg)
    else:
        if request.method == 'GET' and 'admin' in session:
            return redirect(url_for('route.admin'))
        else:
            return render_template('admin/login.html')


@routes.route('/admin/logout', methods=['GET'])
def admin_logout():
    if 'admin' in session:
        session.pop('admin', None)
        obj.login_var = 0
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/register', methods=['POST', 'GET'])
def admin_register():
    if request.method == 'POST' and 'admin' not in session:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        msg = adminob.add_admin(name, email, password, confirm)
        return render_template("admin/create-account.html", message=msg)
    else:
        if request.method == 'GET' and 'admin' in session:
            return redirect(url_for('route.admin'))
        else:
            return render_template('admin/create-account.html')


@routes.route('/admin/forgot', methods=['POST', 'GET'])
def admin_forgot():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        msg = adminob.add_admin(name, email, password, confirm)
        return render_template("admin/create-account.html", message=msg)
    return render_template('admin/forgot-password.html')


@routes.route('/admin/item', methods=['POST', 'GET'])
def admin_item():
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            cate_data = None
            item_data = None
            data = msg[2]
            if request.method == 'POST':
                upload_dir = 'app/static/upload/item/'
                os.makedirs(upload_dir, exist_ok=True)
                categoryid = request.form.get('categoryid')
                name = request.form.get('name')
                description = request.form.get('description')
                imageurl = request.files['imageurl']
                price = request.form.get('price')
                filename = os.path.join(upload_dir, secure_filename(imageurl.filename))
                imageurl.save(filename)
                imageurl = 'upload/item/' + str(imageurl.filename)
                msg = adminob.add_item(categoryid, name, description, imageurl, price)
            msg = adminob.get_category()
            if msg[0] == 1:
                cate_data = msg[2]
                msg.pop()
            msg = adminob.get_item()
            if msg[0] == 1:
                item_data = msg[2]
                msg.pop()
            return render_template('admin/item.html', message=msg, cdata=cate_data, idata=item_data, user=data)
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/item/delete/<int:itemid>', methods=['GET'])
def admin_item_delete(itemid):
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            if request.method == 'GET':
                msg_del = adminob.del_item(itemid)
            return redirect(url_for('route.admin_item'))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/addcategory', methods=['POST'])
def admin_addcategory():
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            data = msg[2]
            cate_data = None
            if request.method == 'POST':
                cate_name = request.form['category_name']
                msg.clear()
                msg = adminob.add_category(cate_name)
                if msg[0] == 1:
                    msg = adminob.get_category()
                    if msg[0] == 1:
                        cate_data = msg[2]
                        msg.pop()
                    return render_template('admin/item.html', message=msg, cdata=cate_data, user=data)
            return render_template('admin/item.html', message=msg, user=data)
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/category/delete/<int:categoryid>', methods=['GET'])
def admin_category_delete(categoryid):
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            if request.method == 'GET':
                msg_del = adminob.del_category(categoryid)
            return redirect(url_for('route.admin_item'))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/booking', methods=['POST', 'GET'])
def admin_booking():
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            msg_offer = None
            if request.method == 'POST':
                upload_dir = 'app/static/upload/offer/'
                os.makedirs(upload_dir, exist_ok=True)
                offername = request.form.get('offername')
                offercode = request.form.get('offercode')
                minamount = request.form.get('minamount')
                offerdisc = request.form.get('offerdisc')
                imageurl = request.files['imageurl']
                offervalid = request.form.get('offervalid')
                filename = os.path.join(upload_dir, secure_filename(imageurl.filename))
                imageurl.save(filename)
                imageurl = 'upload/offer/' + str(imageurl.filename)
                msg_offer = adminob.add_offer(offername, offercode, minamount, offerdisc, imageurl, offervalid)
            mssg = None
            bookdata = None
            offerdata = None
            book = adminob.get_bookings()
            if book[0] == 1:
                bookdata = book[2]
                mssg = book
                mssg.pop()
            offer = adminob.get_offers()
            if offer[0] == 1:
                offerdata = offer[2]
                mssg = offer
                mssg.pop()
            if msg_offer:
                mssg = msg_offer
            return render_template('admin/booking.html', message=mssg, user=msg[2], bdata=bookdata, odata=offerdata)
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/booking/bookupdate/<int:updateid>', methods=['GET'])
@routes.route('/admin/booking/bookdelete/<int:deleteid>', methods=['GET'])
def admin_booking_update(updateid=None, deleteid=None):
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            msg_upd = None
            if request.method == 'GET':
                if updateid is not None:
                    msg_upd = adminob.upd_booking(updateid)
                if deleteid is not None:
                    msg_upd = adminob.del_booking(deleteid)
            return redirect(url_for('route.admin_booking', message=msg_upd))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/booking/offerupdate/<int:updateid>', methods=['GET'])
@routes.route('/admin/booking/offerdelete/<int:deleteid>', methods=['GET'])
def admin_offer_update(updateid=None, deleteid=None):
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            msg_upd = None
            if request.method == 'GET':
                if updateid is not None:
                    msg_upd = adminob.upd_offer(updateid)
                if deleteid is not None:
                    msg_upd = adminob.del_offer(deleteid)
            return redirect(url_for('route.admin_booking', message=msg_upd))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/customer', methods=['POST', 'GET'])
def admin_customer():
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            msg_user = None
            if request.method == 'POST':
                name = request.form.get('name')
                phone = request.form.get('phone')
                email = request.form.get('email')
                password = request.form.get('password')
                msg_user = user.add_user(name, phone, email, password)
            mssg = None
            cusdata = None
            cust = adminob.get_customers()
            if cust[0] == 1:
                cusdata = cust[2]
                mssg = cust
                mssg.pop()
            if msg_user:
                mssg = msg_user
            return render_template('admin/customer.html', message=mssg, user=msg[2], cdata=cusdata)
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/updatecustomerstatus/<int:userid>', methods=['GET'])
def updatecustomerstatus(userid):
    if 'admin' in session:
        msg = adminob.update_customer(userid)
        return redirect(url_for('route.admin_customer'))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/deletecustomer/<int:userid>', methods=['GET'])
def deletecustomer(userid):
    if 'admin' in session:
        msg = adminob.delete_customer(userid)
        return redirect(url_for('route.admin_customer'))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/profile', methods=['POST', 'GET'])
def admin_profile():
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            return render_template('admin/profile.html', user=msg[2])
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/removeorder/<int:odid>', methods=['GET'])
def removeorder(odid):
    if 'admin' in session:
        msg = user.delete_order(odid)
        return redirect(url_for('route.admin'))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/updateorderstatus/<int:odid>', methods=['GET'])
def updateorderstatus(odid):
    if 'admin' in session:
        msg = adminob.update_order(odid)
        return redirect(url_for('route.admin'))
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/vieworder/<int:odid>', methods=['GET'])
def vieworder(odid):
    if 'admin' in session:
        msg = adminob.get_data(session['admin'])
        if msg[0] == -1:
            redirect(url_for('route.admin_login'))
        else:
            orderdata = user.get_orderdata(odid)
            itemdata = user.get_itemdata(odid)
            paydata = user.get_paydata(odid)
            adddata = user.get_adddata(odid)
            return render_template('admin/orderdetails.html', user=msg[2], odata=orderdata[2], idata=itemdata[2], pdata=paydata[2], adata=adddata[2])
    else:
        return redirect(url_for('route.admin_login'))


@routes.route('/admin/updatepassword', methods=['POST'])
def admin_updatepassword():
    if 'admin' in session:
        pmsg = None
        if request.method == 'POST':
            old = request.form['old']
            new = request.form['new']
            conf = request.form['conf']
            pmsg = adminob.admin_update_password(session['admin'], old, new)
        return redirect(url_for('route.admin_profile'))
    else:
        return redirect(url_for('route.login'))
