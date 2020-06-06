import numpy as np

class Preporcessor:
    def __init__(self, filters):
        self._filters =filters


    def preprocess(self, initinal_strings):
        result= list()
        # входной массив обрабатываем поэлементно
        for initinal_string in initinal_strings:
            # если вдруг есть
            result.append(self._process_string(initinal_string))
        return np.concatenate(result)

    def _process_string(self, adress_string):
        result = list()
        # сплтим по переводу строки, если есть
        substrings = [s.lower() for s in adress_string.split('\n')]
        for substring in substrings:
            for one_filter in self._filters:
                substring = one_filter(substring)
            # зздесь вызываем поочердёно фильтры, лежащие в self._filters
            result.append(substring)

        return result


def filter_lower(input_string):
    # тут происходит фильтрация: сплит, выкидывание, склейка. Это самый простой вариант фильтра - пустой :)
    return input_string


# переводит римские числа в арабские
def filter_roman(input_string):
    def roman_to_int(s):
        rom_val = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}
        int_val = 0
        for i in range(len(s)):
            if s[i] not in rom_val:
                return s
            if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
                int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
            else:
                int_val += rom_val[s[i]]
        return str(int_val)

    splited_string = input_string.split(' ')

    for i in range(len(splited_string)):
        splited_string[i] =roman_to_int(splited_string[i])

    result = ' '.join(splited_string)
    return result


# фильтруем названия станций метро и мцк
def filter_stations(input_string):
    splited_string = input_string.split(',')
    for i in range(len(splited_string)):
        w = splited_string[i]
        if (w[:2] == 'м.') or (w[-2:] == ' м') or ('мцк' in w):
            splited_string[i] = ''
    return ','.join(splited_string)


# убираем плохие символы из строки
def filter_bad_signs(input_string):
    input_string = input_string.replace('№', '')
    input_string = input_string.replace('/', '')
    return input_string


# фиксим аббревиатуры
def filter_abb(input_string):
    input_string = input_string.replace('р-он', 'район')
    input_string = input_string.replace('р-н', 'район')
    input_string = input_string.replace('пом.', 'помещение')
    input_string = input_string.replace('корп.', 'корпус')
    input_string = input_string.replace('д. ', 'д.')
    return input_string


def filter_exclam(input_string):
    input_string = input_string.replace('!-', '1-')
    return input_string