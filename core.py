import datetime
import random
import pymysql
import config


def add_agent(agent_id):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"INSERT INTO agents (`agent_id`) VALUES (%s)", (agent_id,))
    con.commit()

    cur.close()
    con.close()



def add_file(req_id, file_id, file_name, type):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"INSERT INTO files (`req_id`, `file_id`, `file_name`, `type`) VALUES (%s, %s, %s, %s)", (req_id, file_id, file_name, type,))
    con.commit()

    cur.close()
    con.close()



def new_req(user_id, request):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()


    cur.execute(f"INSERT INTO requests (`user_id`, `req_status`) VALUES (%s, 'waiting')", (user_id,))


    req_id = cur.lastrowid

    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')


    cur.execute(f"INSERT INTO messages (`req_id`, `message`, `user_status`, `date`) VALUES (%s, %s, 'user', %s)", (req_id, request, date_now,))

    con.commit()

    cur.close()
    con.close()

    return req_id



def add_message(req_id, message, user_status):
    if user_status == 'user':
        req_status = 'waiting'
    elif user_status == 'agent':
        req_status = 'answered'

    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()


    cur.execute(f"INSERT INTO messages (`req_id`, `message`, `user_status`, `date`) VALUES (%s, %s, %s, %s)", (req_id, message, user_status, date_now,))


    cur.execute(f"UPDATE requests SET `req_status` = %s WHERE `req_id` = %s", (req_status, req_id))

    con.commit()

    cur.close()
    con.close()




def check_agent_status(user_id):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT * FROM agents WHERE `agent_id` = %s", (user_id,))
    agent = cur.fetchone()

    cur.close()
    con.close()

    if agent == None:
        return False
    else:
        return True




def get_file(message):
    """
    Атрибут file_name доступен только в типах файлов - document и video.
    Если пользователь отправляет не документ и не видео - в качестве имени файла передать дату и время отправки (date_now)
    """

    types = ['document', 'video', 'audio', 'voice']
    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')


    try:
        return {'file_id': message.json['photo'][-1]['file_id'], 'file_name': date_now, 'type': 'photo', 'text': str(message.caption)}


    except:
        for type in types:
            try:
                if type == 'document' or type == 'video':
                    file_name = message.json[type]['file_name']
                else:
                    file_name = date_now

                return {'file_id': message.json[type]['file_id'], 'file_name': file_name, 'type': type, 'text': str(message.caption)}
            except:
                pass

        return None



def get_icon_from_status(req_status, user_status):
    if req_status == 'confirm':
        return '✅'

    elif req_status == 'waiting':
        if user_status == 'user':
            return '⏳'
        elif user_status == 'agent':
            return '❗️'

    elif req_status == 'answered':
        if user_status == 'user':
            return '❗️'
        elif user_status == 'agent':
            return '⏳'



def get_file_text(file_name, type):
    if type == 'photo':
        return f'📷 | Фото {file_name}'
    elif type == 'document':
        return f'📄 | Документ {file_name}'
    elif type == 'video':
        return f'🎥 | Видео {file_name}'
    elif type == 'audio':
        return f'🎵 | Аудио {file_name}'
    elif type == 'voice':
        return f'🎧 | Голосовое сообщение {file_name}'




def get_user_id_of_req(req_id):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `user_id` FROM requests WHERE `req_id` = %s", (req_id,))
    user_id = cur.fetchone()[0]

    cur.close()
    con.close()

    return user_id



def get_file_id(id):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `file_id` FROM files WHERE `id` = %s", (id,))
    file_id = cur.fetchone()[0]

    cur.close()
    con.close()

    return file_id



def get_req_status(req_id):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `req_status` FROM requests WHERE `req_id` = %s", (req_id,))
    req_status = cur.fetchone()[0]

    cur.close()
    con.close()

    return req_status



def delete_agent(agent_id):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"DELETE FROM {config.db_name}.agents WHERE `agent_id` = %s", (agent_id,))
    con.commit()

    cur.close()
    con.close()



def confirm_req(req_id):
    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"UPDATE requests SET `req_status` = 'confirm' WHERE `req_id` = %s", (req_id,))
    con.commit()

    cur.close()
    con.close()




def get_agents(number):
    limit = (int(number) * 10) - 10

    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `agent_id` FROM agents LIMIT {limit}, 10")
    agents = cur.fetchall()

    cur.close()
    con.close()

    return agents



def my_reqs(number, user_id):
    limit = (int(number) * 10) - 10

    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `req_id`, `req_status` FROM requests WHERE `user_id` = %s ORDER BY `req_id` DESC LIMIT {limit}, 10", (user_id,))
    reqs = cur.fetchall()

    cur.close()
    con.close()

    return reqs



def get_reqs(number, callback):
    limit = (int(number) * 10) - 10
    req_status = callback.replace('_reqs', '')

    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `req_id`, `req_status` FROM requests WHERE `req_status` = %s ORDER BY `req_id` DESC LIMIT {limit}, 10", (req_status,))
    reqs = cur.fetchall()

    cur.close()
    con.close()

    return reqs

def get_files(number, req_id):
    limit = (int(number) * 10) - 10

    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `id`, `file_name`, `type` FROM files WHERE `req_id` = %s ORDER BY `id` DESC LIMIT {limit}, 10", (req_id,))
    files = cur.fetchall()

    cur.close()
    con.close()

    return files



def get_request_data(req_id, callback):
    if 'my_reqs' in callback:
        get_dialog_user_status = 'user'
    else:
        get_dialog_user_status = 'agent'

    con = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cur = con.cursor()

    cur.execute(f"SELECT `message`, `user_status`, `date` FROM messages WHERE `req_id` = %s", (req_id,))
    messages = cur.fetchall()

    cur.close()
    con.close()

    data = []
    text = ''
    i = 1

    for message in messages:
        message_value = message[0]
        user_status = message[1]
        date = message[2]

        if user_status == 'user':
            if get_dialog_user_status == 'user':
                text_status = '👤 Ваше сообщение'
            else:
                text_status = '👤 Сообщение пользователя'
        elif user_status == 'agent':
            text_status = '🧑‍💻 Агент поддержки'


        backup_text = text
        text += f'{text_status}\n{date}\n{message_value}\n\n'


        if len(text) >= 4096:
            data.append(backup_text)
            text = f'{text_status}\n{date}\n{message_value}\n\n'


        if len(messages) == i:
            if len(text) >= 4096:
                data.append(backup_text)
                text = f'{text_status}\n{date}\n{message_value}\n\n'

            data.append(text)

        i += 1

    return data
