import random
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class ProblemSolving(StatesGroup):
    view_problem = State()
    view_solution = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        "Здравствуйте! Это телеграм-бот для решения задач по геометрии. "
        "Все задачи разбиты на 3 категории:\n    1) Лёгкий уровень\n    "
        "2) Средний уровень\n    3) Сложный уровень\n"
        "Доступные команды:\n"
        "\"Новая задача\" - получить новую задачу\n"
        "\"Показать решение\" - увидеть решение текушей задачи (автоматически отмечает задачу решённой)\n"
        "\"Отметить решённой\" - отметить текущую задачу решённой (решённые задачи больше не попадаются)\n"
        "\"/reset_solved\" - сбросить список решённых задач\n"
        "\"/help\" - увидеть полный список команд"
        , reply_markup=kb.main)
    await message.answer("Решите новую задачу!", reply_markup=kb.complexity_catalog)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "\"Новая задача\" - получить новую задачу\n"
        "\"Показать решение\" - увидеть решение текушей задачи (автоматически отмечает задачу решённой)\n"
        "\"Отметить решённой\" - отметить текущую задачу решённой (решённые задачи больше не попадаются)\n"
        "\"/reset_solved\" - сбросить список решённых задач\n"
        "\"/help\" - увидеть полный список команд"
    )


@router.message(F.text == "Новая задача")
async def new_problem(message: Message):
    await message.answer("Выберите сложность задачи:", reply_markup=kb.complexity_catalog)


async def give_problem(user_id, compl):
    problems = await rq.get_problems(user_id, compl)
    if not problems:
        return "all solved"
    problem = random.choice(problems)
    return problem


@router.callback_query(F.data == "lvl_easy")
async def lvl_easy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProblemSolving.view_problem)
    await callback.answer("Вы выбрали лёгкий уровень")

    problem = await give_problem(callback.from_user.id, 1)
    if problem == "all solved":
        await callback.message.answer("Задачи лёгкой сложности закончились, вы решили все!")
        await state.clear()
    else:
        await state.update_data(problem_id=problem.id)
        await callback.message.answer(problem.problem_text, reply_markup=kb.show_solution_and_mark_solved)


@router.callback_query(F.data == "lvl_medium")
async def lvl_medium(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProblemSolving.view_problem)
    await callback.answer("Вы выбрали средний уровень")

    problem = await give_problem(callback.from_user.id, 2)
    if problem == "all solved":
        await callback.message.answer("Средние задачи закончились, вы решили все!")
        await state.clear()
    else:
        await state.update_data(problem_id=problem.id)
        await callback.message.answer(problem.problem_text, reply_markup=kb.show_solution_and_mark_solved)


@router.callback_query(F.data == "lvl_hard")
async def lvl_hard(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProblemSolving.view_problem)
    await callback.answer("Вы выбрали сложный уровень")

    problem = await give_problem(callback.from_user.id, 3)
    if problem == "all solved":
        await callback.message.answer("Сложные задачи закончились, вы решили все!")
        await state.clear()
    else:
        await state.update_data(problem_id=problem.id)
        await callback.message.answer(problem.problem_text, reply_markup=kb.show_solution_and_mark_solved)


@router.callback_query(F.data == "show_solution")
async def show_solution(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        await callback.answer("Произошла ошибка")
        await state.clear()
        return

    problem = await rq.get_problem(data["problem_id"])
    await rq.mark_solved(callback.from_user.id, data["problem_id"])

    await callback.answer("Показываем решение задачи")
    await callback.message.answer(problem.solution_text)
    await state.clear()


@router.callback_query(F.data == "mark_solved")
async def mark_solved(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        await callback.answer("Произошла ошибка")
        await state.clear()
        return

    await rq.mark_solved(callback.from_user.id, data["problem_id"])
    await callback.answer("Задача помечена решённой")


@router.message(Command("reset_solved"))
async def reset_solved(message: Message):
    await rq.reset_solved(message.from_user.id)
    await message.answer("Список решённых задач сброшен")
