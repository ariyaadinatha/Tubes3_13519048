import fileIO
import boyer_moore
import re
import datetime


def getListOfKataPenting():
    # Mengembalikan Daftar Kata Penting
    return ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]


def getFlag():
    # Mengembalikan Daftar Flag Kata Kunci
    return ["help", "assistant", "undur","maju","ubah", "selesai", "kapan", "deadline", "tugas", "apa saja", "apa aja"]


def GetInputDate(inputTask):
    # Mengembalikan list berupa tanggal dari teks masukan user
    # Mendapatkan tanggal dengan regex
    inputDate = re.findall(
        "(\d{1,2}).(\d{1,2}).(\d{2,4})|(\d{1,2}).(\w+).(\d{4})", inputTask)
    
    # Memfilter hasil search dengan regex supaya bersih dari empty space
    filteredDate = []
    for date in inputDate:
        filteredData = []
        for data in date:
            if len(data) != 0:
                filteredData.append(data)
        filteredDate.append(filteredData)
    
    # return
    return (filteredDate)


def DateConverter(inputListDate):
    # Inisialisasi daftar bulan
    ListOfMonths = ["januari", "februari", "maret", "april", "mei", "juni",
                    "juli", "agustus", "september", "oktober", "november", "desember"]

    # Cek apakah masukan bulan berupa angka
    try:
        intMonth = int(inputListDate[1])
        # proses masukan bulan jika angka
        if(len(inputListDate[2])==2):
            inputListDate[2] = "20" + inputListDate[2]
        return datetime.datetime(int(inputListDate[2]), intMonth, int(inputListDate[0])).strftime("%d/%m/%Y")
    except:
        pass
    
    # proses masukan bulan jika bukan angka
    i = 0
    while i < (len(ListOfMonths)):
        if inputListDate[1].lower() == ListOfMonths[i]:
            break
        i += 1
    # Jika tidak ditemukan bulan, throw exception
    if i == 12:
        raise Exception("Invalid Date Input!")
    # return tanggal 
    return datetime.datetime(int(inputListDate[2]), i+1, int(inputListDate[0])).strftime("%d/%m/%Y")


def GetInputKodeKuliah(inputTask):   
    # Ambil Kode Kuliah dengan regex dari input user
    task = re.search(
        "([a-zA-Z][a-zA-Z]\d{4})", inputTask)
    # Jika tidak temukan kembalikan teks kosong
    if task is None:
        return ""
    # Jika ditemukan proses hasil pencarian regex dan kembalikan kode kuliah
    else:
        task = task.group().strip(" pada")
        inputKodeKuliah = re.search(
            "([a-zA-Z][a-zA-Z]\d{4})", task).group()
        return inputKodeKuliah


def GetInputDeskripsiTugas(inputTask):
    # Ambil Deskripsi Task dengan regex dari input user
    task = re.search(
        "([a-zA-Z][a-zA-Z]\d{4})(.(\w*))*(?=\s(\d{1,2}).(\d{1,2}).(\d{2,4})|\s(\d{1,2}).(\w+).(\d{4}))", inputTask)
     # Jika tidak temukan kembalikan keterangan tidak ditemukan
    if task is None:
        return "No description provided"
        
    # Jika ditemukan proses hasil pencarian regex dan kembalikan Deskripsi Task
    task = task.group().strip(" pada")
    temp = re.search(
        "(?<=([a-zA-Z][a-zA-Z]\d{4}\s))(.(\w*))*", task)
    if (temp is None):
        return "No description provided"
    return temp.group()


def GetKategoriTugas(inputTask):
    # Mengembalikan Kategori Tugas dari input user dengan Algoritam String Match Boyer Moore
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
    # Mengambil list kata penting
    kata_penting = getListOfKataPenting()
    # Container untuk daftar kata penting yang dimasukkan oleh user
    match = []

    # Mengambil kata penting yang dimasukkan user
    for kata in kata_penting:
        if (boyer_moore.boyer_moore_string_matching(sentence.lower(), kata.lower())):
            match += [kata]

    # Indeks = 1 artinya dicari yang berkategori tugas (hanya tubes dan tucil), jika ada match yang bukan tampilkan pesan error
    if (indeks == 1):
        for kata in match:
            if (kata not in ["Tubes", "Tucil"]):
                return ["Error"]
    
    # Isi dataabse dengan ID untuk dipakai nanti
    for i in range(len(database)):
        database[i].append(i+1)
    # Ambil task dari database yang belum selesai
    db = []
    for data in database:
        if (not data[4]):
            db += [data]
    # Cari input yang berupa tanggal
    list_of_date = GetInputDate(sentence)
    try :
        list_of_date = [DateConverter(inputDate) for inputDate in list_of_date]
    except:
        return ["Invalid Date Input!"]

    result = []
    today = datetime.date.today()
    # Jika tidak ditemukan tanggal, kemungkinan ada keterangan waktu yang tidak straightforward, misalnya: "minggu depan"
    if (len(list_of_date) == 0):
        # Pemetaan dari keterangan waktu menuju value nya
        date = datetime.date.today()
        special_time = ["besok", "lusa", "minggu depan",
                        "bulan depan", "tahun depan", "hari ini", "minggu ini", "bulan ini", "tahun ini"]
        special_time_value = ["1 hari", "2 hari",
                              "7 hari", "1 bulan", "1 tahun", "1 hari", "7 hari", "1 bulan", "1 tahun"]
        for i in range(len(special_time)):
            sentence = sentence.replace(special_time[i], special_time_value[i])

        # Definisikan time unit dan cari kemunculannya di input user
        time_unit = ["hari", "minggu", "bulan", "tahun"]
        idIDX = re.findall("(?<=\s)(\d+)(?=\s)", sentence)
        time_unit_found = []
        for unit in time_unit:
            if (boyer_moore.boyer_moore_string_matching(sentence.lower(), unit.lower())):
                time_unit_found.append(unit)

        # Jika tidak ditemukan time unit, tidak ada filtering apapun
        if (idIDX == []):
            result = db
        # Jika ditemukan lebih dari 1 time unit, maka error
        elif (len(time_unit_found) > 1):
            return ["Error"]
        # Jika ditemukan 1 dan ada 1 keterangan nilai dari time unit, maka kalkulasikan date yang dimaksud
        elif (len(time_unit_found) == 1) and len(idIDX) == 1:
            if (time_unit_found[0] == "hari"):
                date += datetime.timedelta(days=int(idIDX[0]))
            elif (time_unit_found[0] == "minggu"):
                date += datetime.timedelta(days=(int(idIDX[0])*7))
            elif (time_unit_found[0] == "bulan"):
                date += datetime.timedelta(days=(int(idIDX[0])*30))
            elif (time_unit_found[0] == "tahun"):
                date += datetime.timedelta(days=(int(idIDX[0])*365))
            # Query db yang memiliki tanggal yang cocok
            for each in db:
                temp = each[0].split("/")
                deadline = datetime.date(
                    int(temp[2]), int(temp[1]), int(temp[0]))

                if (deadline >= today) and (date >= deadline):
                    result += [each]
        # Sisanya maka error
        else:
            return ["Error"]
    # Jika ditemukan 1 tanggal, maka filter task di db yang tanggal nya <= dari tanggal yang dimasukkan user dan >= dari tanggal sekarang      
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


    # Jika ada 2 tanggal, cari task dengan deadline yang berada diantara 2 date itu
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

    # Jika ada lebih dari 2 tanggal berikan pesan error
    elif (len(list_of_date) > 2):
        return []

    # Bagian filtering kode kuliah
    final = []
    code = []
    # Ambil kode kuliah dari input user
    try:
        code.append(GetInputKodeKuliah(sentence))
    except:
        pass

    # Jika tidak ada maka tidak ada query apapun
    if (code == [''] or code == []):

        final = result
    # Jika ada cari yang sesuai di result
    else:
        final = query(result, code, 1)

    # Jika pencarian sekarang deadline, maka hanya melayani tugas
    if (indeks == 1):
        if (len(match) == 0):
            return query(final, ["Tubes", "Tucil"], 2)
        return query(final, match, 2)
    # Jika tidak, maka tidak ada query terpisah, cukup dengan match
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
    
    # Cek Kata Penting
    flagFound = ""
    for flag in getFlag():
        if boyer_moore.boyer_moore_string_matching(inputTask.lower(), flag):
            flagFound = (flag)
            break
        
    # Jika tidak ditemukan flag, asumsi user ingin menambahkan task
    if len(flagFound) == 0:
        # Ambil tanggal, kode kuliah, kategori task ,dan deskripsi task dari input user
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
            
            # Jika tanggal, kode kuliah,dan kategori task ditemukan , tambah kedatabase dan berikan respon ke user
            if inputDate and inputKodeKuliah and inputKategoriTugas :
                # Tambah Task Ke Database
                ListOfTask.append([inputDate[0], inputKodeKuliah, inputKategoriTugas, inputDeskripsiTugas, False])
                fileIO.saveTask(ListOfTask)
                # Berikan Respon Ke User
                output = "[TASK BERHASIL DICATAT]\n<br>"
                output += "(ID: "+str(len(ListOfTask))+") "+str(ListOfTask[-1][0])+" - " + str(
                    ListOfTask[-1][1])+" - "+str(ListOfTask[-1][2]) + " - "+str(ListOfTask[-1][3])+"\n<br>"
                return output
            else:
                return "Invalid Input! No Argument Detected"
    # Jika ditemukan flag "help" atau "assistant", kembalikan respon berupa daftar fitur dan daftar kata penting
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
    # Jika ditemukan flag "deadline" atau "tugas" pada input user
    elif ("deadline" in flag) or ("tugas" in flag):
        # result diambil dari fungsi task_viewer, dimana indeks 1 mengkhususkan katergori tugas (tubes, tucil)
        result = task_viewer(inputTask, 1, ListOfTask)
        # Jika hasil kosong
        if (result == []):
            return "Tidak ada"
        # Jika hasil error karena hal tertentu
        elif (result == ["Error"]):
            return "Error"
        # Jika hasil error karena kesalahan tanggal
        elif (result == ["Invalid Date Input!"]):
            return "Invalid Date Input!"
        # Jika tidak ada error, tampilkan daftar deadline yang sesuai
        else:
            output = "[Daftar Deadline]\n<br><br>"
            idx = 1
            for each in result:
                output += str(idx) + ". (ID: " + str(each[5]) + ") " + each[0] + \
                    " - " + each[1] + " - " + each[2] + " - " + each[3] + "\n<br>"
                idx += 1
            return output

    # Jika ditemukan flag "apa saja" atau "apa aja"
    elif ("apa saja" in flag) or ("apa aja" in flag):
        # Memanggil fungsi task_viewer dengan indeks 2, yakni filter seluruh tipe task
        result = task_viewer(inputTask, 2, ListOfTask)
        # Jika hasil kosong
        if (result == []):
            return "Tidak ada"
        # Jika hasil error karena hal tertentu
        elif (result == ["Error"]):
            return "Error"
        # Jika hasil error karena kesalahan tanggal
        elif (result == ["Invalid Date Input!"]):
            return "Invalid Date Input!"
        # Jika tidak ada error, tampilkan daftar task yang sesuai
        else:
            output = "[Daftar Task]\n<br><br>"
            idx = 1
            for each in result:
                output += str(idx) + ". (ID: " + str(each[5]) + ") " + each[0] + \
                    " - " + each[1] + " - " + each[2] + " - " + each[3] + "\n<br>"
                idx += 1
            return output
    
    # Jika ditemukan flag "kapan" pada input user
    elif ("kapan" in flag):
        # Memanggil fungsi task_viewer dengan indeks 2, yakni filter seluruh tipe task
        result = task_viewer(inputTask, 2, ListOfTask)
        # Jika hasil kosong
        if (result == []):
            return "Tidak ada"
        # Jika hasil error karena hal tertentu
        elif (result == ["Error"]):
            return "Error"
        # Jika hasil error karena kesalahan tanggal
        elif (result == ["Invalid Date Input!"]):
            return "Invalid Date Input!"
        # Jika tidak ada error, tampilkan daftar task yang sesuai
        else:
            # Jika hanya ada 1 hasil, langsung tuliskan tanggalnya
            if (len(result) == 1):
                return result[0][0]
            # Jika lebih, tuliskan seluruh detailnya
            else :
                output = ""
                idx = 1
                for each in result:
                    output += str(idx) + ". (ID: " + str(each[5]) + ") " + each[0] + \
                        " - " + each[1] + " - " + each[2] + " - " + each[3] + "\n<br>"
                    idx+=1
                return output
    
    # Jika ditemukan flag "undur" ,"maju",atau "ubah", proses input untuk mengubah deadline task
    elif ("undur" in flag) or ("maju" in flag)or ("ubah" in flag):
        # Ambil id Task dengan regex
        idIDXList = re.findall("(\w+)\s(\d+)", inputTask)
        idIDX = [id for id in idIDXList if "task" in id[0].lower()]
        idIDX = [id[1] for id in idIDX]
        
        # Ambil tanggal baru dari input user
        try:
            tgl_diundur = DateConverter(GetInputDate(inputTask)[0])
        except:
            return "Invalid Date Input!"
        
        # Cek Apakah id task Ada pada database
        found = False
        for i in range(len(ListOfTask)):
            if str(i+1) in (idIDX):
                ListOfTask[i][0] = tgl_diundur
                found = True
        
        # Kembalikan pesan error jika tidak ditemui
        if(not found):
            return "ID Task tidak ditemui"
        
        # Simpan perubahan tanggal pada database jika ditemui
        fileIO.saveTask(ListOfTask)
        
        # Kembalikan respon berhasil
        return "Task Berhasil Di Update"
    
    # Jika ditemukan flag "selesai", proses input untuk mengubah status kesudahan task menjadi sudah selesai
    elif ("selesai" in flag):
        # Ambil id Task dengan regex
        idIDXList = re.findall("(\w+)\s(\d+)", inputTask)
        idIDX = [id for id in idIDXList if "task" in id[0].lower()]
        idIDX = [id[1] for id in idIDX]
        
        # Cek Apakah id task Ada pada database
        found = False
        for i in range(len(ListOfTask)):
            if str(i+1) in (idIDX):
                ListOfTask[i][4] = True
                found = True

        # Kembalikan pesan error jika tidak ditemui
        if(not found):
            return "ID Task tidak ditemui"
        
         # Simpan perubahan status pada database jika ditemui
        fileIO.saveTask(ListOfTask)
        
        # Kembalikan respon berhasil
        return "Task Berhasil ditandai"

    ListOfTask.append([])


