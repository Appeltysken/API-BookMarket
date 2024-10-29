import asyncio
from app.database import async_session_maker
from app.entities.users.models import User
from app.entities.books.models import Book
from app.entities.orders.models import Order
from app.entities.reviews.models import Review
from app.entities.authors.models import Author
from app.entities.users.auth import get_password_hash
async def populate_data():
    async with async_session_maker() as session:
        authors = [
            Author(name="Джордж Оруэлл", bio="Английский романист и критик, известный своими произведениями '1984' и 'Скотный двор'.", author_picture=None),
            Author(name="Джоан Роулинг", bio="Британская писательница, наиболее известная по серии книг о Гарри Поттере.", author_picture=None),
            Author(name="Айзек Азимов", bio="Американский писатель и профессор биохимии, известный своими произведениями в жанре научной фантастики.", author_picture=None),
            Author(name="Джон Р. Р. Толкин", bio="Английский писатель, известный по книгам 'Хоббит' и 'Властелин колец'.", author_picture=None),
            Author(name="Стивен Кинг", bio="Американский писатель, автор книг в жанрах ужасов, научной фантастики и фэнтези.", author_picture=None),
        ]
        
        session.add_all(authors)
        await session.commit()

        users = [
            User(username="+79161234567", password=get_password_hash("HashedPass1!"), Fname="Александр", Lname="Петров", sex="Мужской", email="alex.petroff@mail.ru", phone="+79161234567", profile_picture=None),
            User(username="ekaterina.sidorova@mail.ru", password=get_password_hash("SecurePass2@"), Fname="Екатерина", Lname="Сидорова", sex="Женский", email="ekaterina.sidorova@mail.ru", phone="+79011234567", profile_picture=None),
            User(username="ivan.ivanov@example.com", password=get_password_hash("Password3$"), Fname="Иван", Lname="Иванов", sex="Мужской", email="ivan.ivanov@example.com", phone="+79561234567", profile_picture=None),
            User(username="+79301234567", password=get_password_hash("StrongPass4%"), Fname="Мария", Lname="Николаева", sex="Женский", email="maria.nikolaeva@mail.ru", phone="+79301234567", profile_picture=None),
        ]
        
        session.add_all(users)
        await session.commit()

        books = [
            Book(name="1984", author_id=1, genre="Антиутопия", publisher="Secker & Warburg", description="Антиутопический роман о тоталитарном обществе.", price=15.99, book_picture=None, user_id=2),
            Book(name="Гарри Поттер и философский камень", author_id=2, genre="Фэнтези", publisher="Bloomsbury", description="Мальчик узнает, что он волшебник и поступает в школу магии Хогвартс.", price=12.99, book_picture=None, user_id=3),
            Book(name="Основание", author_id=3, genre="Научная фантастика", publisher="Gnome Press", description="Научно-фантастическая серия о будущем галактической империи.", price=20.00, book_picture=None, user_id=2),
            Book(name="Хоббит", author_id=4, genre="Фэнтези", publisher="George Allen & Unwin", description="Фэнтезийный роман о приключениях Бильбо Бэггинса.", price=18.50, book_picture=None, user_id=4),
            Book(name="Сияние", author_id=5, genre="Ужасы", publisher="Doubleday", description="Ужасный роман о семье, останавливающейся в изолированном отеле с зловещей атмосферой.", price=14.99, book_picture=None, user_id=5),
        ]
        
        session.add_all(books)
        await session.commit()

        orders = [
            Order(status="Ожидает обработки", price=15.99, user_id=2, books_id=1),
            Order(status="Завершен", price=12.99, user_id=4, books_id=2),
            Order(status="Отменен", price=20.00, user_id=3, books_id=3),
            Order(status="В процессе", price=18.50, user_id=4, books_id=4),
            Order(status="Завершен", price=14.99, user_id=5, books_id=5),
        ]
        
        session.add_all(orders)
        await session.commit()

        reviews = [
            Review(text="Холодная история о тоталитаризме. Обязательное чтение!", mark=5, user_id=2, book_id=1),
            Review(text="Завораживающее приключение для всех возрастов.", mark=5, user_id=3, book_id=2),
            Review(text="Заставляет задуматься и остается актуальным.", mark=4, user_id=2, book_id=3),
            Review(text="Классическая фэнтези, проверенная временем.", mark=5, user_id=4, book_id=4),
            Review(text="Ужасающе и захватывающе. Кинг в лучшем виде.", mark=4, user_id=5, book_id=5),
        ]
        
        session.add_all(reviews)
        await session.commit()

def main():
    asyncio.run(populate_data())

if __name__ == "__main__":
    main()