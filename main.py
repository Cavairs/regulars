from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_dict = {}
for contact in contacts_list:
    key = (contact[0].lower().strip(), contact[1].lower().strip())
    if key in contacts_dict:
        existing_contact = contacts_dict[key]
        for i in range(7, len(contact)):
            if contact[i] != '':
                existing_contact[i] = contact[i]
    else:
        contacts_dict[key] = contact

# телефонны к единому  формату
phone_regex = re.compile(
    r"\+?(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\sдоб.\s)?(\d+)?")
for contact in contacts_dict.values():
    phone = contact[5]
    match = phone_regex.fullmatch(phone)
    if match:
        groups = match.groups()
        phone = f"+7({groups[1]}){groups[2]}-{groups[3]}-{groups[4]}"
        if groups[5] and groups[6]:
            extension = f" доб.{groups[6]}"
            phone += extension
    contact[5] = phone

for contact in contacts_dict.values():
    full_name = contact[0]
    parts = full_name.split(" ")
    if len(parts) > 0:
        contact[0] = parts[0]
    if len(parts) > 1:
        contact[1] = parts[1]
    if len(parts) > 2:
        contact[2] = parts[2]

pprint(list(contacts_dict.values()))

with open("phonebook.csv", "w", encoding="utf-8-sig") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(contacts_dict.values())
