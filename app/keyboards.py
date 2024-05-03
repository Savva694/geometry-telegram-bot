from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Новая задача"),
                                      KeyboardButton(text="/help")]],
                           resize_keyboard=True)

complexity_catalog = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Лёгкий уровень", callback_data="lvl_easy")],
                     [InlineKeyboardButton(text="Средний уровень", callback_data="lvl_medium")],
                     [InlineKeyboardButton(text="Сложный уровень", callback_data="lvl_hard")]])

show_solution_and_mark_solved = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Показать решение", callback_data="show_solution")],
                     [InlineKeyboardButton(text="Отметить решённой", callback_data="mark_solved")]])
