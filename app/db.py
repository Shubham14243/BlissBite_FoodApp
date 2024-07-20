import sqlite3
import cryptocode
from datetime import datetime

class DB:

    def __init__(self):
        self.__dbname = 'feane.db'
        self.__hash = 'enaef'

    def get_name(self):
        return self.__dbname

    def get_hash(self):
        return self.__hash


class User(DB):

    def __init__(self):
        super().__init__()
        self.__db = self.get_name()
        self.__hash = self.get_hash()

    def add_user(self, name, phone, email, password):
        message = ''
        status = 0
        validrev = 1

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        check_qry = 'SELECT * FROM user WHERE email = ?'
        cursor.execute(check_qry, (email,))
        row = cursor.fetchone()

        if row:
            conn.close()
            status = 0
            message = 'User Already Registered!'
        else:
            password = cryptocode.encrypt(password, self.__hash)
            try:
                add_qry = 'INSERT INTO user(name, phone, email, password, validrev) VALUES(?, ?, ?, ?, ?)'
                cursor.execute(add_qry, (name, phone, email, password, validrev,))
                conn.commit()
                status = 1
                message = 'User Registered Successfully!'
            except sqlite3.Error as e:
                status = -1
                message = f'Error Occured!\n{e}'
            finally:
                conn.close()
        msg = [status, message]
        return msg

    def auth_user(self, email, password):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        check_qry = 'SELECT * FROM user WHERE email = ?'
        cursor.execute(check_qry, (email,))
        row = cursor.fetchone()

        if row:
            raw = row[4]
            match_val = cryptocode.decrypt(raw, self.__hash)
            if password == match_val:
                try:
                    auth_qry = 'SELECT * FROM user WHERE email = ? AND password = ?'
                    cursor.execute(auth_qry, (email, raw,))
                    row2 = cursor.fetchone()
                    if row2:
                        status = 1
                        message = 'User Logged-In Successfully!'
                        data = row2
                    else:
                        status = -1
                        message = 'Error Occured!'
                except sqlite3.Error as e:
                    status = -1
                    message = f'Error Occured!\n{e}'
                finally:
                    conn.close()
            else:
                status = 0
                message = 'Invalid Password!'
        else:
            conn.close()
            status = 0
            message = 'User Not Registered!'
        msg = [status, message, data]
        return msg

    def get_user(self, userid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()
        try:
            auth_qry = 'SELECT * FROM user WHERE userid = ?'
            cursor.execute(auth_qry, (userid,))
            row = cursor.fetchone()
            if row:
                status = 1
                message = 'Userdata Fetched Successfully!'
                data = row
            else:
                status = -1
                message = 'Error Occured!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()
        msg = [status, message, data]
        return msg

    def get_menu(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT item.itemid, item.categoryid, category.categoryname, item.itemname, item.description, item.imageurl, item.price FROM item INNER JOIN category ON item.categoryid = category.categoryid'
            cursor.execute(check_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_category(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT DISTINCT c.categoryname FROM category c JOIN item i ON c.categoryid = i.categoryid'
            cursor.execute(check_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def add_address(self, userid, landmark, add1, add2, city, pincode, default_val):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'INSERT INTO address(userid, landmark, line1, line2, city, pincode, default_val) VALUES(?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(add_qry, (userid, landmark, add1, add2, city, pincode, default_val,))
            conn.commit()
            status = 1
            message = 'Address Added Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def get_address(self, userid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM address WHERE userid = ?'
            cursor.execute(check_qry, (userid,))
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def delete_address(self, addressid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'DELETE FROM address WHERE addressid = ?'
            cursor.execute(check_qry, (addressid,))
            conn.commit()
            status = 1
            message = 'Data Deleted Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def add_booking(self, userid, bookdate, booktime, no_person):
        message = ''
        status = 0

        date_time_str = f'{bookdate} {booktime}'
        book_status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'INSERT INTO book(userid, noperson, datetime, status) VALUES(?, ?, ?, ?)'
            cursor.execute(add_qry, (userid, no_person, date_time_str, book_status,))
            conn.commit()
            status = 1
            message = 'Booking Added Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def get_booking(self, userid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT bookid, date(datetime), time(datetime), noperson, status FROM book WHERE userid = ?'
            cursor.execute(check_qry, (userid,))
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def delete_booking(self, bookid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'DELETE FROM book WHERE bookid = ?'
            cursor.execute(check_qry, (bookid,))
            conn.commit()
            status = 1
            message = 'Data Deleted Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def update_review(self, userid, ratings, usermessage):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'UPDATE user SET review = ?, star = ?, validrev = 1 WHERE userid = ?'
            cursor.execute(add_qry, (usermessage, ratings, userid,))
            conn.commit()
            status = 1
            message = 'Ratings Updated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def update_profile(self, name, phone, email):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'UPDATE user SET name = ?, phone = ? WHERE email = ?'
            cursor.execute(add_qry, (name, phone, email,))
            conn.commit()
            status = 1
            message = 'Profile Updated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def update_password(self, usid, old, new):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT password FROM user WHERE userid = ?'
            cursor.execute(check_qry, (usid,))
            row = cursor.fetchone()
            if row:
                raw = row[0]
                match_val = cryptocode.decrypt(raw, self.__hash)
                if old == match_val:
                    password = cryptocode.encrypt(new, self.__hash)
                    add_qry = 'UPDATE user SET password = ? WHERE userid = ?'
                    cursor.execute(add_qry, (password, usid,))
                    conn.commit()
                    status = 1
                    message = 'Password Updated Successfully!'
                else:
                    status = 0
                    message = f'Password Not Matched!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def addto_cart(self, userid, itemid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT price FROM item WHERE itemid = ?'
            cursor.execute(get_qry, (itemid,))
            row = cursor.fetchone()
            quantity = 1
            total = row[0]
            add_qry = 'INSERT INTO cart(userid, itemid, quantity, total) VALUES(?, ?, ?, ?)'
            cursor.execute(add_qry, (userid, itemid, quantity, total,))
            conn.commit()
            status = 1
            message = 'Item Added to Cart Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def delete_cart(self, cartid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'DELETE FROM cart WHERE cartid = ?'
            cursor.execute(check_qry, (cartid,))
            conn.commit()
            status = 1
            message = 'Data Deleted Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def update_cart(self, cartid, itemid, quantity):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            if int(quantity) <= 0:
                self.delete_cart(cartid)
            else:
                get_qry = 'SELECT price FROM item WHERE itemid = ?'
                cursor.execute(get_qry, (itemid,))
                row = cursor.fetchone()
                price = row[0]
                total = int(quantity) * float(price)
                add_qry = 'UPDATE cart SET quantity = ?, total = ? WHERE cartid = ?'
                cursor.execute(add_qry, (quantity, total, cartid,))
                conn.commit()
                status = 1
                message = 'Item Updated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def get_cart(self, userid):
        message = ''
        status = 0
        data = None
        total = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT c.cartid, c.itemid, c.quantity, c.total, i.itemname, i.imageurl FROM cart c JOIN item i ON c.itemid = i.itemid WHERE userid = ?'
            cursor.execute(check_qry, (userid,))
            row = cursor.fetchall()
            if row:
                data = row
                check_qry = 'SELECT SUM(total) FROM cart WHERE userid = ?'
                cursor.execute(check_qry, (userid,))
                total_row = cursor.fetchone()
                total = total_row[0]
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data, total]

        return msg

    def set_address(self, userid, addressid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        default_val = 0

        try:
            add_qry = 'UPDATE address SET default_val = ? WHERE userid = ?'
            cursor.execute(add_qry, (default_val, userid,))
            conn.commit()
            default_val = 1
            add_qry = 'UPDATE address SET default_val = ? WHERE addressid = ?'
            cursor.execute(add_qry, (default_val, addressid,))
            conn.commit()
            status = 1
            message = 'Address Set Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def set_offer(self, orderid, offercode):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()
        valid = 1

        try:
            flag = 0
            get_qry = 'SELECT offerid FROM offer WHERE code = ? AND valid = ?'
            cursor.execute(get_qry, (offercode, valid))
            row = cursor.fetchone()
            if row:
                update_qry = 'Update orders set offerid = ? WHERE orderid = ?'
                cursor.execute(update_qry, (row[0], orderid,))
                conn.commit()
                self.update_offerdiscount(orderid)
                status = 1
                message = 'OrderList Updated Successfully!'
            else:
                status = 0
                message = 'Invalid Code!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def update_offerdiscount(self, orderid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT offerid, amount FROM orders WHERE orderid = ?'
            cursor.execute(get_qry, (orderid,))
            row = cursor.fetchone()
            if row:
                offid = row[0]
                amount = float(row[1])
                get_qry = 'SELECT minamount, discount FROM offer WHERE offerid = ?'
                cursor.execute(get_qry, (offid,))
                row2 = cursor.fetchone()
                if row2:
                    minamt = float(row2[0])
                    disc = float(row2[1])
                    if amount >= minamt:
                        offdiscamt = (amount*disc)/100
                        grandtotal = amount - offdiscamt
                        update_qry = 'Update orders set offeramount = ?, grandtotal = ? WHERE orderid = ?'
                        cursor.execute(update_qry, (offdiscamt, grandtotal, orderid,))
                        conn.commit()
                        status = 1
                        message = 'OrderList Updated Successfully!'
            else:
                status = 0
                message = 'Error Occured!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def get_summary(self, userid):
        message = ''
        status = 0
        data = None
        total = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT c.quantity, c.total, i.itemname, i.price FROM cart c JOIN item i ON c.itemid = i.itemid WHERE userid = ?'
            cursor.execute(check_qry, (userid,))
            row = cursor.fetchall()
            if row:
                data = row
                check_qry = 'SELECT SUM(total) FROM cart WHERE userid = ?'
                cursor.execute(check_qry, (userid,))
                total_row = cursor.fetchone()
                total = total_row[0]
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data, total]

        return msg

    def get_addressid(self, userid):
        try:
            default_val = 1
            conn = sqlite3.connect(self.__db)
            cursor = conn.cursor()
            get_qry = 'SELECT addressid FROM address WHERE userid = ? AND default_val = ?'
            cursor.execute(get_qry, (userid, default_val,))
            row = cursor.fetchone()
            if row:
                addressid = row[0]
            else:
                addressid = 0
            return addressid
        except sqlite3.Error as e:
            print('AddressID Error', e)

    def check_order_init(self, userid):
        try:
            odstatus = '-1'
            conn = sqlite3.connect(self.__db)
            cursor = conn.cursor()
            chk_qry = 'SELECT orderid FROM orders WHERE userid = ? AND odstatus = ?'
            cursor.execute(chk_qry, (userid, odstatus,))
            odrow = cursor.fetchone()
            if odrow:
                orderid = odrow[0]
            else:
                orderid = 0
            return orderid
        except sqlite3.Error as e:
            print('Check Order Init Error', e)

    def ready_checkout(self, userid):
        message = ''
        status = 0
        data = None
        od_summary = None
        odrow = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        datetime_str = ''
        amount = 0
        offerid = 0
        offeramt = 0
        grandtotal = 0
        odstatus = '-1'
        paystatus = 0
        orderid = 0

        try:
            addressid = self.get_addressid(userid)
            orderid = self.check_order_init(userid)
            if orderid == 0:
                create_qry = 'INSERT INTO orders(userid, datetime, amount, offerid, offeramount, grandtotal, addressid, odstatus, paystatus) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
                cursor.execute(create_qry, (userid, datetime_str, amount, offerid, offeramt, grandtotal, addressid, odstatus, paystatus,))
                orderid = cursor.lastrowid
                conn.commit()
            data = self.get_summary(userid)
            od_summary = data[2]
            total_amount = data[3]
            update_qry = 'Update orders set amount = ?, grandtotal = ? WHERE orderid = ?'
            cursor.execute(update_qry, (total_amount, total_amount, orderid,))
            conn.commit()
            self.update_offerdiscount(orderid)
            chk_qry = 'SELECT amount, offeramount, grandtotal FROM orders WHERE orderid = ?'
            cursor.execute(chk_qry, (orderid,))
            odrow = cursor.fetchone()
            status = 1
            message = 'Order Initiated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, od_summary, odrow, orderid]

        return msg

    def update_orderlist(self, userid, orderid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'SELECT * FROM cart WHERE userid = ?'
            cursor.execute(add_qry, (userid,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    create_qry = 'INSERT INTO orderlist(orderid, itemid, quantity, total) VALUES(?, ?, ?, ?)'
                    cursor.execute(create_qry, (orderid, row[2], row[3], row[4],))
                    conn.commit()
            del_qry = 'DELETE FROM cart WHERE userid = ?'
            cursor.execute(del_qry, (userid,))
            conn.commit()
            status = 1
            message = 'OrderList Updated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def place_order(self, userid, orderid, pay, total):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M")

        odstatus = 1
        paystatus = 1

        if pay == 'UPI':
            paystatus = 1
        if pay == 'CASH':
            paystatus = -1

        try:
            addressid = int(self.get_addressid(userid))
            if addressid != 0:
                upd_qry = 'UPDATE orders SET datetime = ?, odstatus = ?, paystatus = ?, addressid = ? WHERE orderid = ?'
                cursor.execute(upd_qry, (dt_string, odstatus, paystatus, addressid, orderid,))
                conn.commit()
                add_qry = 'INSERT INTO payment(orderid, amount, mode) VALUES(?, ?, ?)'
                cursor.execute(add_qry, (orderid, total, pay,))
                conn.commit()
                msg = self.update_orderlist(userid, orderid)
                status = 1
                message = 'Order Placed Successfully!'
            else:
                status = 0
                message = 'Please Select A Delivery Address!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def get_orderdata(self, orderid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM orders WHERE orderid = ?'
            cursor.execute(check_qry, (orderid,))
            row = cursor.fetchone()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_itemdata(self, orderid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT c.quantity, c.total, i.itemname, i.price FROM orderlist c JOIN item i ON c.itemid = i.itemid WHERE c.orderid = ?'
            cursor.execute(check_qry, (orderid,))
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_paydata(self, orderid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM payment WHERE orderid = ?'
            cursor.execute(check_qry, (orderid,))
            row = cursor.fetchone()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_adddata(self, orderid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT addressid FROM orders WHERE orderid = ?'
            cursor.execute(check_qry, (orderid,))
            row = cursor.fetchone()
            if row[0] > 0:
                check_qry = 'SELECT * FROM address WHERE addressid = ?'
                cursor.execute(check_qry, (row[0],))
                row = cursor.fetchone()
                if row:
                    data = row
                    status = 1
                    message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_breiforder(self, userid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT orderid, datetime, grandtotal, odstatus, paystatus FROM orders WHERE userid = ? and odstatus > -1'
            cursor.execute(check_qry, (userid,))
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def delete_order(self, orderid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'DELETE FROM payment WHERE orderid = ?'
            cursor.execute(check_qry, (orderid,))
            conn.commit()
            check_qry = 'DELETE FROM orderlist WHERE orderid = ?'
            cursor.execute(check_qry, (orderid,))
            conn.commit()
            check_qry = 'DELETE FROM orders WHERE orderid = ?'
            cursor.execute(check_qry, (orderid,))
            conn.commit()
            status = 1
            message = 'Data Deleted Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_offer_data(self):
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM offer WHERE valid = 1 ORDER BY offerid DESC LIMIT 2'
            cursor.execute(check_qry)
            data = cursor.fetchall()
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        return data

    def get_menu_data(self):
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM item LIMIT 3'
            cursor.execute(check_qry)
            data = cursor.fetchall()
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        return data

    def get_review_data(self):
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT name, review, star FROM user WHERE validrev = 1 ORDER BY userid DESC LIMIT 3'
            cursor.execute(check_qry)
            data = cursor.fetchall()
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        return data


class Admin(DB):

    def __init__(self):
        super().__init__()
        self.__db = self.get_name()
        self.__hash = self.get_hash()

    def add_admin(self, name, email, password, confirm):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        chkadmin = 'SELECT COUNT(*) FROM admin'
        cursor.execute(chkadmin)
        count = cursor.fetchall()

        if count[0][0] <= 0:
            if password != confirm:
                status = 0
                message = 'Password and Confirm Password Not Matched!'
            else:
                password = cryptocode.encrypt(password, self.__hash)
                try:
                    role = 'admin'
                    add_qry = 'INSERT INTO admin(role, name, email, password) VALUES(?, ?, ?, ?)'
                    cursor.execute(add_qry, (role, name, email, password,))
                    conn.commit()
                    status = 1
                    message = 'Admin Registered Successfully!'
                except sqlite3.Error as e:
                    status = -1
                    message = f'Error Occured!\n{e}'
                finally:
                    conn.close()
        else:
            conn.close()
            status = 0
            message = 'Admin Already Registered!'
        msg = [status, message]
        return msg

    def auth_admin(self, email, password):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT adminid, password FROM admin WHERE email = ?'
            cursor.execute(check_qry, (email,))
            row = cursor.fetchone()

            if row:
                raw = row[1]
                match_val = cryptocode.decrypt(raw, self.__hash)
                if password == match_val:
                    status = 1
                    message = 'Admin Logged-In Successfully!'
                    data = row[0]
                else:
                    status = 0
                    message = 'Invalid Password!'
            else:
                conn.close()
                status = 0
                message = 'Admin Not Registered!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]
        return msg

    def get_category(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM category'
            cursor.execute(check_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
            else:
                status = 0
                message = "No Data Found!"
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def add_category(self, name):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'INSERT INTO category(categoryname) VALUES(?)'
            cursor.execute(add_qry, (name,))
            conn.commit()
            status = 1
            message = 'Category Added Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]
        return msg

    def del_category(self, categoryid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            del_qry = 'DELETE FROM category WHERE categoryid = ?'
            cursor.execute(del_qry, (categoryid,))
            conn.commit()
            del_qry = 'DELETE FROM item WHERE categoryid = ?'
            cursor.execute(del_qry, (categoryid,))
            conn.commit()
            status = 1
            message = 'Category Deleted Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]
        return msg

    def add_offer(self, name, code, amount, discount, imgurl, valid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'INSERT INTO offer(name, code, minamount, discount, imageurl, valid) VALUES(?, ?, ?, ?, ?, ?)'
            cursor.execute(add_qry, (name, code, amount, discount, imgurl, valid,))
            conn.commit()
            status = 1
            message = 'Offer Added Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]
        return msg

    def get_data(self, adminid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM admin WHERE adminid = ?'
            cursor.execute(check_qry, (adminid,))
            row = cursor.fetchone()
            if row:
                data = row
                status = 1
                message = 'Logged-In Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_customers(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM user'
            cursor.execute(check_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Customers Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_bookings(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT book.bookid, book.userid, user.name, book.noperson, book.datetime, book.status FROM book INNER JOIN user ON book.userid = user.userid'
            cursor.execute(check_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def upd_booking(self, bookid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT status FROM book WHERE bookid = ?'
            cursor.execute(get_qry, (bookid,))
            row = cursor.fetchone()
            if row:
                val = 0
                upd_qry = 'UPDATE book SET status = ? WHERE bookid = ?'
                if row[0] == 0:
                    val = 1
                elif row[0] == 1:
                    val = -1
                elif row[0] == -1:
                    val = 0
                else:
                    val = 0
                cursor.execute(upd_qry, (val, bookid,))
                conn.commit()
                status = 1
                message = 'Booking Updated Successfully!'
            else:
                status = 0
                message = 'Booking Not Found!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

    def del_booking(self, bookid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'DELETE FROM book WHERE bookid = ?'
            row = cursor.execute(get_qry, (bookid,))
            conn.commit()
            if row:
                status = 1
                message = 'Booking Deleted Successfully!'
            else:
                status = 0
                message = 'Booking Not Found!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]
        return msg

    def get_offers(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT * FROM offer'
            cursor.execute(check_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def upd_offer(self, offerid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT valid FROM offer WHERE offerid = ?'
            cursor.execute(get_qry, (offerid,))
            row = cursor.fetchone()
            if row:
                val = 0
                upd_qry = 'UPDATE offer SET valid = ? WHERE offerid = ?'
                if row[0] == 0:
                    val = 1
                elif row[0] == 1:
                    val = 0
                else:
                    val = 0
                cursor.execute(upd_qry, (val, offerid,))
                conn.commit()
                status = 1
                message = 'Offer Updated Successfully!'
            else:
                status = 0
                message = 'Offer Not Found!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

    def del_offer(self, offerid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'DELETE FROM offer WHERE offerid = ?'
            row = cursor.execute(get_qry, (offerid,))
            conn.commit()
            if row:
                status = 1
                message = 'Offer Deleted Successfully!'
            else:
                status = 0
                message = 'Offer Not Found!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]
        return msg

    def get_item(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT item.itemid, item.categoryid, category.categoryname, item.itemname, item.description, item.imageurl, item.price FROM item INNER JOIN category ON item.categoryid = category.categoryid'
            cursor.execute(get_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
            else:
                status = 0
                message = 'No Items Found!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def add_item(self, categoryid, name, description, imageurl, price):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            add_qry = 'INSERT INTO item(categoryid, itemname, description, imageurl, price) VALUES(?, ?, ?, ?, ?)'
            cursor.execute(add_qry, (categoryid, name, description, imageurl, price,))
            conn.commit()
            status = 1
            message = 'Item Added Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]
        return msg

    def del_item(self, itemid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'DELETE FROM item WHERE itemid = ?'
            row = cursor.execute(get_qry, (itemid,))
            conn.commit()
            if row:
                status = 1
                message = 'Item Deleted Successfully!'
            else:
                status = 0
                message = 'Item Not Found!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]
        return msg

    def get_orders(self):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT o.orderid, o.userid, o.datetime, o.amount, o.offeramount, o.grandtotal, o.odstatus, o.paystatus, a.landmark, a.line1, a.line2, a.city, a.pincode FROM orders o INNER JOIN address a ON o.addressid = a.addressid WHERE o.odstatus > -1'
            cursor.execute(get_qry)
            row = cursor.fetchall()
            if row:
                data = row
                status = 1
                message = 'Data Fetched Successfully!'
            else:
                status = 0
                message = 'No Items Found!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def get_dash(self):
        message = ''
        status = 0
        data = [0, 0, 0, 0]

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT COUNT(*) FROM user'
            cursor.execute(get_qry)
            row = cursor.fetchone()
            if row:
                data[0] = row[0]
            get_qry = 'SELECT COUNT(*) FROM orders'
            cursor.execute(get_qry)
            row = cursor.fetchone()
            if row:
                data[1] = row[0]
            get_qry = 'SELECT SUM(grandtotal) FROM orders'
            cursor.execute(get_qry)
            row = cursor.fetchone()
            if row:
                data[2] = row[0]
            get_qry = 'SELECT COUNT(*) FROM item'
            cursor.execute(get_qry)
            row = cursor.fetchone()
            if row:
                data[3] = row[0]
            status = 1
            message = 'Data Fetched Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message, data]

        return msg

    def update_order(self, orderid):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            upd_qry = 'UPDATE orders SET odstatus = ?, paystatus = ? WHERE orderid = ?'
            cursor.execute(upd_qry, (2, 1, orderid,))
            conn.commit()
            status = 1
            message = 'Data Updated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def update_customer(self, userid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            get_qry = 'SELECT validrev FROM user WHERE userid = ?'
            cursor.execute(get_qry, (userid,))
            row = cursor.fetchone()
            if row:
                data = row[0]
            upd_qry = 'UPDATE user SET validrev = ? WHERE userid = ?'
            if data == 0:
                cursor.execute(upd_qry, (1, userid,))
            else:
                cursor.execute(upd_qry, (0, userid,))
            conn.commit()
            status = 1
            message = 'Data Updated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def clear_book_cart(self, userid):
        conn = sqlite3.connect(self.__db)
        try:
            cursor = conn.cursor()
            upd_qry = 'DELETE FROM book WHERE userid = ?'
            cursor.execute(upd_qry, (userid,))
            conn.commit()
            upd_qry = 'DELETE FROM cart WHERE userid = ?'
            cursor.execute(upd_qry, (userid,))
            conn.commit()
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

    def clear_orders(self, userid):
        conn = sqlite3.connect(self.__db)
        try:
            cursor = conn.cursor()
            get_qry = 'SELECT orderid FROM orders WHERE userid = ?'
            cursor.execute(get_qry, (userid,))
            row = cursor.fetchall()
            if row:
                for oid in row:
                    upd_qry = 'DELETE FROM orderlist WHERE orderid = ?'
                    cursor.execute(upd_qry, (oid,))
                    conn.commit()
                    upd_qry = 'DELETE FROM payment WHERE orderid = ?'
                    cursor.execute(upd_qry, (oid,))
                    conn.commit()
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

    def delete_customer(self, userid):
        message = ''
        status = 0
        data = None

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            self.clear_book_cart(userid)
            self.clear_orders(userid)
            cursor = conn.cursor()
            upd_qry = 'DELETE FROM address WHERE userid = ?'
            cursor.execute(upd_qry, (userid,))
            conn.commit()
            upd_qry = 'DELETE FROM user WHERE userid = ?'
            cursor.execute(upd_qry, (userid,))
            conn.commit()
            status = 1
            message = 'Data Updated Successfully!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg

    def admin_update_password(self, adid, old, new):
        message = ''
        status = 0

        conn = sqlite3.connect(self.__db)
        cursor = conn.cursor()

        try:
            check_qry = 'SELECT password FROM admin WHERE adminid = ?'
            cursor.execute(check_qry, (adid,))
            row = cursor.fetchone()
            if row:
                raw = row[0]
                match_val = cryptocode.decrypt(raw, self.__hash)
                if old == match_val:
                    password = cryptocode.encrypt(new, self.__hash)
                    add_qry = 'UPDATE admin SET password = ? WHERE adminid = ?'
                    cursor.execute(add_qry, (password, adid,))
                    conn.commit()
                    status = 1
                    message = 'Password Updated Successfully!'
                else:
                    status = 0
                    message = f'Password Not Matched!'
        except sqlite3.Error as e:
            status = -1
            message = f'Error Occured!\n{e}'
        finally:
            conn.close()

        msg = [status, message]

        return msg
