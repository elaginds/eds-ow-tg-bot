import telebot
import os
import json

TOKEN = os.getenv('EDS_OW_TG_BOT_TOKEN')

with open('tanks-list.json', 'r') as file:
    TANKS_LIST = json.load(file)

print('TOKEN', TOKEN)
if not TOKEN:
    raise RuntimeError('EDS_OW_TG_BOT_TOKEN не задан')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def main(message):
    print('START')
    bot.send_message(message.chat.id, 'HELLO!')


# dva - D.Va
# doomfist - Doomfist
# hazard - Hazard
# queen - Junker Queen
# mauga - Mauga
# orisa - Orisa
# ramattra - Ramattra
# rein - Reinhardt
# hog - Roadhog
# sigma - Sigma
# winston - Winston
# ball - Wrecking Ball
# zarya - Zarya
@bot.message_handler(commands=['dva', 'doomfist', 'hazard', 'queen', 'mauga', 'orisa', 'ramattra', 'rein', 'hog', 'sigma', 'winston', 'ball', 'zarya'])
def main(message):
    print('NOW', message.text)

    msg = getMessage(message.text)
    # msg = 'HI'
    bot.send_message(message.chat.id, msg, parse_mode='HTML')

def getMessage(command):
    print('command', command)
    tank_id = getIdFromChat(command)
    print('tankId', tank_id)

    strong_against_them = getStrongAgainstThem(tank_id)
    print('strong_against_them', strong_against_them)

    weak_against_them = getWeakAgainstThem(tank_id)
    print('weak_against_them', weak_against_them)

    msg = createMessage(strong_against_them, weak_against_them)
    print('msg', msg)

    return msg

def getIdFromChat(command):
    found_dict = None

    for item in TANKS_LIST:
        if item.get('command') == command:
            found_dict = item
            break

    return found_dict['id']

def getStrongAgainstThem(tank_id):
    tank = getDictFromId(tank_id)

    tank['strong'] = [getDictFromId(item)['name'] for item in tank['strong']]
    tank['good'] = [getDictFromId(item)['name'] for item in tank['good']]

    return tank

def getDictFromId(tank_id):
    found_dict = None

    for item in TANKS_LIST:
        if item.get('id') == tank_id:
            found_dict = item
            break

    return found_dict

def getWeakAgainstThem(tank_id):
    result = {
        'weak': [],
        'bad': []
    }

    for item in TANKS_LIST:
        if tank_id in item.get('strong'):
            result['weak'].append(getDictFromId(item.get('id'))['name'])

        if tank_id in item.get('good'):
            result['bad'].append(getDictFromId(item.get('id'))['name'])

    return result

def createMessage(strong_against_them, weak_against_them):
    result_list = [getMsgName(strong_against_them['name']),
                   getMsgStrong(strong_against_them),
                   getMsgGood(strong_against_them),
                   getMsgBad(weak_against_them),
                   getMsgWeak(weak_against_them)]

    print('result_list', result_list)

    return "\n".join(result_list)

def getMsgName(name):
    return f'<b>{name}</b>'

def getMsgStrong(strong_against_them):
    return f'<b>Strong - {", ".join(strong_against_them['strong']) if strong_against_them['strong'] else "None"}</b>'

def getMsgGood(strong_against_them):
    return f'<b><i>Good - {", ".join(strong_against_them['good']) if strong_against_them['good'] else "None"}</i></b>'

def getMsgBad(weak_against_them):
    return f'<i>Bad - {", ".join(weak_against_them['bad']) if weak_against_them['bad'] else "None"}</i>'

def getMsgWeak(weak_against_them):
    return f'<i>Weak - {", ".join(weak_against_them['weak']) if weak_against_them['weak'] else "None"}</i>'


# getMessage('/dva')
bot.polling(none_stop=True)