from datetime import timedelta, datetime
import math
 
# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


# список всех имен таблиц в базе данных
# print(engine.table_names())
class Athelete(Base):

    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    """
    Опиывает структуру таблицы user для хранения записей музыкальной библиотеки
    """
    # указываем имя таблицы
    __tablename__ = "user"
    # Задаем колонки в формате
    # название_колонки = sa.Column(ТИП_КОЛОНКИ)
    # идентификатор строки
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
	# Пол
    gender = sa.Column(sa.Text)
	# адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # Дата рождения
    birthdate = sa.Column(sa.Text)
    # Рост
    height = sa.Column(sa.REAL)

def pars_date(str_date):
    dat = str_date.split("-")
    year = dat[0].strip()
    month = dat[1].strip()
    day = dat[2].strip()
    ye = int(year)
    mo = int(month)
    da = int(day)
    # print(ye, mo, da)
    return [ye, mo, da]


def find_athl(id_, session):
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # нахдим все записи в таблице User, у которых поле User.first_name совпадает с парарметром name
    dh = 10
    h_id = 1
    d_id = 1
    d = 1000000
    query = session.query(User).filter(User.id == id_)
    if query.count() == 0:
        print("Такого атлета нет")
    else:
        all_atl_list = session.query(Athelete).all()
        atl_et = query[0]
        dat = pars_date(atl_et.birthdate)
        dat_et = datetime(dat[0], dat[1], dat[2])
        
        for atl in all_atl_list:
            if atl.height and atl.birthdate:
                dat = pars_date(atl.birthdate)
                data = datetime(dat[0], dat[1], dat[2])
                da = (dat_et - data)
                # print(da.days)
                p = math.fabs(da.days)
                if p < d:
                    d = p
                    d_id = atl.id
                # print(atl_et.height, atl.height)
                p = math.fabs(atl_et.height - atl.height)
                if  p < dh:
                    dh = p
                    h_id = atl.id
        near_height_atl = all_atl_list[h_id-1]
        near_birthdate_atl = all_atl_list[d_id-1]

        print("Ближайший по росту атлет", near_height_atl.id,near_height_atl.name, near_height_atl.height)
        print("Ближайший по дате рождения атлет", near_birthdate_atl.id,near_birthdate_atl.name, near_birthdate_atl.birthdate)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()




def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    
    session = connect_db()

    # выводим приветствие
    print("Привет! Ищем ближайших по росту и дате рождения атлетов.")
    # запрашиваем у пользователя данные
    id_ = input("Введите ID атлета: ")

    # # вызываем функцию поиска по имени
    
    find_athl(id_, session)

    all_users_list = session.query(User).all()
    # print('Вы выбрали', user.id, ' Имя: ', user.first_name, ' Фамилия: ', user.last_name, ' Рост: ', user.height, ' Дата рождения: ', user.birthdate)



     # вызываем функцию печати на экран результатов поиска
    print('Все пользователи в базе "user"')
    for user in all_users_list:
        print(user.id, ' Имя: ', user.first_name, ' Фамилия: ', user.last_name, ' Рост: ', user.height, ' Дата рождения: ', user.birthdate)

    
    # print("Некорректный режим:(")


if __name__ == "__main__":
    main()
