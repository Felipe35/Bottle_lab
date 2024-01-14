from bottle import route, run, request, template, static_file, response, redirect
import db_stuff
import datetime
import hashlib
import uuid

@route('/views/static/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='./views/static')

@route('/views/static/images/<picture>')
def serve_pictures_img(picture):
    return static_file(picture, root='./views/static/images')


@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='./views/static')




@route('/', method='GET')
def log():
    return template('log')



@route('/', method='POST')
def post_log():

    name = request.forms.get('name')
    password = request.forms.get('pass')

    pw = password.encode('utf-8')
    pw = hashlib.sha1(pw).hexdigest() 

    obj = db_stuff.DataBase_Client()
    admin_credentials = obj.check_user_credentials(name, pw)

    if len(name) > 0 and len(pw) > 0 and admin_credentials == True:

        cookie_val = str(uuid.uuid4())
        response.set_cookie('COOKIE', cookie_val)

        data = {'name': name, 'bienvenido': 'Bienvenido'}

        return template('index', data)
    else:
        data = {'log_fail': 'Contrasena y Usuario son incorrectos'}
        return template('log', data)









@route('/home', method='GET')
def post_clients():
    if not request.get_cookie('COOKIE'):
        redirect('/')
    return template('index')


@route('/show_client', method='GET')
def get_client_info():
    if not request.get_cookie('COOKIE'):
        redirect('/')
    return template('search_client')


@route('/show_client', method='POST')
def post_client_info():
    # file_name = request.forms.get('file')
    full_name = request.forms.get('full_name')
    obj = db_stuff.DataBase_Client()
    # name = obj.get_full_name(full_name=full_name)
    client_exists = obj.check_user_exists((full_name,))
    # (unp_name,) = name
    # print(name)
    

    if len(full_name) == 0:
        data = {'blank': 'Por favor ingresa un nombre'}
        return template('search_client', data)
    # file_name = request.forms.get('file_name')
    # elif client_exists == '':
    #     data = {'asd': full_name}
    #     return template('search_client', data)
    elif client_exists == []:
        data = {'no_exists': full_name}
        return template('search_client', data)
    
    elif client_exists:
        obj = db_stuff.DataBase_Client()
        rows = obj.display_table(full_name=full_name)
        # un_pack_tuple = [s for t in rows for s in t]

        data = {'rows': rows}
        return template('search_client', data)
    
    else:
        return template('search_client')


@route('/show_file', method='POST')
def post_client_file():
    file_name = request.forms.get('file_name')
    # obj_file = db_stuff.
    if len(file_name) == 0:

        data = {'no_file': 'Por favor ingrese nombre de archivo'}

        return template('show_file', data)
    else:
        data = {'file': file_name}

        return template('show_file', data)


@route('/add_new_file', method='GET')
def add_new_file():
    if not request.get_cookie('COOKIE'):
        redirect('/')
    return template('add_new_file')


@route('/add_new_file', method='POST')
def post_add_new_file():
    full_name = request.forms.get('full_name').lower()
    file = request.forms.get('file_name')
    print(len(file))
    obj = db_stuff.DataBase_Client()
    client_exist = obj.check_user_exists((full_name,))
    print(client_exist == [(full_name,)] and len(file) > 0)
   

    
    if client_exist == [] and len(file) == 0:
        print(file + 'if')
        data_file = {'blank': 'Por favor ingrese nombre y archivo del cliente'}
        return template('add_new_file', data_file)
    
    elif client_exist == [] and len(file) == 0:
        print(file + '1 elif')
        client = {'no_exists': full_name}
        return template('add_new_file', client)
    
    elif client_exist == [(full_name,)] and len(file) == 0:
        data = {'only_name_exists': full_name}
        return template('add_new_file', data)
    
    elif (client_exist == [(full_name, )]) and (len(file) > 0):
        print(file + '2 elif')
        row = obj.get_client_id(full_name=full_name)
        (c_id, ) = row
        db_file = db_stuff.File_Master()
        file_status = db_file.get_file(file=file, c_id=c_id)
        rows = obj.display_table(full_name=full_name)
        # for x in obj_file.load_directory():
        #     if file in x:
        #         with open(f"E:\E_Documents\Documents\Project Carlos\media\{x}", "rb") as f:
        #             data = f.read()
        #             obj_file.insert_file(file_name=x, file_data=data, client_id=c_id)
        #             print("{} Added to data base".format(x))
                
        data_file = {'file_status': file_status, 'full_name': full_name}

        return template('add_new_file', data_file)


    else:
        print(file)
        return template('add_new_file')
        # check = full_name == ''
    # if check:
    #     data = {'full_name': full_name}
    #     return template('show_client', data)
    # else:
    #     data = {'full_name': full_name}

    #     return template('show_file', data)


@route('/add_client', method='GET')
def display_add_client():
    if not request.get_cookie('COOKIE'):
        redirect('/')
    return template('add_client')


@route('/add_client', method='POST')
def add_client():
  
    cur_date = datetime.datetime.now()
    records = []
    db_file = db_stuff.File_Master()
    clean = db_stuff.Clean_Format()
    
    file = request.forms.get('file')
    full_name = request.forms.get('full_name')
    age = request.forms.get('age')
    date = cur_date.strftime("%A %B %m, %Y: %H:%M")
    first_phone = request.forms.get('first_phone')
    second_phone = request.forms.get('second_phone')
    address = request.forms.get('address')
    f_phone_format = clean.phone_format(first_phone)
    s_phone_format = clean.phone_format(second_phone)
  
    
    check = full_name == '' or age == '' or address == '' or first_phone == '' or date == '' or file == ''
    # print(file + 'before if')
    if check:
        
        # print(file + 'in if')
        return template('add_client')

    else:
        obj = db_stuff.DataBase_Client()

        records.append(None)
        records.append(request.forms.get('full_name').lower())
        records.append(request.forms.get('age'))
        records.append(date)
        records.append(f_phone_format)
        records.append(s_phone_format)
        records.append(request.forms.get('address').lower())

        obj.insert_user(records)
        
        id = obj.get_user_id(full_name)
        (un_id,) = id
        # print(id_obj, id, file)
        # obj.insert_phone(phone=phone.lower())
        # obj.insert_address(address=address.lower())
        # obj.insert_user(name=full_name.lower(), age=age, date=date)
        db_file = db_stuff.File_Master()
        client_file = db_file.get_file(file=file, c_id=un_id)

        # for x in obj_file.load_directory():
        #     # print(x + 'this is x in the for')
        #     # id = obj.get_user_id(full_name)
        #     if file in x:
        #         with open(f"E:\E_Documents\Documents\Project Carlos\media\{x}", "rb") as f:
                    
        #             data = f.read()
        #             obj_file.insert_file(file_name=x, file_data=data, client_id=un_id)
        #             print("{} Added to data base".format(x))
            
        data_file = {'file_status': client_file, 'full_name': full_name}
        # print(file + 'in else')
        return template('add_client', data_file)
            

# @route('/show_client_id_name', method='GET')
# def get_cliente_update():

#     return template('update_client')


@route('/show_client_id_name', method='POST')
def show_client_to_post():

    
    full_name = request.forms.get('name')
    obj = db_stuff.DataBase_Client()
    rows = obj.get_full_name(full_name=full_name)
    client_exist = obj.check_user_exists((full_name,))

    if client_exist == []:
        data = {'no_exists': full_name}
        return template('update_client', data)

    elif [(full_name, )] == client_exist:
        
        data = {'rows': rows}
        return template('update_client', data)
    
    else:
        data_msn = {'msn_one': 'Por favor ingrese nombre del cliente'}
        return template('update_client', data_msn)
    

@route('/update_client', method='GET')
def get_cliente_update():
    if not request.get_cookie('COOKIE'):
        redirect('/')
    return template('update_client')


@route('/update_client', method='POST')
def post_update_client_info():
    clean = db_stuff.Clean_Format()

    records = []

    client_id = request.forms.get('client_id')
    full_name = request.forms.get('full_name')
    f_phone = request.forms.get('first_phone')
    s_phone = request.forms.get('second_phone')
    address = request.forms.get('address')
    f_phone_format = clean.phone_format(f_phone)
    s_phone_format = clean.phone_format(s_phone)

    # no_check = full_name == '' or f_phone == '' or s_phone == '' or address == '' or client_id == ''
    
    

    # are_entries_empty = full_name != '' and f_phone != '' and s_phone != '' and address != '' and client_id != ''
    are_entries_empty = len(full_name) == 0 and len(f_phone) == 0 and len(s_phone) == 0 and len(address) == 0
    print(are_entries_empty)

    if are_entries_empty == False:
    
        records.append(request.forms.get('full_name').lower())
        records.append(f_phone_format)
        records.append(s_phone_format)
        records.append(request.forms.get('address').lower())
        records.append(request.forms.get('client_id'))
        obj = db_stuff.DataBase_Client()
        obj.update_client(records=records)
        update = obj.update_display(cliend_id=client_id)

        # check_records = records == []

        data_succes = {'update': update, 'full_name': full_name, 'f_phone': f_phone, 's_phone': s_phone, 'address': address, 'c_id': client_id}
        print('data success')
        return template('update_detail', data_succes)
      

    else:
        # data = {'full_name': full_name, 'f_phone': f_phone, 's_phone':s_phone, 'address': address}
        data = {'fail_update': 'Por favor ingresar datos'}
        print('no succes')
        return template('update_detail', data)
        


@route('/show_client_delete', method='GET')
def get_delete():
    if not request.get_cookie('COOKIE'):
        redirect('/')
    return template('delete_client')


@route('/show_client_delete', method='POST')
def show_client_delete():
    full_name = request.forms.get('full_name').lower()
    obj = db_stuff.DataBase_Client()
    client_exists = obj.check_user_exists((full_name,))
    rows = obj.get_full_name(full_name=full_name)

    if len(full_name) == 0:
        data = {'blank': 'Por favor ingresa un nombre'}
        return template('delete_client', data)
    # file_name = request.forms.get('file_name')
    # elif client_exists == '':
    #     data = {'asd': full_name}
    #     return template('search_client', data)
    elif client_exists == []:
        data = {'no_exists': full_name}
        return template('delete_client', data)
    
    elif client_exists:

        data = {'rows': rows}
        return template('delete_client', data)


@route('/delete_client', method='POST')
def delete_client():
    obj = db_stuff.DataBase_Client()
    client_id = request.forms.get('client_id')

    id = obj.get_id_from_db(client_id)
    

    if client_id == "" or id == False:
        data = {'fail_id': 'ID no encontrado'}

        return template('delete_client', data)
    
    elif client_id != "" and id == True:
        # SqliteStudio does not support DELETE JOINS
        obj.delete_from_client(client_id=client_id)
        obj.delete_from_results(client_id=client_id)

        data = {'delete': client_id}

        return template('delete_client', data)
    

run(host='localhost', port=8080)