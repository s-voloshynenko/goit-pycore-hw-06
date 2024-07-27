import re
from collections import UserDict

class NotValidPhoneNumberError(Exception):
    def __init__(self, message="Wrong phone number"):
        self.message = message
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # keep it empty, no overrides
    pass

class Phone(Field):
    PHONE_NUMBER_REGEX = r"\d{10}"

    def __init__(self, value: str):
        if not re.fullmatch(Phone.PHONE_NUMBER_REGEX, value):
            raise NotValidPhoneNumberError("Phone number must be 10 digits")

        super().__init__(value)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_to_remove: str):
        self.phones = [phone for phone in self.phones if phone.value != phone_to_remove]

    def edit_phone(self, phone_to_edit: str, phone_new_value: str):
        for phone in self.phones:
            if phone.value == phone_to_edit:
                phone.value = phone_new_value
                break # exit from the loop when found the first match

    def find_phone(self, phone_to_find: str):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Phone:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
