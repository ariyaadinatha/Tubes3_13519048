import fileIO
import boyer_moore
import re
import datetime


def getListOfKataPenting():
    return ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]


def getFlag():
    # TODO : Lengkapin Flag
    return ["deadline", "help", "assistant", "diundur"]


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
    print(filteredDate)
    return (filteredDate)


def DateConverter(inputListDate):
    ListOfMonths = ["januari", "februari", "maret", "april", "mei", "juni",
                    "juli", "agu2stus", "september", "oktober", "november", "desember"]
    print(inputListDate)
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
    return datetime.datetime(inputListDate[2], i, inputListDate[0]).strftime("%d/%m/%Y")


def GetInputKodeKuliah(inputTask):
    task = re.search(
        "([a-zA-Z][a-zA-Z]\d{4})(.(\w*))*(?=\s(\d{1,2}).(\d{1,2}).(\d{4})|\s(\d{1,2}).(\w+).(\d{4}))", inputTask)
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


def HandleInput(inputTask):
    # Init local storage
    ListOfTask = []
    # Load File
    try:
        ListOfTask = fileIO.loadTask()
    except Exception:
        pass

    flagFound = []
    for flag in getFlag():
        if boyer_moore.boyer_moore_string_matching(inputTask, flag):
            flagFound.append(flag)
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
                print("Befero Append")
                ListOfTask.append([DateConverter(
                    inputDate[0]), inputKodeKuliah, inputKategoriTugas, inputDeskripsiTugas, False])
                print("after Append")
                fileIO.saveTask(ListOfTask)

                output = "[TASK BERHASIL DICATAT]\n"
                output += "(ID: "+str(len(ListOfTask))+") "+str(ListOfTask[-1][0])+" - " + str(
                    ListOfTask[-1][1])+" - "+str(ListOfTask[-1][2]) + " - "+str(ListOfTask[-1][3])+"\n"
                return output
            else:
                return "Invalid Input1"

    ListOfTask.append([])
    print(ListOfTask)


if __name__ == "__main__":

    print(HandleInput("Tubes IF2211 String Matching pada 14-02-2021"))

# for j in range(len(ListOfTask)):
#                         output+=str(j+1)+" "+ListOfTask[j][0]+" - "+ListOfTask[j][1]+" - "+ListOfTask[j][2]+" - "+ListOfTask[j][3]+"\n"
#                     return output
