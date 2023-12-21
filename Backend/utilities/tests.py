# from itertools import permutations
# import numpy as np
# import datetime
#
# BOARD_SIZE = 8
#
# # def eight_queens(board_size):
# #     columns = range(board_size)
# #     for positions in permutations(columns):
# #         if (board_size == len(set(positions[i] + i for i in columns))
# #                 == len(set(positions[i] - i for i in columns))):
# #             pass
# #             # print(positions)
# #
# #
# # start = datetime.datetime.now()
# # eight_queens(BOARD_SIZE)
# # end = datetime.datetime.now()
# # duration = end - start
# # print('The time of permutations is: ', duration)
#
# # ---------------------------------------------------------------------
# # Queen = np.zeros((BOARD_SIZE, BOARD_SIZE))
# count = 0
#
#
# def check(row, column, BOARD_SIZE, Queen):
#     # 检查行列
#     for k in range(BOARD_SIZE):
#         if Queen[k][column] == 1:
#             return False
#
#     # 检查主对角线
#
#     for i, j in zip(range(row - 1, -1, -1), range(column - 1, -1, -1)):
#         if Queen[i][j] == 1:
#             return False
#
#             # 检查副对角线
#     for i, j in zip(range(row - 1, -1, -1), range(column + 1, BOARD_SIZE)):
#         if Queen[i][j] == 1:
#             return False
#
#     return True
#
#
# def print_queen(BOARD_SIZE, Queen):
#     print(Queen)
#     for i in range(BOARD_SIZE):
#         for j in range(BOARD_SIZE):
#             if Queen[i][j] == 1:
#                 print('☆ ' * j + '★ ' + '☆ ' * (7 - j))
#     print("\n\n")
#
#
# def find_Queen(row, BOARD_SIZE, Queen):
#     if row > BOARD_SIZE - 1:
#         global count
#         count = count + 1
#         # print_queen(BOARD_SIZE, Queen)
#         return
#
#     for column in range(BOARD_SIZE):
#         if check(row, column, BOARD_SIZE, Queen):
#             Queen[row][column] = 1
#             find_Queen(row + 1, BOARD_SIZE, Queen)
#             Queen[row][column] = 0
#
#
# for BOARD_SIZE in range(4, 13):
#     Queen = np.zeros((BOARD_SIZE, BOARD_SIZE))
#     start = datetime.datetime.now()
#     find_Queen(0, BOARD_SIZE, Queen)
#     end = datetime.datetime.now()
#     duration = end - start
#     print('%d*%d： ------> solutions: %d, time:  ' % (BOARD_SIZE, BOARD_SIZE, count), duration)
#
#
# # 使用遗传算法求解八皇后问题
# import random
# import numpy as np
# import datetime
#
#
# # eight queens problems
# class EightQueens:
#     def __init__(self, size):
#         self.size = size
#         self.population = []
#         self.fitness = []
#         self.best = []
#         self.best_fitness = 0
#         self.best_fitness_list = []
#         self.best_fitness_list.append(self.best_fitness)
#
#     def init_population(self, population_size):
#         self.population = []
#         for i in range(population_size):
#             chromosome = []
#             for j in range(self.size):
#                 chromosome.append(random.randint(0, self.size - 1))
#             self.population.append(chromosome)
#
#     def fitness_function(self):
#         self.fitness = []
#         for i in range(len(self.population)):
#             chromosome = self.population[i]
#             fitness = 0
#             for j in range(self.size - 1):
#                 for k in range(j + 1, self.size):
#                     if chromosome[j] == chromosome[k]:
#                         fitness += 1
#                     if abs(chromosome[j] - chromosome[k]) == abs(j - k):
#                         fitness += 1
#             self.fitness.append(fitness)
#
#     def select(self):
#         self.best_fitness = min(self.fitness)
#         self.best_fitness_list.append(self.best_fitness)
#         index = self.fitness.index(self.best_fitness)
#         self.best = self.population[index]
#         new_population = []
#         for i in range(len(self.population)):
#             if self.fitness[i] == self.best_fitness:
#                 new_population.append(self.population[i])
#         self.population = new_population
#
#     def crossover(self):
#         new_population = []
#         for i in range(len(self.population)):
#             for j in range(i + 1, len(self.population)):
#                 chromosome1 = self.population[i]
#                 chromosome2 = self.population[j]
#                 new_chromosome1 = []
#                 new_chromosome2 = []
#                 for k in range(self.size):
#                     if random.random() < 0.5:
#                         new_chromosome1.append(chromosome1[k])
#                         new_chromosome2.append(chromosome2[k])
#                     else:
#                         new_chromosome1.append(chromosome2[k])
#                         new_chromosome2.append(chromosome1[k])
#                 new_population.append(new_chromosome1)
#                 new_population.append(new_chromosome2)
#         self.population = new_population
#
#     def mutation(self):
#         for i in range(len(self.population)):
#             chromosome = self.population[i]
#             for j in range(self.size):
#                 if random.random() < 0.05:
#                     chromosome[j] = random.randint(0, self.size - 1)
#
#     def run(self, population_size, max_generation):
#         self.init_population(population_size)
#         for i in range(max_generation):
#             self.fitness_function()
#             self.select()
#             self.crossover()
#             self.mutation()
#         return self.best_fitness_list
#
#     def print_best(self):
#         print('best fitness: ', self.best_fitness)
#         print('best chromosome: ', self.best)
#         for i in range(self.size):
#             for j in range(self.size):
#                 if self.best[i] == j:
#                     print('★', end='')
#                 else:
#                     print('☆', end='')
#             print()
#         print()
#
#     def print_best_fitness(self):
#         print(self.best_fitness_list)
#
#     def print_best_fitness_plot(self):
#         import matplotlib.pyplot as plt
#         plt.plot(self.best_fitness_list)
#         plt.show()
#
#
#
#
#
#
#
#
