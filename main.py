import csv
import re
from collections import defaultdict

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


text = " ".join([", ".join(contact) for contact in contacts_list])

phone_numbers = re.findall(
    r'\+?\d{1,2}\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{2})[\s.-]?(\d{2})\s*(?:\(доб\.\s(\d{4})\)|\доб\.\s(\d{4}))?', text)

formatted_numbers = []
for phone in phone_numbers:
    formatted_number = f"+7({phone[0]}){phone[1]}-{phone[2]}-{phone[3]}"
    if phone[5]:
        formatted_number += f" доб.{phone[5]}"
    elif phone[4]:
        formatted_number += f" доб.{phone[4]}"
    formatted_numbers.append(formatted_number)


for i, contact in enumerate(contacts_list):
    if i < len(formatted_numbers):
        contacts_list[i][5] = formatted_numbers[i]
contact_dict = defaultdict(list)


for contact in contacts_list[1:]:
    full_name = f"{contact[0]} {contact[1]} {contact[2]}".strip()
    contact_info = contact[3:]

    if full_name in contact_dict:
        existing_contact = contact_dict[full_name]
        email_index = next(
            (i for i, val in enumerate(existing_contact) if val), None)
        for i in range(len(contact_info)):
            if contact_info[i] and not existing_contact[i]:
                existing_contact[i] = contact_info[i]
            if i == len(contact_info) - 1 and email_index is not None:
                existing_contact[email_index] = contact_info[i]
            elif i == len(contact_info) - 1 and email_index is None:
                existing_contact.append(contact_info[i])
    else:
        contact_dict[full_name] = contact_info

new_contacts_list = [["lastname", "firstname", "surname",
                      "organization", "position", "phone", "email"]]


for full_name, contact_info in contact_dict.items():
    new_contacts_list.append([*full_name.split(), *contact_info])


phone_pattern = re.compile(
    r'\+?\d{1,2}\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{2})[\s.-]?(\d{2})\s*(?:\(доб\.\s(\d{4})\)|\доб\.\s(\d{4}))?')

data_dict = {}
for item in new_contacts_list:
    key = item[0] + item[1]
    if key in data_dict:
        if item[-1]:  # проверяем, что есть адрес электронной почты
            data_dict[key][-1] = item[-1]  # обновляем адрес электронной почты
        if item[5]:  # проверяем, что есть номер телефона
            phone_match = phone_pattern.search(item[5])
            if phone_match:
                # обновляем номер телефона
                data_dict[key][5] = phone_match.group()
        if 'доб' in item[5]:  # проверяем наличие добавочного номера
            # проверяем наличие добавочного номера в существующем контакте
            if 'доб' in data_dict[key][5]:
                existing_phone, existing_extension = data_dict[key][5].split(
                    ' доб.')
                new_extension = item[5].split('доб.')[-1].strip()
                # data_dict[key][5] = f"{existing_phone} доб.{
                #     new_extension}"  # обновляем добавочный номер
            else:
                # добавляем новый добавочный номер, если его еще нет
                data_dict[key][5] += f' {item[5].split("доб.")[-1].strip()}'
    else:
        if item[5]:  # проверяем, что есть номер телефона
            phone_match = phone_pattern.search(item[5])
            if phone_match:
                item[5] = phone_match.group()  # обновляем номер телефона
            if 'доб' in item[5]:  # проверяем наличие добавочного номера
                # добавляем добавочный номер
                item[5] += ' ' + item[5].split('доб.')[-1].strip()
        data_dict[key] = item

filtered_data = list(data_dict.values())


with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(filtered_data)
