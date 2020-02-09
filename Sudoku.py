import numpy as np
import copy
import time

NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
MAX_EPOCHS = 100


class Sudoku:
    deepness = 0
    variation = 0
    values = np.empty((9, 9), int)
    possibilities = {}

    def solve(self):
        self.initialize_all_values()

        epoch = 0
        solved = False

        while epoch <= MAX_EPOCHS and not solved:
            print("\nEpoch", epoch + 1)
            self.clear_values()

            ''' Elimination '''
            advancing, solvable = self.assign_values()
            self.clear_values()
            if not solvable:
                return False

            solved = self.check_solved()
            if solved:
                return True

            ''' Placement possibilities '''
            if not advancing:
                print("I am not advancing by elimination.",
                      "\nLet's do it by placement possibilities!")
                advancing = self.check_lonely()
                self.clear_values()

                solved = self.check_solved()
                if solved:
                    return True

                if not advancing:
                    print("I am not advancing at all :( \n"
                          "I will try it by brute force.")
                    sudoku_solved = self.solve_by_brute_force()
                    return sudoku_solved
                else:
                    print("\nUpdate by placement:")
                    self.print_values()

            else:
                print("\nUpdate by elimination:")
                self.print_values()

            epoch += 1

    def solve_by_brute_force(self):
        for index in self.possibilities:
            possibilities = self.possibilities[index]
            if type(possibilities) == list:
                sudokus = self.split_in_several_possibilities(index)
                for sudoku in sudokus:
                    solvable = sudoku.solve()
                    if solvable is not None:
                        if solvable:
                            return True

    def split_in_several_possibilities(self, index):
        print("I split the sudoku in several possibilities for the", index,
              "slot:")
        possibilities = self.possibilities[index]
        sudokus = list()
        for i in range(len(possibilities)):
            number = possibilities[i]
            sudoku_variation = self.copy_sudoku()
            sudoku_variation.deepness += 1
            sudoku_variation.variation = i+1
            sudoku_variation.assign_value(index[0], index[1], number)
            sudoku_variation.clear_values()
            sudoku_variation.print_values()
            sudokus.append(sudoku_variation)

        return sudokus

    def check_solved(self):
        solved = True
        for i in range(9):
            for j in range(9):
                if self.values[i, j] not in NUMBERS:
                    solved = False

        if solved:
            print("\nThe Sudoku is solved!")
            print("Final Sudoku:")
            self.print_values()
            return True
        else:
            return False

    def check_lonely(self):
        advancing = False

        """ Check in row """
        for i in range(9):
            amounts = np.zeros(9)
            for j in range(9):
                possibilities = self.possibilities[(i, j)]
                if type(possibilities) == list:
                    for possibility in possibilities:
                        amounts[possibility-1] += 1

            for pre_num, amount in enumerate(amounts):
                if amount == 1:
                    number = pre_num + 1
                    for j in range(9):
                        possibilities = self.possibilities[(i, j)]
                        if type(possibilities) == list:
                            if number in possibilities:
                                print("The only possibility in the row",
                                      i, " for the number", number,
                                      "is the slot", (i, j))
                                self.assign_value(i, j, number)
                    advancing = True

        """ Check in column """
        for j in range(9):
            amounts = np.zeros(9)
            for i in range(9):
                possibilities = self.possibilities[(i, j)]
                if type(possibilities) == list:
                    for possibility in possibilities:
                        amounts[possibility-1] += 1

            for pre_num, amount in enumerate(amounts):
                if amount == 1:
                    number = pre_num + 1
                    for i in range(9):
                        possibilities = self.possibilities[(i, j)]
                        if type(possibilities) == list:
                            if number in possibilities:
                                print("The only possibility in the column",
                                      j, " for the number", number,
                                      "is the slot", (i, j))
                                self.assign_value(i, j, number)
                    advancing = True

        """ Check in block """
        for a in range(3):
            for b in range(3):
                amounts = np.zeros(9)
                for ref_i in range(3):
                    for ref_j in range(3):
                        i = a * 3 + ref_i
                        j = a * 3 + ref_j
                        possibilities = self.possibilities[(i, j)]
                        if type(possibilities) == list:
                            for possibility in possibilities:
                                amounts[possibility - 1] += 1

                for pre_num, amount in enumerate(amounts):
                    if amount == 1:
                        number = pre_num + 1
                        for ref_i in range(3):
                            for ref_j in range(3):
                                i = a * 3 + ref_i
                                j = a * 3 + ref_j
                                possibilities = self.possibilities[(i, j)]
                                if type(possibilities) == list:
                                    if number in possibilities:
                                        print("The only possibility in the",
                                              "block", (a, b), "for the number"
                                              , number, "is the slot", (i, j))
                                        self.assign_value(i, j, number)
                        advancing = True

        return advancing

    def clear_values(self):
        for i in range(9):
            for j in range(9):
                if self.values[i, j] in NUMBERS:
                    self.remove_values(i, j)

    def assign_values(self):
        advancing = False
        solvable = True
        for i in range(9):
            for j in range(9):
                possibilities = self.possibilities[(i, j)]
                if type(possibilities) == list:
                    if len(possibilities) == 1:
                        number = possibilities[0]
                        print("The only possibility in the slot",
                              (i, j), "is the number", number)
                        advancing = self.assign_value(i, j, number)
                    elif len(possibilities) == 0:
                        print("This sudoku is unsolvable!")
                        solvable = False
        return advancing, solvable

    def copy_sudoku(self):
        new_sudoku = Sudoku()
        new_sudoku.values = copy.copy(self.values)
        new_sudoku.possibilities = copy.copy(self.possibilities)
        new_sudoku.deepness = self.deepness
        new_sudoku.variation = 0
        return new_sudoku

    def assign_value(self, i, j, number):
        self.values[i, j] = number
        self.possibilities[(i, j)] = number
        self.clear_values()
        return True

    def initialize_all_values(self):
        for i in range(9):
            for j in range(9):
                if self.values[i, j] in NUMBERS:
                    self.possibilities[(i, j)] = self.values[i, j]
                else:
                    self.possibilities[(i, j)] = list(NUMBERS)

    def remove_values(self, i, j):
        number = self.values[i, j]
        # print("Removing from", (i, j))

        """ Remove in row """
        for k in range(9):
            possibilities = self.possibilities[(i, k)]
            if type(possibilities) == list:
                # print(possibilities)
                try:
                    possibilities.remove(number)
                except ValueError:
                    pass
                # print(possibilities)

        """ Remove in column """
        for k in range(9):
            possibilities = self.possibilities[(k, j)]
            if type(possibilities) == list:
                # print(possibilities)
                try:
                    possibilities.remove(number)
                except ValueError:
                    pass
                # print(possibilities)

        """ Remove in block """
        ref_i, ref_j = 3 * (i//3), 3 * (j//3)
        # print(ref_i, ref_j)
        for a in range(3):
            for b in range(3):
                possibilities = self.possibilities[(ref_i + a, ref_j + b)]
                if type(possibilities) == list:
                    # print(possibilities)
                    try:
                        possibilities.remove(number)
                    except ValueError:
                        pass
                    # print(possibilities)

    def assign_example(self, index):
        if index == 1:
            self.values[0, 7] = 7
            self.values[1, 4] = 5
            self.values[1, 6] = 8
            self.values[1, 8] = 1
            self.values[2, 2] = 6
            self.values[2, 3] = 4
            self.values[2, 4] = 1
            self.values[2, 7] = 3
            self.values[2, 8] = 5
            self.values[3, 0] = 6
            self.values[3, 2] = 7
            self.values[3, 6] = 5
            self.values[3, 7] = 2
            self.values[4, 3] = 2
            self.values[4, 5] = 9
            self.values[5, 1] = 4
            self.values[5, 2] = 1
            self.values[5, 6] = 6
            self.values[5, 8] = 9
            self.values[6, 0] = 9
            self.values[6, 1] = 7
            self.values[6, 4] = 2
            self.values[6, 5] = 1
            self.values[6, 6] = 4
            self.values[7, 0] = 1
            self.values[7, 2] = 5
            self.values[7, 4] = 3
            self.values[8, 1] = 8
        elif index == 2:
            self.values[0, 3] = 6
            self.values[0, 4] = 4
            self.values[0, 7] = 3
            self.values[0, 8] = 5
            self.values[1, 0] = 5
            self.values[1, 1] = 3
            self.values[1, 2] = 6
            self.values[1, 3] = 7
            self.values[2, 1] = 7
            self.values[2, 3] = 5
            self.values[2, 5] = 2
            self.values[2, 7] = 6
            self.values[2, 8] = 8
            self.values[3, 2] = 7
            self.values[3, 6] = 3
            self.values[4, 2] = 2
            self.values[4, 4] = 6
            self.values[5, 0] = 1
            self.values[5, 1] = 9
            self.values[5, 3] = 4
            self.values[5, 5] = 7
            self.values[5, 7] = 5
            self.values[5, 8] = 6
            self.values[6, 0] = 3
            self.values[6, 1] = 6
            self.values[6, 2] = 8
            self.values[6, 8] = 7
            self.values[7, 3] = 3
            self.values[7, 5] = 6
            self.values[7, 6] = 1
            self.values[7, 8] = 9
            self.values[8, 0] = 9
            self.values[8, 3] = 2
            self.values[8, 5] = 8
            self.values[8, 7] = 4
            self.values[8, 8] = 3
        elif index == 3:
            self.values[0, 0] = 1
            self.values[0, 4] = 2
            self.values[0, 5] = 3
            self.values[0, 8] = 5
            self.values[1, 2] = 6
            self.values[1, 3] = 7
            self.values[1, 6] = 4
            self.values[2, 3] = 1
            self.values[2, 4] = 4
            self.values[2, 7] = 7
            self.values[3, 2] = 3
            self.values[3, 6] = 5
            self.values[3, 8] = 2
            self.values[4, 4] = 8
            self.values[5, 0] = 4
            self.values[5, 2] = 9
            self.values[5, 6] = 8
            self.values[6, 1] = 7
            self.values[6, 4] = 5
            self.values[6, 5] = 4
            self.values[7, 2] = 4
            self.values[7, 5] = 6
            self.values[7, 6] = 7
            self.values[8, 0] = 6
            self.values[8, 3] = 2
            self.values[8, 4] = 1
            self.values[8, 8] = 9
        elif index == 4:
            self.values[0, 2] = 6
            self.values[0, 3] = 4
            self.values[0, 4] = 9
            self.values[1, 3] = 1
            self.values[1, 5] = 2
            self.values[1, 8] = 8
            self.values[2, 2] = 9
            self.values[2, 6] = 3
            self.values[2, 7] = 4
            self.values[3, 0] = 1
            self.values[3, 2] = 2
            self.values[3, 7] = 9
            self.values[4, 4] = 6
            self.values[5, 1] = 6
            self.values[5, 6] = 8
            self.values[5, 8] = 5
            self.values[6, 1] = 7
            self.values[6, 2] = 4
            self.values[6, 6] = 5
            self.values[7, 0] = 2
            self.values[7, 3] = 3
            self.values[7, 5] = 4
            self.values[8, 4] = 1
            self.values[8, 5] = 8
            self.values[8, 6] = 4

    def print_values(self):
        print("Deepness :", self.deepness, "Variation:", self.variation)
        for i in range(9):
            if i % 3 == 0:
                print("")

            row = ""
            for j in range(9):
                if j % 3 == 0:
                    row += "|"

                if self.values[i, j] in NUMBERS:
                    row += str(self.values[i, j]) + " "
                else:
                    row += "- "

            print(row)


if __name__ == "__main__":
    start = time.time()
    sudoku_to_solve = Sudoku()
    sudoku_to_solve.assign_example(4)
    print("Let's solve the Sudoku:")
    sudoku_to_solve.print_values()
    sudoku_to_solve.solve()
    end = time.time()
    time_elapsed = end - start
    print("\nTime to do it :", time_elapsed, "seconds")
