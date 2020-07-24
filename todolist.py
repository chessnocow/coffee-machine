from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


class ToDoList:
    engine = None
    Base = declarative_base()
    Session = None

    class Task(Base):
        __tablename__ = 'task'
        id = Column(Integer, primary_key=True)
        task = Column(String, default='default_value')
        deadline = Column(Date, default=datetime.today())

        def __repr__(self):
            return str(self.id) + " " + self.task + " " + self.deadline.strftime("%m/%d/%Y")

    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, text, date):
        session = self.Session()
        new_row = self.Task(task=text, deadline=date)
        session.add(new_row)
        session.commit()
        session.close()

    def print_task(self, date1, date2):
        session = self.Session()

        for day in [date1 + timedelta(days=x) for x in range(0, (date2 - date1).days)]:
            print("")
            print(day.strftime("%A %d %b:"))
            rows = session.query(self.Task).filter(self.Task.deadline == day.date()).all()
            if not rows:
                print("Nothing to do!")
            else:
                n = 1
                for row in rows:
                    print(f'{n}. {row.task}')
                    n += 1
        print("")
        session.close()

    def print_all_task(self, date=None):
        session = self.Session()
        if date:
            rows = session.query(self.Task).filter(self.Task.deadline <= date.date()).all()
        else:
            rows = session.query(self.Task).all()
        n = 1
        if not rows:
            print("Nothing to do!")
        else:
            for row in rows:
                print(f'{n}. {row.task} {row.deadline.strftime("%d %b")}')
                n += 1
        print("")
        session.close()

    def delete_task(self):
        session = self.Session()
        id_lst = []
        rows = session.query(self.Task).all()
        n = 1
        if not rows:
            print("Nothing to do!")
        else:
            for row in rows:
                print(f'{n}. {row.task} {row.deadline.strftime("%d %b")}')
                id_lst.append(row.id)
                n += 1
        del_num = int(input("Chose the number of the task you want to delete:"))
        session.delete(rows[del_num - 1])
        session.commit()
        print("The task has been deleted!")
        session.close()

    def menu(self):
        print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
''')
        choice = int(input())
        if choice == 0:
            exit(0)
        elif choice == 1:
            self.print_task(datetime.today(), datetime.today() + timedelta(days=1))
        elif choice == 2:
            self.print_task(datetime.today(), datetime.today() + timedelta(days=7))
        elif choice == 3:
            self.print_all_task()
        elif choice == 4:
            self.print_all_task(datetime.today())
        elif choice == 5:
            task_text = input('Enter task: ')
            deadline = input('Enter deadline: ')
            self.add_task(task_text, datetime.strptime(deadline, "%Y-%m-%d"))
            print("The task has been added!")
        elif choice == 6:
            self.delete_task()


def main():
    tdl = ToDoList()
    while True:
        tdl.menu()


if __name__ == '__main__':
    main()
