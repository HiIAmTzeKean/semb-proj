from datetime import date

def retrieve_data_from_csv():
    data = []
    with open('testdata.csv') as f:
        line = f.readline()
        line = f.readline()  # skip first row
        while line and line[-1] == '\n':
            if len(line) > 1:
                data.append(line[:-1].split(','))

            line = f.readline()

        if line:
            data.append(line.split(','))

    return data

# print(retrieve_data_from_csv())


def retrieve_test_personnel_and_status():
    data = retrieve_data_from_csv()
    personnel = []
    personnel_status = []
    today = date.today().strftime('%Y-%m-%d')
    for i, p in enumerate(data, start=1):
        personnel.append((p[0], "RANK" + str(i), "Sembawang"))
        personnel_status.append((str(i), today, p[1].upper(), p[2].strip(), p[3].upper(), p[4].strip()))

    return personnel, personnel_status


def retrieve_test_users():
    return ("Admin", "Admin"), ("COS", "COS")


def write_testdata_file():
    personnel_list, personnel_status_list = retrieve_test_personnel_and_status()
    with open('test_data.sql', 'w') as f:
        f.write('INSERT INTO "user" ("username", "password")\n')
        f.write('VALUES {};\n'.format(str(retrieve_test_users())[1:-1]))

        f.write('\n')

        f.write('INSERT INTO "personnel" ("name", "rank", "fmw")\n')
        f.write('VALUES\n')
        for i, personnel in enumerate(personnel_list, start=1):
            f.write(str(personnel))
            f.write(',\n' if i != len(personnel_list) else ';\n')

        f.write('\n')

        f.write('INSERT INTO "personnel_status" ("personnel_id", "date", "am_status", "am_remarks", "pm_status", "pm_remarks")\n')
        f.write('VALUES\n')
        for i, personnel in enumerate(personnel_status_list, start=1):
            f.write(str(personnel))
            f.write(',\n' if i != len(personnel_status_list) else ';\n')


def generate_personnels():
    text =''
    for i in range(100):
        if i<=30:
            unit_id = 2
        elif i>30 and i<=50: 
            unit_id = 3
        elif i>50 and i <=80:
            unit_id = 6
        else:
            unit_id = 1
        print("('{}','{}',{},{}),".format("Person"+str(i),"RANK"+str(i),1,unit_id))
    return text

if __name__ == "__main__":
    generate_personnels()
