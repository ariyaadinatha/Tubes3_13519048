import fileIO
import boyer_moore
import re
import datetime


def getListOfKataPenting():
    return ["kuis", "ujian", "tucil", "tubes", "praktikum"]


def getFlag():
    # TODO : Lengkapin Flag
    return ["help", "assistant", "diundur", "selesai", "deadline"]


def GetInputDate(inputTask):

    inputDate = re.findall(
        "(\d{1,2}).(\d{1,2}).(\d{4})|(\d{1,2}).(\w+).(\d{4})", inputTask)
    filteredDate = []
    for date in inputDate:
        filteredData = []
        for data in date:
            if len(data) != 0:
                filteredData.append(data)
        filteredDate.append(filteredData)
    # print(filteredDate)
    return (filteredDate)


def DateConverter(inputListDate):
    ListOfMonths = ["januari", "februari", "maret", "april", "mei", "juni",
                    "juli", "agustus", "september", "oktober", "november", "desember"]
    # print(inputListDate)
    try:

        intMonth = int(inputListDate[1])

        return datetime.datetime(int(inputListDate[2]), intMonth, int(inputListDate[0])).strftime("%d/%m/%Y")
    except:
        pass
    i = 1
    while i < (len(ListOfMonths)):

        if inputListDate[1].lower() == ListOfMonths[i]:
            break
        i += 1
    if i == 13:
        raise Exception("Invalid Month Input!")
    return datetime.datetime(int(inputListDate[2]), i, int(inputListDate[0])).strftime("%d/%m/%Y")


def GetInputKodeKuliah(inputTask):
    task = ""
    task = re.search(
        "([a-zA-Z][a-zA-Z]\d{4})(.(\w*))*(?=\s(\d{1,2}).(\d{1,2}).(\d{4})|\s(\d{1,2}).(\w+).(\d{4}))", inputTask)

    if task:
        print("yo",task)
    else:
        print(task)
        task = task.group().strip(" pada")
        inputKodeKuliah = re.search(
            "([a-zA-Z][a-zA-Z]\d{4})", task).group()
        return inputKodeKuliah


def GetInputDeskripsiTugas(inputTask):
    task = re.search(
        "([a-zA-Z][a-zA-Z]\d{4})(.(\w*))*(?=\s(\d{1,2}).(\d{1,2}).(\d{4})|\s(\d{1,2}).(\w+).(\d{4}))", inputTask)
    task = task.group().strip(" pada")
    inputDeskripsiTugas = re.search(
        "(?<=([a-zA-Z][a-zA-Z]\d{4}\s))(.(\w*))*", task).group()
    return inputDeskripsiTugas


def GetKategoriTugas(inputTask):
    count = 0
    idx = -1

    for i in range(len(getListOfKataPenting())):
        if (boyer_moore.boyer_moore_string_matching(inputTask, getListOfKataPenting()[i])):
            count += 1
            idx = i
    if count > 1:
        raise Exception("More Than One Categories Inserted!")

    return getListOfKataPenting()[idx]


def query(database, queries, idx):
    # idx is the idx of the query type in database
    # For example if query type is "kode mata kuliah" then the idx is 1
    result = []
    for query in queries:
        for data in database:
            if data[idx] == query:
                result += [data]
    return result


def task_viewer(sentence):
    database = fileIO.loadTask()

    kata_penting = getListOfKataPenting()
    match = []
    for kata in kata_penting:
        if (boyer_moore.boyer_moore_string_matching(sentence, kata)):
            match += [kata]
    print("match: " + str(match))
    db = []

    for data in database:
        if (not data[4]):
            db += [data]

    # Dari regex
    list_of_date = GetInputDate(sentence)
    list_of_date = [DateConverter(inputDate) for inputDate in list_of_date]

    # for i in range(len(list_of_date)):
    #     list_of_date[i]
    print(list_of_date)

    result = []
    today = datetime.date.today()
    # Cari deadline yang < dari date
    if (len(list_of_date) == 1):
        print("Masuk")
        for each in db:
            date = list_of_date[0].split('/')
            temp = each[0].split("/")
            date = datetime.date(
                int(date[2]), int(date[1]), int(date[0]))
            deadline = datetime.date(
                int(temp[2]), int(temp[1]), int(temp[0]))
            if (deadline >= today) and (date <= deadline):
                result += [each]
        print("back")

    # Cari deadline yang diantara 2 date itu
    elif (len(list_of_date) == 2):
        print("Masuk2")
        for each in db:
            date1 = list_of_date[0].split('/')
            date2 = list_of_date[1].split('/')
            temp = each[0].split("/")
            deadline = datetime.date(
                int(temp[2]), int(temp[1]), int(temp[0]))
            deadline = datetime.date(
                int(temp[2]), int(temp[1]), int(temp[0]))

            if (deadline >= min(date1, date2)) and (max(date1, date2) <= deadline):
                result += [each]
        print("Keluar2")

    elif (len(list_of_date) > 2):
        # Error g
        print("Error")
        return []

    final =[]
    code = []
    try:
        code.append(GetInputKodeKuliah(sentence))
    except:
        pass

    if (code == []):
        final = result
    else:
        
    # 1 is the index of codes in database
    result = query(db, code, 1)

    # Jika match tidak ada, return semua
    tugas_in_match = [match[i] for i in range(
        len(match)) if match[i] in ["Tubes", "Tucil"]]
    if (tugas_in_match == []):
        return query(result, ["Tubes", "Tucil"], 2)
    else:
        return query(result, tugas_in_match, 2)


def HandleInput(inputTask):
    # Init local storage
    ListOfTask = []
    # Load File
    inputTask = inputTask.lower()
    try:
        ListOfTask = fileIO.loadTask()
    except Exception:
        pass

    flagFound = ""
    for flag in getFlag():
        if boyer_moore.boyer_moore_string_matching(inputTask, flag):
            flagFound = (flag)
            break
    if len(flagFound) == 0:

        inputDate = GetInputDate(inputTask)

        inputKodeKuliah = GetInputKodeKuliah(inputTask)
        try:
            inputKategoriTugas = GetKategoriTugas(inputTask)
        except Exception:
            return "Invalid Input! There can only be one category in input!"
        inputDeskripsiTugas = GetInputDeskripsiTugas(inputTask)
        if len(inputDate) > 1:
            return "Invalid Input! There can only be one date in input!"
        else:

            if inputDate and inputKodeKuliah and inputKategoriTugas and inputDeskripsiTugas:
                # print("Befero Append")
                ListOfTask.append([DateConverter(
                    inputDate[0]), inputKodeKuliah, inputKategoriTugas, inputDeskripsiTugas, False])
                # print("after Append")
                fileIO.saveTask(ListOfTask)

                output = "[TASK BERHASIL DICATAT]\n"
                output += "(ID: "+str(len(ListOfTask))+") "+str(ListOfTask[-1][0])+" - " + str(
                    ListOfTask[-1][1])+" - "+str(ListOfTask[-1][2]) + " - "+str(ListOfTask[-1][3])+"\n"
                return output
            else:
                return "Invalid Input1"
    elif("help" in flag) or ("assistant" in flag):
        return """
            [Fitur]
            1. Menambahkan task baru
            2. Melihat daftar task
            3. Melihat deadline dari suatu task
            4. Memperbaharui task
            5. Menandai suatu task sudah selesai
            6. Menampilkan opsi help

            [Daftar kata penting]
            1. Kuis
            2. Ujian
            3. Tucil
            4. Tubes
            5. Praktikum

        """
    elif ("deadline" in flag):
        task_viewer("")
    elif ("diundur" in flag):
        idIDX = re.findall("(?<=\s)(\d+)(?=\s)", inputTask)
        tgl_diundur = DateConverter(GetInputDate(inputTask)[0])
        found = False
        for i in range(len(ListOfTask)):
            if str(i+1) in (idIDX):
                ListOfTask[i][0] = tgl_diundur
                found = True
        if(not found):
            return "ID Task tidak ditemui"
        fileIO.saveTask(ListOfTask)
        return "Task Berhasil Di Update"
    elif ("selesai" in flag):
        idIDX = re.findall("(?<=\s)(\d+)(?=\s)", inputTask)
        found = False
        for i in range(len(ListOfTask)):
            if str(i+1) in (idIDX):
                ListOfTask[i][0] = True
                found = True
        if(not found):
            return "ID Task tidak ditemui"
        fileIO.saveTask(ListOfTask)
        return "Task Berhasil ditandai"

    ListOfTask.append([])
    # print(ListOfTask)


if __name__ == "__main__":
    #print(task_viewer("Apa aja deadline sampai 28-04-2021"))
    #print(HandleInput(" Deadline task 3 diundur menjadi 01/01/2021"))
    print(HandleInput("yo"))
    # print(HandleInput("Tubes IF2211 String Matching pada 14-02-2021"))

    # for j in range(len(ListOfTask)):
    #                         output+=str(j+1)+" "+ListOfTask[j][0]+" - "+ListOfTask[j][1]+" - "+ListOfTask[j][2]+" - "+ListOfTask[j][3]+"\n"
    #                     return output
