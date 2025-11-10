import asyncio
from datetime import datetime, timedelta

from database.controllers import teacher, student as student_controller, my_class, subject, lesson
from database.database import create_tables
from database.cache import cache


async def main():
    await cache.set_token('124', {'gege': '1234'}, 124)

    await create_tables()

    class_obj = await my_class.get_by_name("РПО-52")
    class_id = class_obj.id if class_obj else None
    if class_id is None:
        print("РПО-52 - создан")
        class_id = await my_class.new_class("РПО-52")


    subject_obj = await subject.get_by_name("БД")
    subject_id = subject_obj.id if subject_obj else None
    if subject_id is None:
        subject_id = await subject.new_subject("БД")

    teacher_obj = await teacher.get_by_username("puzikov")
    teacher_id = teacher_obj.id if teacher_obj else None

    if teacher_id is None:
        print("puzikov - создан")
        teacher_id = await teacher.new_teacher(username="puzikov", name="Пузиков", password="12345")


    if await teacher.auth("puzikov", "12345") is None:
        print("Неправильный логин или пароль")


    students = [
        {"username": "garizanov", "name": "Гаризанов", "password": "1234"},
        {"username": "borodanov", "name": "Бороданов", "password": "1234"},
        {"username": "cherepanov", "name": "Черепанов", "password": "1234"}
    ]

    student_ids = []
    for student in students:
        student_obj = await student_controller.get_by_username(student["username"])
        if student_obj is None:
            print(f"{student['username']} - создан")
            student_id = await student_controller.new_student(
                username=student["username"],
                name=student["name"],
                password=student["password"],
                class_id=class_id
            )
            student_ids.append(student_id)
        else:
            student_ids.append(student_obj.id)

    lesson_obj = await lesson.get_by_id(5)
    lesson_id = lesson_obj.id if lesson_obj else None

    if lesson_id is None:
        lesson_id = await lesson.new_lesson(
            subject_id=subject_id,
            teacher_id=teacher_id,
            class_id=class_id,
            theme="pGAdmin",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=3)
        )
        print(f"Создан новый урок с ID: {lesson_id}")
    else:
        await lesson.update_mark_date(lesson_id)
        await lesson.update_theme(lesson_id, "Новая БД")

        await lesson.update_present_students(lesson_id, student_ids[0])
        await lesson.update_late_students(lesson_id, student_ids[1])
        await lesson.update_not_student(lesson_id, student_ids[2])

        print(f"Урок изменен: {lesson_id}")




if __name__ == '__main__':
    asyncio.run(main())