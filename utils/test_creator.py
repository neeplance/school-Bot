def test_creator(directory):
    # Вовзращает список списков, построенный на основе полученного файла. Сначала файл делится на списки, резделитель
    # отступ между строками, затем списки делятся на строки, разделитель - новая строка
    with open(directory, encoding='UTF-8') as f:
        content = f.read()
    gg = []
    for g in content.split('\n\n'):
        g = g.split('\n')
        gg.append(g)
    return gg


def file_reader(directory):
    # Вовзращает список списков, построенный на основе полученного файла. Сначала файл делится на списки, резделитель
    # отступ между строками, затем списки делятся на строки, разделитель - новая строка
    with open(directory, encoding='UTF-8') as f:
        content = f.read()
        f.close()
        return content




def name_creator(name):
    # Очищает имя файла от id и расширения
    name1 = name.split('.')
    name1[-1]=''
    name = ''
    for n in name1:
        name += n
    return name
