import fileIO


def getListOfKataPenting():
    return ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]


def HandleInput(inputTask):
    # Init local storage
    ListOfTask = []
    # Load File
    try:
        ListOfTask = fileIO.loadTask()
    except Exception:
        pass
    # Edit local Storage
    # format task = [date,kode_kuliah,kategori_tugas,deksripsi_tugas,isTaskFinished]
    ListOfTask.append(inputTask)
    # Save to Tasks.db
    fileIO.saveTask(ListOfTask)


if __name__ == "__main__":
    HandleInput(["dd/mm/yyyy", "ZZ9999", getListOfKataPenting()
                 [0], "PlaceHolder Task", False])
