from app.database.models import async_session
from app.database.models import User, Complexity, Problem
from sqlalchemy import select

import app.database.problems as pr
import app.database.solutions as sol


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, solved=""))
            await session.commit()


async def get_problems(user_id, compl):
    async with async_session() as session:
        problems = list(await session.scalars(select(Problem).where(Problem.complexity == compl)))
        viewed_problems = list(await session.scalars(select(User).where(User.tg_id == user_id)))[0].solved.split()
        not_viewed_problems = [problem for problem in problems if not str(problem.id) in viewed_problems]
        return not_viewed_problems


async def get_problem(problem_id):
    async with async_session() as session:
        problems = list(await session.scalars(select(Problem).where(Problem.id == problem_id)))
        return problems[0]


async def mark_solved(user_id, problem_id):
    async with async_session() as session:
        user = list(await session.scalars(select(User).where(User.tg_id == user_id)))[0]
        if not str(problem_id) in user.solved.split():
            user.solved = user.solved + " " + str(problem_id)
        await session.commit()


async def reset_solved(user_id):
    async with async_session() as session:
        user = list(await session.scalars(select(User).where(User.tg_id == user_id)))[0]
        user.solved = ""
        await session.commit()


async def download_complexities():
    async with async_session() as session:
        complexity = await session.scalar(select(Complexity).where(Complexity.id == 1))
        if not complexity:
            session.add(Complexity(name="easy"))
            await session.commit()

        complexity = await session.scalar(select(Complexity).where(Complexity.id == 2))
        if not complexity:
            session.add(Complexity(name="medium"))
            await session.commit()

        complexity = await session.scalar(select(Complexity).where(Complexity.id == 3))
        if not complexity:
            session.add(Complexity(name="hard"))
            await session.commit()


async def download_problems():
    async with async_session() as session:
        problems = [[pr.problem_1_1, sol.solution_1_1, 1],
                    [pr.problem_1_2, sol.solution_1_2, 1],
                    [pr.problem_1_3, sol.solution_1_3, 1],
                    [pr.problem_2_1, sol.solution_2_1, 2],
                    [pr.problem_3_1, sol.solution_3_1, 3],
                    [pr.problem_3_2, sol.solution_3_2, 3]]

        for problem in problems:
            problem_text, solution_text, complexity = problem[0], problem[1], problem[2]
            bd_problem = await session.scalar(select(Problem).where(Problem.problem_text == problem_text))
            if not bd_problem:
                session.add(Problem(problem_text=problem_text,
                                    solution_text=solution_text,
                                    complexity=complexity))
                await session.commit()
