from telethon import Button
from telethon.sync import TelegramClient, events, functions, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio,re,random,time,hashlib,uuid,json
from datetime import datetime, timedelta
from mysql.connector import pooling
import json
import asyncio
import io

api_id = 114514
api_hash = 'eeeeeeeeeeeeeeeeeeeeeeeeeeee'
bot_token = '2333333:fffffffffffffffffffffffffffff'
client = TelegramClient('subticket', api_id, api_hash).start(bot_token=bot_token)

admin = [10000,100001]
dbconfig = {
    "host": "127.0.0.1",
    "user": "subticket",
    "password": "qweasdzxc123",
    "database": "subticket"
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool",pool_size=5,**dbconfig)

def admin_act(act, data):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Error: {e}")
        return False
    if act == "read_groups":
        try:
            sql = "SELECT * FROM `groups`"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Error: {e}")
            return False
    if act == "add_groups":
        try:
            sql = "SELECT * FROM `groups` WHERE group_id = %s"
            cursor.execute(sql, (data["group_id"],))
            # if group exists, return False else create group
            if cursor.fetchone():
                return False
            else:
                sql = "INSERT INTO `groups` (group_id, group_name) VALUES (%s, %s)"
                cursor.execute(sql, (data["group_id"], data["group_name"]))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True
    elif act == "edit_group":
        try:
            sql = "UPDATE `groups` SET group_name = %s ,group_id = %s WHERE id = %s"
            cursor.execute(sql, (data["group_name"], data["group_id"], data["id"]))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True
    elif act == "del_group":
        try:
            sql = "DELETE FROM `groups` WHERE id = %s"
            cursor.execute(sql, (data["id"],))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

def update_group_users(group_id, users):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Error: {e}")
        return False
    try:
        sql = "UPDATE `groups` SET users = %s WHERE group_id = %s"
        cursor.execute(sql, (users, group_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

def read_group_users(group_id):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Error: {e}")
        return False
    try:
        sql = "SELECT users FROM `groups` WHERE group_id = %s"
        cursor.execute(sql, (group_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if not result:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    return result["users"]

def create_ticket(user_id, user_name, nickname, ticket_key):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Error: {e}")
        result = False
    try:
        sql = "INSERT INTO `tickets` (user_id, user_name, nickname, ticket_key) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, user_name, nickname, ticket_key))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

def read_ticket(ticket, remove = False):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Error: {e}")
        result = False
    if "key" in ticket:
        try:
            sql = "SELECT * FROM `tickets` WHERE ticket_key = %s limit 1"
            cursor.execute(sql, (ticket["key"],))
            result = cursor.fetchone()
            if not result:
                result = False
            if remove:
                sql = "DELETE FROM `tickets` WHERE ticket_key = %s"
                cursor.execute(sql, (ticket["key"],))
                conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            result = False
    elif "user_id" in ticket:
        try:
            sql = "SELECT * FROM `tickets` WHERE user_id = %s limit 1"
            cursor.execute(sql, (ticket["user_id"],))
            result = cursor.fetchone()
            if not result:
                result = False
            if remove:
                sql = "DELETE FROM `tickets` WHERE user_id = %s"
                cursor.execute(sql, (ticket["user_id"],))
                conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            result = False
    cursor.close()
    conn.close()
    return result

def link_acts(act, data):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Error: {e}")
        result = False
    if act == "create_link" and data:
        try:
            sql = "INSERT INTO `links` (link, source, dest, exp) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql,(data["link"], data["source"], data["dest"], data["exp"]))
            conn.commit()
            cursor.close()
            conn.close()
            result = True
        except Exception as e:
            print(f"Error: {e}")
            result = False
        return result
    if act == "read_link":
        try:
            if data:
                sql = "SELECT * FROM `links` WHERE link = %s"
                cursor.execute(sql, (data["link"], ))
                result = cursor.fetchone()
            else:
                sql = "SELECT * FROM `links`"
                cursor.execute(sql)
                result = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")
            result = False
        return result
    if act == "del_link" and data:
        try:
            sql = "DELETE FROM `links` WHERE id = %s"
            cursor.execute(sql, (data["id"],))
            conn.commit()
            cursor.close()
            conn.close()
            result = True
        except Exception as e:
            print(f"Error: {e}")
            result = False
        return result
    if act == "mod_exp" and data:
        try:
            sql = "UPDATE `links` SET exp = %s WHERE link = %s"
            cursor.execute(sql, (data["exp"], data["link"]))
            conn.commit()
            cursor.close()
            conn.close()
            result = True
        except Exception as e:
            print(f"Error: {e}")
            result = False
        return result
    if act == "add_request" and data:
        try:
            sql = "UPDATE `links` SET requests = %s WHERE link = %s"
            cursor.execute(sql, (data["requests"], data["link"]))
            conn.commit()
            cursor.close()
            conn.close()
            result = True
        except Exception as e:
            print(f"Error: {e}")
            result = False
        return result

async def log_worker(new_user, new_id, old_user, old_id, nickname, group_name, group_id):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Error: {e}")
        return
    try:
        time_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO `log` (time, new_id, old_id, group_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (time_now, new_id, old_id, group_id))
        conn.commit()
        cursor.close()
        conn.close()
        for user in admin:
            await client.send_message(user, f"新账号 [{new_user}] (ID:{new_id}) 通过原账号 [{old_user}, 昵称:{nickname}] (ID:{old_id}) 的车票申请了返回群组 [{group_name}] (ID:{group_id})")
    except Exception as e:
        print(f"Error: {e}")
        return
    return True

async def create_invite_links(group_id, user_id):
        exp = datetime.now() + timedelta(days=3)
        try:
            result = await client(functions.messages.ExportChatInviteRequest(
                peer=int(group_id),
                title=str(user_id),
                expire_date=exp,
                usage_limit=1
            ))
            invite_link = result.link
            return invite_link
        except Exception as e:
            print(f"Error: {e}")
            return False

async def link_process(event):
    chat_id = event.chat_id
    sender = await event.get_sender()
    sender_id = event.sender_id
    try:
        link = event.raw_text.split("link-")[1]
        result = link_acts("read_link", {"link": link})
    except Exception as e:
        print(f"Error1: {e}")
        return
    if not result:
        return
    try:
        source_users = read_group_users(result["source"])
        if source_users:
            source_users = json.loads(source_users)
        else:
            await client.send_message(chat_id, '旧群组用户列表获取失败，添加群组后请等待至少6分钟')
            return
        if str(sender_id) not in source_users:
            await client.send_message(chat_id, '您不是旧群组成员，无法申请加入新群组')
            return
    except Exception as e:
        print(f"Error2: {e}")
        return
    if result["exp"] < datetime.now():
        await client.send_message(chat_id, '链接已过期，请联系旧群组管理员重新申请')
        return
    if result["requests"]:
        reqs = json.loads(result["requests"])
    else:
        reqs = {}
    if str(sender_id) in reqs:
        await client.send_message(chat_id, '您已提交过进群申请，每人仅限一次')
        return
    try:
        reqs[str(sender_id)] = sender.username
        reqs = json.dumps(reqs, ensure_ascii=False)
        reqs_result = link_acts("add_request", {"link": link, "requests": reqs})
        if reqs_result:
            invite_link = await create_invite_links(result["dest"], sender_id)
            await client.send_message(chat_id, f'请点击链接加入新群组：{invite_link}')
    except Exception as e:
        print(f"Error3: {e}")
        await client.send_message(chat_id, '加入新群组失败，请联系旧群组管理员')

@client.on(events.NewMessage(pattern='/start|/help'))
async def start(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if event.raw_text.find("link-") != -1:
        await link_process(event)
        return
    content = '欢迎使用车票机器人，以下是可用的命令：'
    if sender_id in admin:
        content += '\n\n/show_groups - 查看已配置的群组\n/add_group - 添加群组\n/del_group - 删除群组\n/edit_group - 编辑群组\n/show_users - 查看群组用户'
    content += '\n\n/get_ticket - 生成车票\n/use_ticket - 使用车票'
    try:
        await client.send_message(chat_id, content)
    except Exception as e:
        print(f"Error: {e}")
        return

@client.on(events.NewMessage(pattern='/get_ticket'))
async def get_ticket(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    ticket = hashlib.shake_128()
    check_user = read_ticket({"user_id": sender_id})
    if check_user:
        content = '你已经拥有一张车票了：' + check_user["ticket_key"]
        await client.send_message(chat_id, content)
        return
    pre_ticket = str(chat_id) + str(sender_id) + str(time.time()) + str(uuid.uuid4())
    ticket.update(pre_ticket.encode('utf-8'))
    ticket = ticket.hexdigest(20)
    if not sender.username:
        await client.send_message(chat_id, '请先设置你的用户名')
        return
    if create_ticket(sender_id, sender.username, str(sender.first_name) + str(sender.last_name), ticket):
        content = '请将这条消息复制在其他地方妥善保存\n车票: `' + ticket + '`'
        content += '\n销号后可凭车票快速上车，核销依顺序联系：@subticketbot @subticket2bot'
        content += '\n\n请不要将车票泄露给其他人，否则你可能无法上车。'
        await client.send_message(chat_id, content)

@client.on(events.NewMessage(pattern=r'/use_ticket.*?'))
async def use_ticket(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    try:
        ticket = re.search(r'/use_ticket\s+([a-fA-F0-9]{40})', event.raw_text).group(0)
        ticket = ticket.split(" ")[1]
    except Exception as e:
        await client.send_message(chat_id, '请使用 "`/use_ticket` 车票" 核销车票，注意空格')
        return
    print(ticket)
    result = read_ticket({"key": ticket})
    if result:
        old_user = result["user_name"]
        old_id = result["user_id"]
        nickname = result["nickname"]
    else:
        return
    groups = admin_act("read_groups", {})
    for group in groups:
        try:
            current_users = await client.get_participants(int(group["group_id"]))
        except Exception as e:
            print(f"Error: {e}")
            continue
        if str(old_id) not in json.loads(group["users"]):
            return
        for user in current_users:
            if old_id == user.id and not user.deleted:
                return
        try:
            await log_worker(sender.username, sender_id, old_user, old_id, nickname, group["group_name"], group["group_id"])
            invite_link = await create_invite_links(group["group_id"], sender_id)
            content = '车票已核销，欢迎上车：' + str(invite_link)
            await client.send_message(chat_id, content)
            read_ticket({"key": ticket}, True)
        except Exception as e:
            print(f"Error: {e}")
            return

@client.on(events.NewMessage(pattern='/show_groups'))
async def show_groups(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    result = admin_act("read_groups", {})
    if result:
        content = '已配置的群组：'
        for r in result:
            content += '\n' + '序号: `' + str(r["id"]) + '` 群组名: [`' + r["group_name"] + '`] (ID: `' + str(r["group_id"]) + '` )'
        await client.send_message(chat_id, content)
    else:
        await client.send_message(chat_id, '暂无已配置的群组，请使用 "`/add_group` 群组名 群组ID" 添加群组，注意空格，名称不可包含符号、表情、空格')

@client.on(events.NewMessage(pattern='/add_group.*?'))
async def add_group(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    try:
        group = re.search(r'/add_group\s+([\u4e00-\u9fa5_a-zA-Z0-9]+)\s+(-?\d+)', event.raw_text).group(0)
    except Exception as e:
        await client.send_message(chat_id, '请使用 "`/add_group` 群组名 群组ID" 添加群组，注意空格，名称不可包含符号、表情、空格')
        return
    group_name = group.split(" ")[1]
    group_id = int(group.split(" ")[2])
    # check if bot in group and is admin
    try:
        bot = await client.get_entity(group_id)
    except Exception as e:
        await client.send_message(chat_id, '群组不存在或机器人未加入该群组，请重试')
        return
    if not bot.admin_rights:
        await client.send_message(chat_id, '机器人不是群组管理员，请重试')
        return
    # check if group already exists
    result = admin_act("read_groups", {})
    if result:
        for r in result:
            if r["group_id"] == group_id:
                await client.send_message(chat_id, '群组已添加过，请重试')
                return
    # add group
    result = admin_act("add_groups", {"group_id": group_id, "group_name": group_name})
    if result:
        await client.send_message(chat_id, '群组添加成功')
    else:
        await client.send_message(chat_id, '群组添加失败，可能已存在该群组')

@client.on(events.NewMessage(pattern='/del_group.*?'))
async def del_group(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    try:
        id = re.search(r'/del_group\s+(\d+)', event.raw_text).group(0)
    except Exception as e:
        await client.send_message(chat_id, '请使用 "`/del_group` 序号" 删除群组，注意空格')
        return
    # check if group exists
    id = int(id.split(" ")[1])
    result = admin_act("read_groups", {})
    if result:
        for r in result:
            if r["id"] == id:
                result = admin_act("del_group", {"id": r["id"]})
                if result:
                    await client.send_message(chat_id, '群组删除成功')
                else:
                    await client.send_message(chat_id, '群组删除失败')
                return
    await client.send_message(chat_id, '群组不存在，请重试')

@client.on(events.NewMessage(pattern='/edit_group.*?'))
async def edit_group(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    try:
        group = re.search(r'/edit_group\s+(\d+)\s+([\u4e00-\u9fa5_a-zA-Z0-9]+)\s+(-?\d+)', event.raw_text).group(0)
    except Exception as e:
        await client.send_message(chat_id, '请使用 "`/edit_group` 序号 群组名 群组ID" 修改已添加的群组，注意空格，名称不可包含符号、表情、空格')
        return
    id = int(group.split(" ")[1])
    group_name = group.split(" ")[2]
    group_id = int(group.split(" ")[3])
    # check if group exists
    result = admin_act("read_groups", {})
    if result:
        for r in result:
            if r["id"] == id:
                result = admin_act("edit_group", {"id": r["id"], "group_id": group_id, "group_name": group_name})
                if result:
                    await client.send_message(chat_id, '群组编辑成功')
                else:
                    await client.send_message(chat_id, '群组编辑失败')
                return
    await client.send_message(chat_id, '群组不存在，请重试')

@client.on(events.NewMessage(pattern='/show_users'))
async def show_users(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    try:
        groups = admin_act("read_groups", {})
        if groups:
        # create an empty dict to store the users from each group, make a for loop to get the users from each group, then convert the dict to json and send it to the chat_id as a file
            users = {}
            for group in groups:
                users[group["group_name"] + "/" + group["group_id"]] = group["users"]
            users = json.dumps(users, ensure_ascii=False).replace("\\","")
            users = io.BytesIO(users.encode('utf-8'))
            users.name = "users.json"
            await client.send_file(chat_id, users, caption="群组用户列表")
        else:
            await client.send_message(chat_id, '暂无已配置的群组，请使用 "`/add_group` 群组名 群组ID" 添加群组，注意空格，名称不可包含符号、表情、空格')
    except Exception as e:
        print(f"Error: {e}")
        await client.send_message(chat_id, '发生错误，请联系admin')

@client.on(events.NewMessage(pattern='/create_link.*?'))
async def create_link(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    try:
        create_info = re.search(r'/create_link\s+(-?\d+)\s+(-?\d+)', event.raw_text).group(0)
    except Exception as e:
        await client.send_message(chat_id, '请使用 "`/create_link` 旧群组序号 新群组序号" 创建群组链接，注意空格\n群组序号可使用 /show_groups 查看')
        return
    old_group_id = int(create_info.split(" ")[1])
    new_group_id = int(create_info.split(" ")[2])
    try:
        groups = admin_act("read_groups", {})
        if groups:
            for group in groups:
                if group["id"] == old_group_id:
                    old_group = group["group_id"]
                if group["id"] == new_group_id:
                    new_group = group["group_id"]
        if not old_group or not new_group:
            await client.send_message(chat_id, '群组序号不存在，请重试')
            return
    except Exception as e:
        print(f"Error: {e}")
        await client.send_message(chat_id, '群组序号不存在，请重试')
        return
    exp = datetime.now() + timedelta(days=30)
    exp = datetime.strftime(exp, "%Y-%m-%d %H:%M:%S")
    link = hashlib.shake_128()
    pre_key = str(old_group) + str(new_group) + str(time.time()) + str(uuid.uuid4())
    link.update(pre_key.encode('utf-8'))
    link = link.hexdigest(10)
    result = link_acts("create_link", {"link": link, "source": old_group, "dest": new_group, "exp": exp})
    if not result:
        await client.send_message(chat_id, '创建链接失败，请联系admin')
    else:
        content = "群组链接创建成功：`https://t.me/subticketbot?start=link-" + link + "` ，旧群组中的所有成员可以使用此链接申请加入新群组，默认有效期为30天，点击下方按钮可修改有效期"
        buttons = [
            [Button.inline("7天有效", f"modlinkexp?link={link}&exp=7"),
             Button.inline("15天有效", f"modlinkexp?link={link}&exp=15"),
             Button.inline("60天有效", f"modlinkexp?link={link}&exp=60"),
             Button.inline("90天有效", f"modlinkexp?link={link}&exp=90")]
        ]
        await client.send_message(chat_id, content, buttons=buttons)

@client.on(events.NewMessage(pattern='/show_links'))
async def show_links(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    try:
        links = link_acts("read_link", {})
        if links:
            content = "已创建的群组链接：\n"
            for link in links:
                content += f"链接序号： {link['id']} , 链接: {link['link']} , 旧群组: {link['source']} , 新群组: {link['dest']} , 有效期: {link['exp']}\n"
            file = io.BytesIO(content.encode('utf-8'))
            file.name = "links.txt"
            await client.send_file(chat_id, file, caption="已创建的群组链接")
        else:
            await client.send_message(chat_id, '暂无已创建的群组链接，请使用 "`/create_link` 旧群组序号 新群组序号" 创建群组链接，注意空格\n群组序号可使用 /show_groups 查看')
    except Exception as e:
        print(f"Error: {e}")
        await client.send_message(chat_id, '发生错误，请联系admin')

@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode('utf-8')
    if data.startswith("modlinkexp"):
        try:
            link = re.search(r'link=([\w-]+)', data).group(0).split("=")[1]
            exp = re.search(r'exp=(\d+)', data).group(0).split("=")[1]
            exp = datetime.now() + timedelta(days=int(exp))
            exp = datetime.strftime(exp, "%Y-%m-%d %H:%M:%S")
            result = link_acts("mod_exp", {"exp": exp, "link": link})
        except Exception as e:
            print(f"Error: {e}")
            await client.send_message(event.chat_id, "出现错误，请联系admin")
            return
        if result:
            await client.send_message(event.chat_id, "链接有效期成功修改为：" + exp)
        else:
            await client.send_message(event.chat_id, "链接不存在，请联系admin")

@client.on(events.NewMessage(pattern='/del_link.*?'))
async def del_link(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if sender_id not in admin:
        return
    try:
        id = re.search(r'/del_link\s+([\w-]+)', event.raw_text).group(0).split(" ")[1]
    except Exception as e:
        await client.send_message(chat_id, '请使用 "`/del_link` 链接序号" 删除群组链接，注意空格\n链接序号可使用 /show_links 查看')
        return
    result = link_acts("del_link", {"id": id})
    if result:
        await client.send_message(chat_id, '群组链接删除成功')
    else:
        await client.send_message(chat_id, '群组链接不存在，链接序号不会小于100000，请勿与群组序号混淆')

async def get_group_users():
    groups = admin_act("read_groups", {})
    for group in groups:
        try:
            users = await client.get_participants(int(group["group_id"]))
        except Exception as e:
            print(f"Error: {e}")
            continue
        if not users:
            continue
        users_from_db = read_group_users(group["group_id"])
        if users_from_db:
            users_from_db = json.loads(users_from_db)
            for user in users:
                users_from_db[str(user.id)] = user.username
            users_from_db = json.dumps(users_from_db,ensure_ascii=False)
            update_group_users(group["group_id"], users_from_db)
        else:
            user_list = {}
            for user in users:
                user_list[user.id] = user.username
            user_list = json.dumps(user_list,ensure_ascii=False)
            update_group_users(group["group_id"], user_list)

#run get_group_users every 6 minutes using APScheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(get_group_users, 'interval', minutes=6)
scheduler.start()

client.start()
client.run_until_disconnected()