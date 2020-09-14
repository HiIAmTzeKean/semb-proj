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
    date = "2020-01-01"
    for i, p in enumerate(data, start=1):
        personnel.append((p[0], "RANK" + str(i), "Sembawang"))
        personnel_status.append((str(i), date, 'AM', p[1].upper(), p[2].strip()))
        personnel_status.append((str(i), date, 'PM', p[3].upper(), p[4].strip()))

    return personnel, personnel_status


def retrieve_test_users():
    return ("Admin", "Admin"), ("COS", "COS")


def write_testdata_file():
    personnel_list, personnel_status_list = retrieve_test_personnel_and_status()
    with open('test_data.sql', 'w') as f:
        f.write('INSERT INTO "user" ("username", "password")\n')
        f.write('VALUES {};\n'.format(retrieve_test_users()))

        f.write('\n')

        f.write('INSERT INTO "personnel" ("name", "rank", "fmw")\n')
        f.write('VALUES\n')
        for i, personnel in enumerate(personnel_list, start=1):
            f.write(str(personnel))
            f.write(',\n' if i != len(personnel_list) else ';\n')

        f.write('\n')

        f.write('INSERT INTO "personnel_status" ("personnel_id", "date", "time", "status", "remarks")\n')
        f.write('VALUES\n')
        for i, personnel in enumerate(personnel_status_list, start=1):
            f.write(str(personnel))
            f.write(',\n' if i != len(personnel_status_list) else ';\n')


if __name__ == '__main__':
    write_testdata_file()
