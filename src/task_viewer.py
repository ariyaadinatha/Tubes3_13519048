from boyer_moore import *
from fileIO import *
from handleInput import *
from datetime import date


def time_unit_converter(sentence):
    # Mungkin regex lebih bagus
    time_unit = ["v hari", "hari ini", "besok", "lusa", "x minggu",
                 "minggu depan", "y bulan", "bulan depan", "z tahun", "tahun depan"]
    # value = [       v,        0,        1,     2,        7*x,          7,         30?, ]


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
    sentence = "Apa aja deadline sampai 03-04-2021 04 Juni 2021"
    # input("Sentence: ")

    # if (boyer_moore_string_matching(sentence, "assistant")) or (boyer_moore_string_matching(sentence, "help")) or (boyer_moore_string_matching("bisa apa")):
    #     return []

    # db = loadTask()
    db = [["10/12/2021", "IF9999", "Kuis", "PlaceHolder Task", False], ["12/12/2021", "IF9997",
                                                                        "Tucil", "PlaceHolder Task", False], ["11/12/2021", "IF9998", "Tubes", "PlaceHolder Task", False]]

    kata_penting = getListOfKataPenting()
    match = []
    for kata in kata_penting:
        if (boyer_moore_string_matching(sentence, kata)):
            match += [kata]
    print("match: " + str(match))
    result = []

    # Dari regex
    list_of_date = GetInputDate(sentence)
    list_of_date = [DateConverter(inputDate) for inputDate in list_of_date]
    # for i in range(len(list_of_date)):
    #     list_of_date[i]
    print(list_of_date)
    # date = extract_date_from_regex_moses(date)
    # for now assume
    date = ["11/12/2021"]

    # codes = extract_codes_from_regex_moses(sentence)
    # for now assume
    codes = ["IF9997"]

    # Cari deadline yang > dari date
    if (len(date) == 1):
        # result = query_date_
        pass
    # Cari deadline yang diantara 2 date itu
    elif (len(date) == 2):
        # TODO Query db
        pass
    elif (len(date) > 2):
        # Error g
        return []

    # 1 is the index of codes in database
    result = query(db, codes, 1)

    # Kasus pencarian tugas dengan deadline
    if (boyer_moore_string_matching(sentence, "deadline")):
        # Jika match tidak ada, return semua
        tugas_in_match = [match[i] for i in range(
            len(match)) if match[i] in ["Tubes", "Tucil"]]
        if (tugas_in_match == []):
            return query(result, ["Tubes", "Tucil"], 2)
        else:
            return query(result, tugas_in_match, 2)

    # include ujian, kuis, dan praktikum
    else:
        # Jika match tidak ada, return semua
        if (match == []):
            # if (codes == [] and date == [])
            return result
        else:
            return query(result, match, 2)


print(task_viewer(""))
