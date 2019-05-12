import csv
subject = input("Enter subject name:")
flag = False
with open('edited/DSL-StrongPasswordData.csv', 'r') as inp, open('./edited_dataset/DSL-StrongPasswordData.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[0] != subject:
            writer.writerow(row)
        else:
            flag = True
            print("subject found, rows deleted!")

if not flag:
    print("subject not found!")

