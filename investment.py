import pandas
data = pandas.read_csv('YNDX_160101_161231.csv', index_col=0)
data_2 = pandas.read_csv('YNDX_150101_151231.csv', index_col=0)
data_all = pandas.concat([data_2, data])
data_all.drop(['<OPEN>', '<CLOSE>'], axis=1, inplace=True)
data_all.reset_index(inplace=True)
data_all['<DATE>'] = pandas.to_datetime(data_all['<DATE>'], format='%Y%m%d', errors='coerce')
data_all['<TIME>'] = pandas.to_datetime(data_all['<TIME>'], format='%H%M%S', errors='coerce')
data_all['<TIME>'] = data_all['<TIME>'].dt.time
data_all['<DATE>'] = data_all['<DATE>'].dt.date

maximum_cost = data_all['<HIGH>'].max()
max_id = data_all['<HIGH>'].idxmax()
max_profit = 0
for i in range(data_all['<HIGH>'].idxmax()):
    current_profit = (maximum_cost - data_all.loc[i, '<LOW>']) * data_all.loc[i, '<VOL>']
    if max_profit < current_profit:
        max_profit = current_profit
        date_of_max = data_all.loc[i, '<DATE>']
        time_of_max = data_all.loc[i, '<TIME>']
        index = i

print("Решение задачи 1 уровня:")
print("1) Покупаем акции", data_all.loc[index, '<DATE>'], "в", data_all.loc[index, '<TIME>'], "в количестве",
data_all.loc[index, '<VOL>'], "по цене", data_all.loc[index, '<LOW>'])
print("2) Продаем акции", data_all.loc[max_id, '<DATE>'], "в", data_all.loc[max_id, '<TIME>'], "по цене",
data_all.loc[max_id, '<HIGH>'])
print("Получаем прибыль в", max_profit)

#----------Решение второй задачи ----------------
print("--------------------\n--------------------\n--------------------")

#Ищем вторую "воронку", где можно купить много дешевых акций
max_profit_2 = 0
for i in range(index + 1, data_all['<HIGH>'].idxmax()):
    current_profit_2 = (maximum_cost - data_all.loc[i, '<LOW>']) * data_all.loc[i, '<VOL>']
    if max_profit_2 < current_profit_2:
        max_profit_2 = current_profit_2
        date_of_max_2 = data_all.loc[i, '<DATE>']
        time_of_max_2 = data_all.loc[i, '<TIME>']
        index_2 = i


# Ищем момент между первой и второй "воронками", когда можно наиболее удачно продать уже имеющиеся акции
max_cost = 0
for i in range(index + 1, index_2 + 1):
    curr_cost = data_all.loc[i, '<HIGH>']
    if max_cost < curr_cost:
        max_cost = curr_cost
        date_of_max_3 = data_all.loc[i, '<DATE>']
        time_of_max_3 = data_all.loc[i, '<TIME>']
        index_3 = i

# max_cost = "пик", найденный между первой и второй "воронками". Таким образом, первый пакет акций
# мы продаем на этом пике, затем на второй "воронке" докупаем акции и продаем на основном пике (задача 1)

profit_1 = (max_cost - data_all.loc[index, '<LOW>']) * data_all.loc[index, '<VOL>']
profit_2 = (data_all.loc[max_id, '<HIGH>'] - data_all.loc[index_2, '<LOW>']) * data_all.loc[index_2, '<VOL>']
print("Решение задачи 2:")
print("1) Покупаем акции", data_all.loc[index, '<DATE>'], "в", data_all.loc[index, '<TIME>'],
"в количестве", data_all.loc[index, '<VOL>'], "по цене", data_all.loc[index, '<LOW>'])
print("2) Продаем акции", data_all.loc[index_3, '<DATE>'], "в", data_all.loc[index_3, '<TIME>'],
"по цене", data_all.loc[index_3, '<LOW>'])
print("3) Покупаем акции", data_all.loc[index_2, '<DATE>'], "в", data_all.loc[index_2, '<TIME>'],
"в количестве", data_all.loc[index_2, '<VOL>'], "по цене", data_all.loc[index_2, '<LOW>'])
print("4) Продаем акции", data_all.loc[max_id, '<DATE>'], "в", data_all.loc[max_id, '<TIME>'],
"по цене", data_all.loc[max_id, '<HIGH>'])
print ("Полученная прибыль = ", profit_1 + profit_2)