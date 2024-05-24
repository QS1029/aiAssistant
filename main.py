import requests
from aiogram import Bot, Dispatcher, types, executor
from config import TELEGRAM_TOKEN, YANDEX_TOKEN

bot = Bot(token = TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command = '/help', description = "Как работает Консультант?"),
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    await message.reply('Привет, я твой AI Консультант, я помогу с подготовкой к собеседованию. На какую должность в'
                        'какой компании ты претендуешь?')

@dp.message_handler(commands = 'help')
async def help(message: types.Message):
    await message.reply('Расскажи мне, в какую компанию ты хочешь устроиться, и на какую должность, я помогу.')

async def get_response(message_text):
    prompt = {
        "modelUri": "gpt://b1gf5pfjsd0phsrq2ldh/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "2000"
        },
        "messages": [
            { #Ты — рекрутер в указанной компании. Имитируй собеседование на работу для указанной должности, задавая вопросы, как будто ты потенциальный работодатель. Твоя задача — определить технические навыки кандидата. Сгенерируй вопросы для интервью с потенциальным кандидатом
                "role": "system",
                "text": "Ты - Ассистент для помощи пользователю. Будь вежлив, и отвечай на каждый заданные вопрос с подробностями, но"
                        "не переборщи с ними."
            },
            {
                "role": "user",
                "text": message_text
            }
        ]
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_TOKEN}"
    }
    response = requests.post(url, headers = headers, json = prompt)
    result = response.json()
    return result['result']['alternatives'][0]['message']['text']

@dp.message_handler()
async def analize_message(message:types.Message):
    response_text = await get_response((message.text))
    await message.answer(response_text)

async def on_startup(dispatcher):
    await set_commands(dispatcher.bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)