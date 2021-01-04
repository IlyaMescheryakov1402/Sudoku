# coding=utf-8
import random
import solver
import pickle

class grid:
    def __init__(self,n = 3):
        """ Generation of the base table """
        self.n = n
        self.table = [[ int((i*n + i/n + j) % (n*n) + 1) for j in range(n*n)] for i in range(n*n)]
        #print("The base table is ready!")

    def __del__(self):
        pass

    def show(self):
        for i in range(self.n*self.n):
            print(self.table[i])

    def transposing(self):
        """ Transposing the whole grid """
        self.table = list(map(list, zip(*self.table)))

    def swap_rows_small(self):
        """ Swap the two rows """
        area = random.randrange(0,self.n,1)
        line1 = random.randrange(0,self.n,1)
        #получение случайного района и случайной строки
        N1 = area*self.n + line1
        #номер 1 строки для обмена

        line2 = random.randrange(0,self.n,1)
        #случайная строка, но не та же самая
        while (line1 == line2):
            line2 = random.randrange(0,self.n,1)

        N2 = area*self.n + line2
        #номер 2 строки для обмена

        self.table[N1], self.table[N2] = self.table[N2], self.table[N1]


    def swap_colums_small(self):
        grid.transposing(self)
        grid.swap_rows_small(self)
        grid.transposing(self)


    def swap_rows_area(self):
        """ Swap the two area horizon """
        area1 = random.randrange(0,self.n,1)
        #получение случайного района

        area2 = random.randrange(0,self.n,1)
        #ещё район, но не такой же самый
        while (area1 == area2):
            area2 = random.randrange(0,self.n,1)

        for i in range(0, self.n):
            N1, N2 = area1*self.n + i, area2*self.n + i
            self.table[N1], self.table[N2] = self.table[N2], self.table[N1]


    def swap_colums_area(self):
        grid.transposing(self)
        grid.swap_rows_area(self)
        grid.transposing(self)

    def mix(self,amt = 10):
        mix_func = ['self.transposing()', 
                    'self.swap_rows_small()', 
                    'self.swap_colums_small()', 
                    'self.swap_rows_area()', 
                    'self.swap_colums_area()']
        for _ in range(1, amt):
            id_func = random.randrange(0,len(mix_func),1)
            eval(mix_func[id_func])
            
    def solve(self, count):
        flook = [[0 for j in range(self.n*self.n)] for i in range(self.n*self.n)] #Заполняем нулями таблицу решения
        iterator = 0
        self.difficult = self.n ** 4 #Первоначально все элементы на месте

        print("---------------------------\n---------------------------\n---------------------------")

        while iterator < self.n ** 4:
            i,j = random.randrange(0, self.n*self.n, 1), random.randrange(0, self.n*self.n, 1) # Выбираем случайную ячейку
            if flook[i][j] == 0:	#Если её не смотрели
                iterator += 1
                flook[i][j] = 1 	#Посмотрим

                temp = self.table[i][j]	#Сохраним элемент на случай если без него нет решения или их слишком много
                self.table[i][j] = 0
                self.difficult -= 1 #Усложняем если убрали элемент

                table_solution = []
                for copy_i in range(0, self.n*self.n):
                    table_solution.append(self.table[copy_i][:]) #Скопируем в отдельный список

                i_solution = 0
                for _ in solver.solve_sudoku((self.n, self.n), table_solution):
                    i_solution += 1 #Считаем количество решений

                if i_solution != 1: #Если решение не одинственное вернуть всё обратно
                    self.table[i][j] = temp
                    self.difficult += 1 # Облегчаем
                
                if self.difficult == count:
                    print("Поле готово! Удачной игры!")
                    break

        if self.difficult != count:
            print("Не удалось сгенерировать. Пока только ", self.difficult, " заполненных ячеек")

def input_check(string):
	while(1):
		try:
			arg_out = int(input(string))
			if arg_out <= 0 or arg_out > 9:
				raise Exception()
			break
		except Exception:
			print("Неверный формат. Попробуйте еще раз")
	return arg_out

def action_input_check(string):
    while(1):
            try:
                arg_choise = int(input(string))
                if arg_choise != 0 and arg_choise != 1:
                    raise Exception()
                break
            except Exception:
                print("Господи, ну тут всего-то надо клацнуть либо на 1, либо на 0. Что сложного то?")
    return arg_choise

def input_cells(string):
    while(1):
            try:
                arg_cells = int(input(string))
                if arg_cells < 0 or arg_cells > 81:
                    raise Exception()
                break
            except Exception:
                print("Неверный формат. Побробуй еще раз. Число должно быть от 0 до 81.\nНо, скорее всего, если число будет меньше 25, то сгенерируется максимальное близкое к этому числу решение")
    return arg_cells

def play_game(example, start_grid):

    game_over = 0
    while (game_over == 0):
        rows_num = input_check("Введите номер строки: ")
        columns_num = input_check("Введите номер колонки: ")
        number = input_check("Введите число: ")

        if start_grid[rows_num - 1][columns_num - 1] == 0: # чтобы нельзя было перезаписать стартовое состояние таблицы
            example.table[rows_num - 1][columns_num - 1] = number
            example.show()
            print("Игра продолжается!")

        else:
            print("Эту ячейку нельзя перезаписывать. Выбери другую")

        pickle.dump(example, open("savefile_example.pkl", "wb"))
        pickle.dump(start_grid, open("savefile_start.pkl", "wb"))

while(1):
    action = action_input_check("Выберите действие:\n[0] Новая игра,\n[1] Загрузка сохранения\n")
    if action == 0:
        newGame = grid()
        newGame.mix()
        #newGame.show() #Раскомментировать, чтобы видеть перед началом матча "ответы"
        print("---------------------------\n---------------------------\n---------------------------")
        newGame.solve(input_cells("Введите количество заполненных ячеек: "))
        newGame.show()

        start_grid = [[newGame.table[i][j] for j in range(newGame.n*newGame.n)] for i in range(newGame.n*newGame.n)] # состояние таблицы на начало игры
        
        play_game(newGame, start_grid)
    else:
        loadGame = pickle.load(open("savefile_example.pkl", "rb"))
        loadGame_start = pickle.load(open("savefile_start.pkl", "rb"))
        print("---------------------------\n---------------------------\n---------------------------")
        loadGame.show()
        play_game(loadGame, loadGame_start)