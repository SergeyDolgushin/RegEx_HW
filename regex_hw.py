import re
import csv

def openCsvFile(path = "docs\phonebook_raw.csv", encoding='utf-8'):
  with open(path, encoding = encoding) as f:
    rows = csv.reader(f, delimiter=",")
    return list(rows)

def writeToCsvFile(contacts_list, path = "phonebook.csv"):
    with open(path, "w", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

def checkNameFieldsEntries(text_data):
    pattern = r"([А-Я])"
    return len(re.findall(pattern, text_data))

def searchPhoneNumber(text_data):
    pattern_phone_number = r"(\+7|8)(\s)?(\()?([\d+]{3})(\))?([\s-])?((\d){3})(-|\s)?((\d){2})(-|\s)?((\d){2})(\s)?(\()?(\w+)?(.)?(\s)?((\d+)(\))?)?"
    return re.sub(pattern_phone_number, r"+7(\4)\7-\10-\13 \17\18\21", text_data)
    
def makeCorrectedList(array_of_string):
    phone_record = []
    phonebook_records = [
    ['lastname','firstname','surname','organization','position','phone','email']
    ]
    for i, record in enumerate (array_of_string):
        if i != 0:
            res = re.split("[ ]", record[0])
            size = len(res)
            if size == 3:
                for i in range(len(res)):
                    phone_record.append(res[i])
                phone_record.append(record[3])
                phone_record.append(record[4])
                phone_record.append(searchPhoneNumber(record[5]).strip())
                phone_record.append(record[6]) if record[6] != '' else phone_record.append('')
            elif size == 2:
                for i in range(len(res)):
                    phone_record.append(res[i])
                phone_record.append(record[2])
                phone_record.append(record[3])
                phone_record.append(record[4])
                phone_record.append(searchPhoneNumber(record[5]).strip())
                phone_record.append(record[6]) if record[6] != '' else phone_record.append('')
            else:
                res = re.split("[ ]", record[1])
                if len(res) == 2:
                    phone_record.append(record[0])
                    phone_record.append(res[0])
                    phone_record.append(res[1])
                    phone_record.append(record[3])
                    phone_record.append(record[4])
                    phone_record.append(searchPhoneNumber(record[5]).strip())
                    phone_record.append(record[6]) if record[6] != '' else phone_record.append('')
                else:
                    phone_record.append(record[0])
                    phone_record.append(record[1])
                    phone_record.append(record[2])
                    phone_record.append(record[3])
                    phone_record.append(record[4])
                    phone_record.append(searchPhoneNumber(record[5]).strip())
                    phone_record.append(record[6]) if record[6] != '' else phone_record.append('')
            phonebook_records.append(phone_record)
            phone_record = []
    return phonebook_records

def deleteDoubleEntries(phonebook_records):
    for i, record in enumerate (phonebook_records):
        if i != 0:
            lastname = record[0]
            for j, record_2 in enumerate(phonebook_records):
                if j == len(phonebook_records): 
                    break
                elif j > i:
                    if lastname == record_2[0]:
                        for k in range(len(phonebook_records[0])):
                            if record[k] == '':
                                record[k] = record_2[k]
                        phonebook_records.pop(j)
    return phonebook_records

if __name__ == '__main__':
        
    corrected_phonebook = makeCorrectedList(openCsvFile()) 
    writeToCsvFile(deleteDoubleEntries(corrected_phonebook), path = "docs\phonebook.csv")
