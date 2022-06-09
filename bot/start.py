from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os, shutil, config
from shutil import make_archive
import math
from random import randint
from time import sleep
from datetime import datetime, timedelta
import pytz
import string, random
from string import digits

IST = pytz.timezone('Asia/Kolkata')

users = config.USERS.split(" ")
LINK_CHAT = int(config.LINK_CHAT)
ZIP_CHAT = int(config.ZIP_CHAT)
FILES_CHAT = int(config.FILES_CHAT)
NAMES_CHAT = int(config.NAMES_CHAT)
NAMES_TEXT_CHAT = int(config.NAMES_TEXT_CHAT)


def get_human_size(num):
    base = 1024.0
    sufix_list = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    for unit in sufix_list:
        if abs(num) < base:
            return f"{round(num, 2)} {unit}"
        num /= base


def check_repeating(x):
    _size = len(x)
    dict = {}
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in dict:
                dict[x[i]] = f'{[o + 1 for o, p in enumerate(x) if p == x[i]]}'
        ls = '\n'.join(
            [list(dict.keys())[i] + ' at ' + list(dict.values())[i] for i in range(len(list(dict.values())))])
    return ls


async def dict_gen(name_check, text, client, message, from_id_channel):
    if not name_check.startswith('https://') or name_check.startswith('\n'):
        text = text.replace(f"https://t.me/c/{from_id_channel}/", "").replace("\n\n", ";").replace("\n", ";")
        resolved_list = text.split(';')
        name = resolved_list[-1]
        ids_list = resolved_list[:-1]
        ids_count = len(ids_list)
        refer = "-100" + from_id_channel
        name = name.upper()
        ongoing_dict_read = open('ongoing_dict.txt', 'r')
        ongoing_dict = ongoing_dict_read.read()
        ongoing_dict_read.close()
        x = eval(ongoing_dict)
        for i in range(len(list(x.values()))):
            pre_ids = eval(list(x.values())[i][1])
            diff = set(ids_list) - set(pre_ids)
            res = set(ids_list) - diff
            if len(res) != 0:
                await client.send_message(chat_id=message.chat.id,
                                          text=f'⚠️ Some Classes Are Already Present⚠️\n\n{str(repr(list(res)))}')
                return
        check_result = check_repeating(ids_list)
        if check_result != '':
            await client.send_message(chat_id=message.chat.id, text=f'⚠️ Reapeating Found ⚠️\n\n{str(check_result)}')
            return
        elif check_result == '':
            await client.send_message(chat_id=message.chat.id, text=f'✅ No Reapeating Found ✅')
            await client.send_message(chat_id=message.chat.id,
                                      text='From_Channel= ' + refer + '\n\nFolder_Name= ' + name + '\n\n' + str(
                                          ids_count) + '  Classes')

            new_dict = "{'" + name + "': ('" + refer + "', " '"' + repr(ids_list) + '")}'
            y = eval(new_dict)
            x.update(y)
            final_write = open("ongoing_dict.txt", "w")
            final_write.write(repr(x))
            final_write.close()

    else:
        text = text.replace(f"https://t.me/c/{from_id_channel}/", "").replace("\n\n", ";").replace("\n", ";")
        ids_list = text.split(';')
        count_ids = len(ids_list)
        await client.send_message(chat_id=message.chat.id,
                                  text='Please Give "callbackto" or Invalid Links \n\n' + str(count_ids) + '  Classes')



@Client.on_message(filters.command("zip"))
async def zipdata(client, message):
    try:
        if not os.path.isdir('./ZIP_DATA/'):
            os.mkdir('./ZIP_DATA/')
        make_archive(f'./ZIP_DATA/NAMES', 'zip', './NAMES')
        make_archive(f'./ZIP_DATA/ARCHIVES', 'zip', './ARCHIVES')
        make_archive(f'./ZIP_DATA/BACKUP', 'zip', './BACKUP')
        make_archive(f'./ZIP_DATA/NAMES_ARCHIVES', 'zip', './NAMES_ARCHIVES')
        make_archive(f'./ALL_DATA', 'zip', './ZIP_DATA')
        await client.send_document(chat_id=message.chat.id, document=f"ALL_DATA.zip")
    except:
        await client.send_message(chat_id=message.chat.id,
                                  text=f'ERROR ❗')

@Client.on_message(filters.command("dict"))
async def senddicts(client, message):
    await client.send_document(chat_id=message.chat.id, document=f"ongoing_dict.txt")



@Client.on_message(filters.command("clear"))
async def cleardicts(client, message):
    await client.send_document(chat_id=message.chat.id, document=f"ongoing_dict.txt")
    final_write2 = open("ongoing_dict.txt", "w")
    final_write2.write("{}")
    final_write2.close()
    await client.send_document(chat_id=message.chat.id, document=f"ongoing_dict.txt")



@Client.on_message(filters.command("upload"))
async def uploadtobot(client, message):
    file_id = int(message.reply_to_message_id)
    chat_id = message.chat.id
    m = await client.get_messages(chat_id, file_id, replies=0)
    DEFAULT_DOWNLOAD_DIR = "./"
    path = await client.download_media(m, DEFAULT_DOWNLOAD_DIR)
    await client.send_message(chat_id=message.chat.id,
                              text=f'Successfully Uploaded')


@Client.on_message(filters.command([f"send"]))
async def forward(client, message):
    if len(message.command) > 1:
        CALL_FROM = ' '.join([message.command[i] for i in range(1, len(message.command))])
        ongoing_dict_open = open('ongoing_dict.txt', 'r')
        ongoing_dict_read = ongoing_dict_open.read()
        ongoing_dict = eval(str(ongoing_dict_read))
        ongoing_dict_keys_list = list(ongoing_dict.keys())
        ongoing_dict_values_list = list(ongoing_dict.values())
        if not os.path.isdir('./BACKUP/'):
            os.mkdir('./BACKUP/')
        classes_count = 0
        for i in range(len(ongoing_dict_keys_list)):
            classes_count = classes_count + len(eval(ongoing_dict_values_list[i][1]))
        TO_ID = int(config.CHAT)
        msgx = await client.send_message(chat_id=message.chat.id,
                                         text=f'Starting Bot')
        idto = ""
        FROM_ID = ""
        MSG_LIST = []
        TIMEZ = ""
        FIN_ID = ""
        BATCH_NAME = CALL_FROM.upper() + " " + str(classes_count) + " CLASSES"
        TOTL_MESSAGES = classes_count
        BOT_DICT = {f'{BATCH_NAME}': {}}
        random_string2 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        CALL_FROMX = random_string2 + '_' + CALL_FROM[:-5].lower().replace(" ", "")
        MSG_DATA_LIST = []
        MSG_DATA_LIST_NAME = []
        BAYCH_NAME_ST = f"🔶 {CALL_FROM.upper()}\n\n📎Total Classes: {str(classes_count)}\n"
        await client.send_message(chat_id=TO_ID,
                                      text=f'{str(BAYCH_NAME_ST)}')
        MSG_DATA_LIST.append(BAYCH_NAME_ST)
        MSG_DATA_LIST_NAME.append(BAYCH_NAME_ST)
        if not os.path.isdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/'):
            os.mkdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/')
        if not os.path.isdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/COPY_DICT/'):
            os.mkdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/COPY_DICT/')
        BOT_DICT_write11 = open(
            f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/COPY_DICT/COPY_DICT_{str(BATCH_NAME).replace(' ', '_')}.txt",
            "w")
        BOT_DICT_write11.write(repr(ongoing_dict))
        BOT_DICT_write11.close()
        MSG_DATA_DICT = {}
        MSG_DATA_DICT_NAME = {}
        for i in range(len(ongoing_dict_keys_list)):
            NAME = ongoing_dict_keys_list[i]
            random_string1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            refer = random_string1 + '_' + NAME[:-7].lower().replace(" ", "")
            NAME_ST = f"\n📌 [{str(i+1)}]{NAME}:"
            MSG_DATA_LIST.append(NAME_ST)
            MSG_DATA_LIST_NAME.append(NAME_ST)
            await client.send_message(chat_id=TO_ID,
                                      text=f'🔲 {NAME}')
            FROM_ID = int(ongoing_dict[ongoing_dict_keys_list[i]][0])
            MSG_LIST = eval(ongoing_dict[ongoing_dict_keys_list[i]][1])
            MSG_TO_LIST = []
            STRING_LINK = ""
            STRING_NAME = ""
            for z in range(len(MSG_LIST)):
                classes_count = classes_count - 1
                REM_MSGS = classes_count
                FIN_ID = MSG_LIST[z]
                datetime_ist = datetime.now(IST)
                TIMEZ = f"{datetime_ist.strftime('%d %B %Y, %I:%M:%S %p')}"
                zm = 7.8 * (REM_MSGS) / (60 * 60)
                hr = math.trunc(zm)
                mint = math.trunc((zm % 1) * 60)
                secs = math.trunc((((zm % 1) * 60) % 1) * 60)
                tme = f"{hr} hours {mint} minutes {secs} seconds "
                after_time = datetime_ist + timedelta(seconds=secs, minutes=mint, hours=hr)
                y_time = after_time.strftime('%I:%M:%S %p, %d %B %Y')
                await msgx.edit_text(
                    f'EST Completion Time: {str(y_time)}\nEST Remaining Time: {str(tme)}\n\nRemaining Messages: {str(REM_MSGS)}\nTrying To Copy Message\n\nMessage_ID: https://t.me/c/{str(FROM_ID)[4:]}/{str(MSG_LIST[z])}\n\nCopied_Msg_ID: https://t.me/c/{str(TO_ID)[4:]}/{idto}\n\nTime: {str(TIMEZ)}')
                sleep(randint(2, 6))
                try:
                    mdv = await client.copy_message(
                        chat_id=TO_ID,
                        from_chat_id=FROM_ID,
                        message_id=int(MSG_LIST[z]))
                    idto = str(mdv.id)
                except Exception as e:
                    await client.send_message(chat_id=message.chat.id,
                                              text=f'Remaining Messages: {str(REM_MSGS)}\nFailed To Copy Message\n\nMessage_ID : https://t.me/c/{str(FROM_ID)[4:]}/{str(MSG_LIST[z])}')
                    return
                sleep(2)
                await msgx.edit_text(
                    f'EST Completion Time: {str(y_time)}\nEST Remaining Time: {str(tme)}\n\nRemaining Messages: {str(REM_MSGS)}\nSuccessfully Copied Message\n\nFROM_ID: https://t.me/c/{str(FROM_ID)[4:]}/{str(MSG_LIST[z])}\n\nTO_ID: https://t.me/c/{str(TO_ID)[4:]}/{idto}\n\nTime: {str(TIMEZ)}')
                try:
                    if mdv.video.file_name:
                        to_file_name = mdv.video.file_name
                        size = mdv.video.file_size
                        duration = mdv.video.duration
                    elif mdv.document.file_name:
                        to_file_name = mdv.document.file_name
                        size = mdv.document.file_size
                        duration = "-:-:-"
                    elif mdv.caption:
                        to_file_name = mdv.caption
                        size = 0
                        duration = "-:-:-"
                except:
                    to_file_name = "NO_NAME"
                    size = 0
                    duration = "-:-:-"
                try:
                    durationx = str(timedelta(seconds=int(duration)))
                except:
                    durationx = "-:-:-"
                try:
                    sizex = get_human_size(int(size))
                except:
                    sizex = "0 B"
                final_to_file_name = f"▫️#Class_{str(z + 1)}: [{str(to_file_name)}](https://t.me/c/{str(TO_ID)[4:]}/{idto}) [Size: {str(sizex)}, Duration: {str(durationx)}]"
                final_to_file_name_new = f"▫️#**Class_{str(z + 1)}**: **--{str(to_file_name)}--** [**Size**: {str(sizex)}, **Duration**: {str(durationx)}]"
                MSG_DATA_LIST_NAME.append(final_to_file_name_new)
                MSG_DATA_LIST.append(final_to_file_name)
                MSG_TO_LIST.append(idto)
                STRING_LINK += "\n" + str(final_to_file_name)
                STRING_NAME += "\n" + str(final_to_file_name_new)
            D_KEY_LINK = str(BAYCH_NAME_ST) + str(NAME_ST) + str(STRING_LINK)
            MSG_DATA_DICT[f'LINK_{refer}'] = D_KEY_LINK
            D_KEY_NAME = str(BAYCH_NAME_ST) + str(NAME_ST) + str(STRING_NAME)
            MSG_DATA_DICT_NAME[f'NAME_{refer}'] = D_KEY_NAME
            FOLDERX = {f'{refer}': (f'{NAME}', f"{repr(MSG_TO_LIST)}", f'{CALL_FROMX}')}
            BOT_DICT[BATCH_NAME].update(FOLDERX)
        await msgx.edit_text(
            f'✅Successfully Copied {str(TOTL_MESSAGES)} Messages\n\nFROM_FINAL_ID: https://t.me/c/{str(FROM_ID)[4:]}/{str(FIN_ID)}\n\nTO_FINAL_ID: https://t.me/c/{str(TO_ID)[4:]}/{idto}\n\nTime: {str(TIMEZ)}')
        await client.send_message(chat_id=TO_ID, text=f'✅ {str(CALL_FROM.upper())}')
        limitx = 4000
        link_msg = ''
        final_msg_list = []
        for i in range(len(MSG_DATA_LIST)):
            limitx = limitx - len(MSG_DATA_LIST[i])
            if limitx >= 0:
                link_msg += str(MSG_DATA_LIST[i]) + '\n'
            if limitx <= 0:
                final_msg_list.append(link_msg)
                limitx = 4000
                link_msg = ''
                limitx = limitx - len(MSG_DATA_LIST[i])
                link_msg += str(MSG_DATA_LIST[i]) + '\n'
        final_msg_list.append(link_msg)
        limitx1 = 1650
        link_msg1 = ''
        final_msg_list_new = []
        for i in range(len(MSG_DATA_LIST_NAME)):
            limitx1 = limitx1 - len(MSG_DATA_LIST_NAME[i])
            if limitx1 >= 0:
                link_msg1 += str(MSG_DATA_LIST_NAME[i]) + '\n'
            if limitx1 <= 0:
                final_msg_list_new.append(link_msg1)
                limitx1 = 1650
                link_msg1 = ''
                limitx1 = limitx1 - len(MSG_DATA_LIST_NAME[i])
                link_msg1 += str(MSG_DATA_LIST_NAME[i]) + '\n'
        final_msg_list_new.append(link_msg1)
        if not os.path.isdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/{str(CALL_FROMX)}/'):
            os.mkdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/{str(CALL_FROMX)}/')
        if not os.path.isdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/BOT_DICT/'):
            os.mkdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/BOT_DICT/')
        if not os.path.isdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/LIST_MSGS/'):
            os.mkdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/LIST_MSGS/')
        if not os.path.isdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/LIST_MSGS_NAME/'):
            os.mkdir(f'./BACKUP/{str(BATCH_NAME).replace(" ", "_")}/LIST_MSGS_NAME/')
        BOT_DICT_write21 = open(
            f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/{str(CALL_FROMX)}/LINK_{str(CALL_FROMX)}.txt", "w")
        BOT_DICT_write21.write(repr(MSG_DATA_DICT))
        BOT_DICT_write21.close()
        BOT_DICT_write31 = open(
            f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/{str(CALL_FROMX)}/NAME_{str(CALL_FROMX)}.txt", "w")
        BOT_DICT_write31.write(repr(MSG_DATA_DICT_NAME))
        BOT_DICT_write31.close()
        BOT_DICT_write = open(
            f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/BOT_DICT/DICT_{str(BATCH_NAME).replace(' ', '_')}.txt", "w")
        BOT_DICT_write.write(repr(BOT_DICT))
        BOT_DICT_write.close()
        BOT_DICT_write1 = open(
            f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/LIST_MSGS/LIST_{str(BATCH_NAME).replace(' ', '_')}.txt", "w")
        BOT_DICT_write1.write(repr(final_msg_list))
        BOT_DICT_write1.close()
        BOT_DICT_write2 = open(
            f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/LIST_MSGS_NAME/LIST_NAME_{str(BATCH_NAME).replace(' ', '_')}.txt",
            "w")
        BOT_DICT_write2.write(repr(final_msg_list_new))
        BOT_DICT_write2.close()
        final_write2 = open("ongoing_dict.txt", "w")
        final_write2.write("{}")
        final_write2.close()
        if not os.path.isdir('./ARCHIVES/'):
            os.mkdir('./ARCHIVES/')
        dst = f"./ARCHIVES/{str(BATCH_NAME).replace(' ', '_')}"  # where to save
        src = f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}"  # directory to be zipped
        path_to_archive = make_archive(dst, 'zip', src)
        if not os.path.isdir('./NAMES/'):
            os.mkdir('./NAMES/')
        if not os.path.isdir('./NAMES_ARCHIVES/'):
            os.mkdir('./NAMES_ARCHIVES/')
        list12 = os.listdir("./NAMES_ARCHIVES") # dir is your directory path
        number_files = len(list12) + 1
        srcx = f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/{str(CALL_FROMX)}"
        dest = f'./NAMES/{str(CALL_FROMX)}'
        destination = shutil.copytree(srcx, dest)
        make_archive(f'./NAMES_ARCHIVES/Names_Backup_[{str(number_files)}]', 'zip', './NAMES')
        try:
            sleep(1)
            await client.send_message(chat_id=ZIP_CHAT,
                                      text=f'{str(BAYCH_NAME_ST)}')
            sleep(1)
            zix = await client.send_document(chat_id=ZIP_CHAT,
                                       document=f"./ARCHIVES/{str(BATCH_NAME).replace(' ', '_')}.zip")
            sleep(1)
            await client.send_message(chat_id=message.chat.id,
                                      text=f'✅Successfully Send Files To [ZIP_CHAT](https://t.me/c/{str(ZIP_CHAT)[4:]}/{str(zix.id)})')
        except:
            await client.send_message(chat_id=message.chat.id,
                                      text=f'❗Failed To Send Files To ZIP_CHAT')
        try:
            sleep(1)
            await client.send_message(chat_id=NAMES_CHAT,
                                      text=f'{str(BAYCH_NAME_ST)}')
            sleep(1)
            zix1 = await client.send_document(chat_id=NAMES_CHAT,
                                       document=f"./NAMES_ARCHIVES/Names_Backup_[{str(number_files)}].zip")
            sleep(1)
            await client.send_message(chat_id=message.chat.id,
                                      text=f'✅Successfully Send Files To [NAMES_CHAT](https://t.me/c/{str(NAMES_CHAT)[4:]}/{str(zix1.id)})')
        except:
            await client.send_message(chat_id=message.chat.id,
                                      text=f'❗Failed To Send Files To NAMES_CHAT')
        try:
            sleep(1)
            await client.send_message(chat_id=FILES_CHAT,
                                      text=f'{str(BAYCH_NAME_ST)}')
            sleep(1)
            await client.send_document(chat_id=FILES_CHAT,
                                       document=f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/{str(CALL_FROMX)}/LINK_{str(CALL_FROMX)}.txt")
            sleep(1)
            await client.send_document(chat_id=FILES_CHAT,
                                       document=f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/{str(CALL_FROMX)}/NAME_{str(CALL_FROMX)}.txt")
            sleep(1)
            await client.send_document(chat_id=FILES_CHAT,
                                       document=f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/BOT_DICT/DICT_{str(BATCH_NAME).replace(' ', '_')}.txt")
            sleep(1)
            await client.send_document(chat_id=FILES_CHAT,
                                       document=f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/LIST_MSGS/LIST_{str(BATCH_NAME).replace(' ', '_')}.txt")
            sleep(1)
            await client.send_document(chat_id=FILES_CHAT,
                                       document=f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/LIST_MSGS_NAME/LIST_NAME_{str(BATCH_NAME).replace(' ', '_')}.txt")
            sleep(1)
            zix2 = await client.send_document(chat_id=FILES_CHAT,
                                       document=f"./BACKUP/{str(BATCH_NAME).replace(' ', '_')}/COPY_DICT/COPY_DICT_{str(BATCH_NAME).replace(' ', '_')}.txt")
            sleep(1)
            await client.send_message(chat_id=message.chat.id,
                                      text=f'✅Successfully Send Files To [FILES_CHAT](https://t.me/c/{str(FILES_CHAT)[4:]}/{str(zix2.id)})')
        except:
            await client.send_message(chat_id=message.chat.id,
                                      text=f'❗Failed To Send Files To FILES_CHAT')
        for x in range(len(final_msg_list)):
            try:
                if x == 0:
                    zix3 = await client.send_message(chat_id=LINK_CHAT,
                                              text=f'{str(BAYCH_NAME_ST)}')
                    sleep(1)
                await client.send_message(chat_id=LINK_CHAT,
                                          text=f'{str(final_msg_list[x])}', parse_mode=enums.ParseMode.MARKDOWN)
                sleep(1)
                if x == len(final_msg_list) - 1:
                    await client.send_message(chat_id=message.chat.id,
                                              text=f'✅Successfully Send LINK MESSAGES To [LINK_CHAT](https://t.me/c/{str(LINK_CHAT)[4:]}/{str(zix3.id)})')
            except:
                await client.send_message(chat_id=message.chat.id,
                                          text=f'❗Failed To Send LINK MESSAGES To LINK_CHAT')

        for xi in range(len(final_msg_list_new)):
            try:
                if xi==0:
                    zix4 = await client.send_message(chat_id=NAMES_TEXT_CHAT,
                                              text=f'{str(BAYCH_NAME_ST)}')
                    sleep(1)
                await client.send_message(chat_id=NAMES_TEXT_CHAT,
                                          text=f'{str(final_msg_list_new[xi])}', parse_mode=enums.ParseMode.MARKDOWN)
                sleep(1)
                if xi == len(final_msg_list_new) - 1:
                    await client.send_message(chat_id=message.chat.id,
                                              text=f'✅Successfully Send NAMES MESSAGES To [NAMES_TEXT_CHAT](https://t.me/c/{str(NAMES_TEXT_CHAT)[4:]}/{str(zix4.id)})')
            except:
                await client.send_message(chat_id=message.chat.id,
                                          text=f'❗Failed To Send NAMES MESSAGES To NAMES_TEXT_CHAT')

    else:
        await client.send_message(chat_id=message.chat.id,
                                  text=f'Give Batch Name')


@Client.on_message(filters.text)
async def on_message_text(client, message):
    if str(message.from_user.id) in users:
            text = str(message.text)
            if text.startswith('https://'):
                text_list = text.splitlines()
                name_check = text_list[-1]
                from_id_channel = text.splitlines()[0].replace("https://t.me/c/", "").split("/")[0]
                await dict_gen(name_check, text, client, message, from_id_channel)
