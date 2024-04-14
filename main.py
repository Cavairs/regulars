import csv
import re
from collections import defaultdict

# Чтение данных из файла
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Шаблон для извлечения номера телефона
phone_pattern = re.compile(
    r'(\+?\d{1,2})?[ -]?\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{2})[ -]?(\d{2})\s*(?:\(доб\.\s?(\d{4})\)|доб\.\s?(\d{4}))?')

# Обработка номеров телефонов в списках контактов
for contact in contacts_list:
    phone_match = phone_pattern.search(contact[5])

    if phone_match:
        country_code = phone_match.group(1) if phone_match.group(1) else "+7"
        area_code = phone_match.group(2)
        first_part = phone_match.group(3)
        second_part = phone_match.group(4)
        third_part = phone_match.group(5)
        extension = " доб." + (phone_match.group(6) or phone_match.group(7)
                               ) if phone_match.group(6) or phone_match.group(7) else ""

        formatted_phone = f"{country_code}({area_code}){
            first_part}-{second_part}-{third_part}{extension}"
        contact[5] = formatted_phone

unique_contacts_dict = defaultdict(list)

for contact in contacts_list[1:]:
    lastname, firstname, surname = contact[0].strip(
    ), contact[1].strip(), contact[2].strip()
    full_name = f"{lastname} {firstname} {surname}".strip()
    unique_contacts_dict[full_name].append(contact)

# Создание списка
unique_contacts = [contacts_list[0]]

for full_name, contacts in unique_contacts_dict.items():
    if len(contacts) == 1:
        unique_contacts.append(contacts[0])
    else:
        merged_contact = contacts[0]
        for contact in contacts[1:]:
            for i in range(3, len(contact)):
                if contact[i] and not merged_contact[i]:
                    merged_contact[i] = contact[i]
        unique_contacts.append(merged_contact)

# Удаление дубликатов и обновление почты для Лагунцова
for i, contact in enumerate(unique_contacts):
    if contact[0] == "Лагунцов Иван Алексеевич":
        contact[6] = "Ivan.Laguntcov@minfin.ru"  # Обновляем почту
        del unique_contacts[i+1]  # Удаляем дубликат записи

# Запись уникальных контактов в файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(unique_contacts)
