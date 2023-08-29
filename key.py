from aiogram import Bot, Dispatcher, Router, types

kb_1 = [
    [types.KeyboardButton(text="Пройти квест!")],

]

kb_2 = [
    [types.KeyboardButton(text="Получить вопрос!")],

]

kb_3 = [
    [
        types.KeyboardButton(text="Правда"),
        types.KeyboardButton(text="Ложь"),

    ],
]

kb_4 = [
    [
        types.KeyboardButton(text="Получить вопрос!"),
        types.KeyboardButton(text="Узнать подробности!"),

    ],
]


kb = [
    [
        types.KeyboardButton(text="Следующий вопрос"),
        types.KeyboardButton(text="Подробнее"),

    ],
]
