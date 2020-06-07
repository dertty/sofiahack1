import numpy as np


class Preporcessor:
  def __init__(self, filters):
    self._filters=filters


  def preprocess(self, initinal_strings):
    result= list()
    #входной массив обрабатываем поэлементно
    for initinal_string in initinal_strings:
      #если вдруг есть
      result.append(self._process_string(initinal_string))
    return np.concatenate(result)

  def _process_string(self, adress_string):
    result = list()
    #сплтим по переводу строки, если есть
    addresses = [s.lower() for s in adress_string.split('\n')]
    for address in addresses:
      #разобьём адрес на кусочки по запятым
      address_parts = [ap.strip() for ap in address.split(',')]
      for i in range(len(address_parts)):
        for one_filter in self._filters:
          address_parts[i] = one_filter(address_parts[i])

      address_fixed = ','.join([ap for ap in address_parts if len(ap)>0])
      #здесь вызываем поочердёно фильтры, лежащие в self._filters
      result.append(address_fixed)

    return result


#переводит римские числа в арабские
def filter_roman(input_string):
  def roman_to_int(s):
    if len(s)==0:
      return ''
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
    splited_string[i] = roman_to_int(splited_string[i] )

  result = ' '.join(splited_string)
  return result

# фильтруем названия станций метро и мцк
def filter_stations(input_string):
  splited_string = input_string.split(',')
  for i in range(len(splited_string)):
    w = splited_string[i]
    if (w[:2]=='м.') or (w[:3]==' м.') or (w[-2:]==' м') or ('мцк' in w) or ('ст.' in w) :
      splited_string[i]=''
  return ''.join(splited_string)


# убираем плохие символы из строки
def filter_bad_signs(input_string):
  input_string = input_string.replace('№','')
  input_string = input_string.replace('/','\\')
  input_string = input_string.replace('"','')
  return input_string

# фиксим аббревиатуры
def filter_abb(input_string):
  input_string = input_string.replace('р-он','район')
  input_string = input_string.replace('р-н','район')
  input_string = input_string.replace('пом.','помещение ')
  #input_string = input_string.replace('пом ','помещение')
  input_string = input_string.replace('корп.','корпус ')
  #input_string = input_string.replace('корп ','корпус')
  input_string = input_string.replace('д. ','дом ')
  #input_string = input_string.replace('д ','дом ')
  input_string = input_string.replace('стр. ','строение ')
  #input_string = input_string.replace('стр ','строение ')
  return input_string

#фиксим плохие знаки
def filter_exclam(input_string):
  input_string = input_string.replace('!-', '1-')
  input_string = input_string.replace('!', '')
  return input_string