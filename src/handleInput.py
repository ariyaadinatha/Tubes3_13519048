import fileIO
import boyer_moore
import re
import datetime


def getListOfKataPenting():
    return ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]


def getFlag():
    return ["help", "assistant", "diundur", "selesai", "kapan", "deadline", "tugas", "apa saja", "apa aja"]


def GetInputDate(inputTask):

    inputDate = re.findall(
        "(\d{1,2}).(\d{1,2}).(\d{2,4})|(\d{1,2}).(\w+).(\d{4})", inputTask)
    filteredDate = []
    for date in inputDate:
        filteredData = []
        for data in date:
            if len(data) != 0:
                filteredData.append(data)
        filteredDate.append(filteredData)

    return (filteredDate)


def DateConverter(inputListDate):
    ListOfMonths = ["januari", "februari", "maret", "april", "mei", "juni",
                    "juli", "agustus", "september", "oktober", "november", "desember"]

    try:

        intMonth = int(inputListDate[1])

        if(len(inputListDate[2])==2):
            inputListDate[2] = "20" + inputListDate[2]
        return datetime.datetime(int(inputListDate[2]), intMonth, int(inputListDate[0])).strftime("%d/%m/%Y")
    except:
        pass
    i = 0
    while i < (len(ListOfMonths)):

        if inputListDate[1].lower() == ListOfMonths[i]:
            break
        i += 1
    if i == 12:
        raise Exception("Invalid Date Input!")
    return datetime.datetime(int(inputListDate[2]), i+1, int(inputListDate[0])).strftime("%d/%m/%Y")


def GetInputKodeKuliah(inputTask):
    task = re.search(
        "([a-zA-Z][a-zA-Z]\d{4})", inputTask)
    if task is None:
        return ""
    else:
        task = task.group().strip(" pada")
        inputKodeKuliah = re.search(
            "([a-zA-Z][a-zA-Z]\d{4})", task).group()
        return inputKodeKuliah


def GetInputDeskripsiTugas(inputTask):
    task = re.search(
        "([a-zA-Z][a-zA-Z]\d{4})(.(\w*))*(?=\s(\d{1,2}).(\d{1,2}).(\d{2,4})|\s(\d{1,2}).(\w+).(\d{4}))", inputTask)
    if task is None:
        return "No description provided"
    task = task.group().strip(" pada")
    temp = re.search(
        "(?<=([a-zA-Z][a-zA-Z]\d{4}\s))(.(\w*))*", task)
    if (temp is None):
        return "No description provided"
    return temp.group()


def GetKategoriTugas(inputTask):
    count = 0
    idx = -1
    for i in range(len(getListOfKataPenting())):
        if (boyer_moore.boyer_moore_string_matching(inputTask.lower(), getListOfKataPenting()[i].lower())):
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
            if data[idx].lower() == query.lower():
                result.append(data)
    return result


def task_viewer(sentence, indeks, database):
    database = fileIO.loadTask()
    
    kata_penting = getListOfKataPenting()
    
    match = []

    for kata in kata_penting:

        if (boyer_moore.boyer_moore_string_matching(sentence.lower(), kata.lower())):
            match += [kata]

    if (indeks == 1):
        for kata in match:
            if (kata not in ["Tubes", "Tucil"]):
                return ["Error"]
    db = []

    for i in range(len(database)):
        database[i].append(i+1)

    for data in database:
        if (not data[4]):
            db += [data]
    # Dari regex
    list_of_date = GetInputDate(sentence)
    try :
        list_of_date = [DateConverter(inputDate) for inputDate in list_of_date]
    except:
        return ["Invalid Date Input!"]

    # for i in range(len(list_of_date)):
    #     list_of_date[i]

    result = []
    today = datetime.date.today()
    # Cari deadline yang < dari date
    if (len(list_of_date) == 0):
        date = datetime.date.today()
        special_time = ["besok", "lusa", "minggu depan",
                        "bulan depan", "tahun depan", "hari ini", "minggu ini", "bulan ini", "tahun ini"]
        special_time_value = ["1 hari", "2 hari",
                              "7 hari", "1 bulan", "1 tahun", "1 hari", "7 hari", "1 bulan", "1 tahun"]

        for i in range(len(special_time)):
            sentence = sentence.replace(special_time[i], special_time_value[i])
        time_unit = ["hari", "minggu", "bulan", "tahun"]
        idIDX = re.findall("(?<=\s)(\d+)(?=\s)", sentence)
        time_unit_found = []
        for unit in time_unit:
            if (boyer_moore.boyer_moore_string_matching(sentence.lower(), unit.lower())):
                time_unit_found.append(unit)

        if (idIDX == []):
            result = db
        elif (len(time_unit_found) > 1):
            return ["Error"]
        elif (len(time_unit_found) == 1) and len(idIDX) == 1:
            if (time_unit_found[0] == "hari"):
                date += datetime.timedelta(days=int(idIDX[0]))
            elif (time_unit_found[0] == "minggu"):
                date += datetime.timedelta(days=(int(idIDX[0])*7))
            elif (time_unit_found[0] == "bulan"):
                date += datetime.timedelta(days=(int(idIDX[0])*30))
            elif (time_unit_found[0] == "tahun"):
                date += datetime.timedelta(days=(int(idIDX[0])*365))

            for each in db:
                temp = each[0].split("/")
                deadline = datetime.date(
                    int(temp[2]), int(temp[1]), int(temp[0]))

                if (deadline >= today) and (date >= deadline):
                    result += [each]

        else:
            return ["Error"]

    elif (len(list_of_date) == 1):

        for each in db:
            date = list_of_date[0].split('/')
            temp = each[0].split("/")
            date = datetime.date(
                int(date[2]), int(date[1]), int(date[0]))
            deadline = datetime.date(
                int(temp[2]), int(temp[1]), int(temp[0]))
            if (deadline >= today) and (date >= deadline):
                result += [each]


    # Cari deadline yang diantara 2 date itu
    elif (len(list_of_date) == 2):

        for each in db:
            date1 = list_of_date[0].split('/')
            date2 = list_of_date[1].split('/')
            temp = each[0].split("/")
            deadline = datetime.date(
                int(temp[2]), int(temp[1]), int(temp[0]))

            date1 = datetime.date(
                int(date1[2]), int(date1[1]), int(date1[0]))
            date2 = datetime.date(
                int(date2[2]), int(date2[1]), int(date2[0]))

            if (deadline >= min(date1, date2)) and (max(date1, date2) >= deadline):
                result += [each]


    elif (len(list_of_date) > 2):

        return []

    final = []
    code = []
    try:
        code.append(GetInputKodeKuliah(sentence))
    except:
        pass



    if (code == [''] or code == []):

        final = result
    else:

        final = query(result, code, 1)


    if (indeks == 1):

        if (len(match) == 0):
            return query(final, ["Tubes", "Tucil"], 2)
        return query(final, match, 2)
    else:

        if (match == []):

            return final
        elif (len(match) == 1):

            return query(final, match, 2)
        else:
            return ["Error"]


def HandleInput(inputTask):
    # Init local storage
    ListOfTask = []
    # Load File

    try:
        ListOfTask = fileIO.loadTask()
    except Exception:
        pass

    flagFound = ""
    for flag in getFlag():
        if boyer_moore.boyer_moore_string_matching(inputTask.lower(), flag):
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
            try :
                inputDate[0] = DateConverter(inputDate[0])
            except:
                return "Invalid Date Input!"
            if inputDate and inputKodeKuliah and inputKategoriTugas :
                ListOfTask.append([inputDate[0], inputKodeKuliah, inputKategoriTugas, inputDeskripsiTugas, False])
                fileIO.saveTask(ListOfTask)

                output = "[TASK BERHASIL DICATAT]\n<br>"
                output += "(ID: "+str(len(ListOfTask))+") "+str(ListOfTask[-1][0])+" - " + str(
                    ListOfTask[-1][1])+" - "+str(ListOfTask[-1][2]) + " - "+str(ListOfTask[-1][3])+"\n<br>"
                return output
            else:
                return "Invalid Input! No Argument Detected"
    elif("help" in flag) or ("assistant" in flag):
        return """
            [Fitur]<br>
            1. Menambahkan task baru<br>
            2. Melihat daftar task<br>
            3. Melihat deadline dari suatu task<br>
            4. Memperbaharui task<br>
            5. Menandai suatu task sudah selesai<br>
            6. Menampilkan opsi help<br>
            <br>
            [Daftar kata penting]<br>
            1. Kuis<br>
            2. Ujian<br>
            3. Tucil<br>
            4. Tubes<br>
            5. Praktikum<br>
        """
    elif ("deadline" in flag) or ("tugas" in flag):
        result = task_viewer(inputTask, 1, ListOfTask)
        if (result == []):
            return "Tidak ada"
        elif (result == ["Error"]):
            return "Error"
        elif (result == ["Invalid Date Input!"]):
            return "Invalid Date Input!"
        else:
            output = "[Daftar Deadline]\n<br><br>"
            idx = 1
            for each in result:
                output += str(idx) + ". (ID: " + str(each[5]) + ") " + each[0] + \
                    " - " + each[1] + " - " + each[2] + " - " + each[3] + "\n<br>"
                idx += 1
            return output

    elif ("apa saja" in flag) or ("apa aja" in flag):
        result = task_viewer(inputTask, 2, ListOfTask)

        if (result == []):
            return "Tidak ada"
        elif (result == ["Error"]):
            return "Error"
        elif (result == ["Invalid Date Input!"]):
            return "Invalid Date Input!"
        else:
            output = "[Daftar Task]\n<br><br>"
            idx = 1
            for each in result:
                output += str(idx) + ". (ID: " + str(each[5]) + ") " + each[0] + \
                    " - " + each[1] + " - " + each[2] + " - " + each[3] + "\n<br>"
                idx += 1
            return output
    
    elif ("kapan" in flag):
        result = task_viewer(inputTask, 2, ListOfTask)
        if (result == []):
            return "Tidak ada"
        elif (result == ["Error"]):
            return "Error"
        elif (result == ["Invalid Date Input!"]):
            return "Invalid Date Input!"
        else:
            if (len(result) == 1):
                return result[0][0]
            else :
                output = ""
                idx = 1
                for each in result:
                    output += str(idx) + ". (ID: " + str(each[5]) + ") " + each[0] + \
                        " - " + each[1] + " - " + each[2] + " - " + each[3] + "\n<br>"
                    idx+=1
                return output

    elif ("diundur" in flag):
        idIDXList = re.findall("(\w+)\s(\d+)", inputTask)
        idIDX = [id for id in idIDXList if "task" in id[0].lower()]
        idIDX = [id[1] for id in idIDX]

        try:
            tgl_diundur = DateConverter(GetInputDate(inputTask)[0])
        except:
            return "Invalid Date Input!"
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
        idIDXList = re.findall("(\w+)\s(\d+)", inputTask)
        idIDX = [id for id in idIDXList if "task" in id[0].lower()]
        idIDX = [id[1] for id in idIDX]
        found = False
        for i in range(len(ListOfTask)):
            if str(i+1) in (idIDX):
                ListOfTask[i][4] = True
                found = True
        if(not found):
            return "ID Task tidak ditemui"
        fileIO.saveTask(ListOfTask)
        return "Task Berhasil ditandai"

    ListOfTask.append([])



# if __name__ == "__main__":
