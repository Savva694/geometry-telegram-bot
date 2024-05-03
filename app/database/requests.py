from app.database.models import async_session
from app.database.models import User, Complexity, Problem
from sqlalchemy import select


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
        problems = [[("Биссектриса внешнего угла при вершине C треугольника "
                      "ABC пересекает описанную окружность в точке D. Докажите, "
                      "что AD = BD."),
                     ("Отметим на продолжении AC за точку C точку X. Заметим, что: "
                      "уг ABD = уг ACD = (уг BCX) / 2 = 180 - уг BCD = уг BAD. "
                      "То есть треугольник ABD - равнобедренный, и AD = BD."),
                     1],
                    [("Две окружности пересекаются в точках A и B. Точка X лежит на прямой "
                      "AB, но не на отрезке AB. Докажите, что длины всех касательных, "
                      "проведенных из точки X к окружностям, равны."),
                     ("По теореме о квадрате касательной квадрат каждого из отрезков "
                      "касательных, проведённых из точки X к данным окружностям, равен XA * XB."),
                     1],
                    [("ABCD — параллелограмм, M — середина AF, N — середина CE, где E и F лежат на "
                      "CD и AD соотвтственно. Доказать, что если B, M и E на одной прямой, то и B, "
                      "N, F тоже на одной прямой."),
                     ("Проведём через точку F, прямую параллельную AB, ее пересечение с ВС это Т. "
                      "Пересечение с ВМ это К. Тогда легко заметить что МF- паралельно BT, и равно "
                      "его половине. Следовательно MF- средняя линия ТК, тогда по замечательному "
                      "свойству трапеции В, N, F лежат на одной прямой"),
                     1],
                    [("Точка HI — ортоцентр треугольника A1BC и центр вписанной окружности треугольника "
                      "A2BC. O — центр описанной окружности треугольника A1BC. A2 такова, что HI - "
                      "центр вписанной окружности треугольника A2BC. Докажите, что A1A2, OHI и BC "
                      "пересекаются в одной точке."),
                     ("Заметим, что A1O параллельно A2HI; Также BA1 и BHI изогонали относительно <A2BO. "
                      "Тогда теорема об изогоналях завершает задачу"),
                     2],
                    [("Дан описанный четырехугольник ABCD, в котором диагональ AC не является "
                      "биссектрисой угла С. На этой биссектрисе отмечена точка E, такая, что AE и "
                      "BD перпендикулярны. Точка F — основание перпендикуляра, опущенного из точки "
                      "E на сторону BC. Докажите, что AB=BF."),
                     ("Отметим на CD т. G: AD=DG. Тогда FC=CG, поэтому выполнена "
                      "теорема Карно для BCD, AFG."),
                     3],
                    [("Две окружности касаются внешним образом в точке A. На их общей внешней "
                      "касательной выбрана точка D. Из точки D проведена касательная DB к первой "
                      "окружности, пересекающая вторую в точке C. Докажите, что окружность (ABC) "
                      "касается прямой, соединяющей D с центром первой окружности."),
                     ("Сделаем инверсию в точке А. Тогда окружности станут параллельными прямыми. "
                      "Окружность (ABC) станет прямой BC, а прямая DO станет окружностью, проходящей "
                      "через D и A, центр которой лежит на BQ. Покажем, что такая окр касается BC. "
                      "X и Y - пересечение PQ с BC и BE. Заметим, что отношения степеней точек X и Y "
                      "относительно зел. и син. окр равны => по лемме о соосных окружностях (XYAD) - "
                      "вписанный. Но O1O2 и BQ - серперы к AD и XY => S (их пересечение) - центр (XYAD) "
                      "=> уг SXB = 90 => (XYAD) касается BC. Остается только осознать, что эта "
                      "окружность (XYAD) нам подходит. В самом деле, ведь она проходит через A и "
                      "D, а ее центр лежит на BQ. Отдельно стоит пояснить почему уг SXB = 90. SQ*SB "
                      "= SD^2 = SX^2 => SX/SQ = SB/SX => треуги SXQ и SBX - подобны => уг SXB = "
                      "уг SQX = 90"),
                     3]
                ]

        for problem in problems:
            problem_text, solution_text, complexity = problem[0], problem[1], problem[2]
            bd_problem = await session.scalar(select(Problem).where(Problem.problem_text == problem_text))
            if not bd_problem:
                session.add(Problem(problem_text=problem_text,
                                    solution_text=solution_text,
                                    complexity=complexity))
                await session.commit()
