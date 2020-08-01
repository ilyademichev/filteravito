from avito_parser import AvitoParser

algorithm = {
    "TASK 0": ["Обнинск","Боровск","Обнинск","Боровск"]
    # "TASK 1":["Москва", "Москва", "Москва"],
    #"TASK 2": ["Обнинск", "Обнинск", "Обнинск"]  # ,
    # "TASK 3":["Москва", "Обнинск", "Москва", "Обнинск","Москва", "Обнинск"]
}
for i in range(0,100):
    try:

        p = AvitoParser()
        p.run_parser_task(algorithm)
    except Exception as e:
        pass
