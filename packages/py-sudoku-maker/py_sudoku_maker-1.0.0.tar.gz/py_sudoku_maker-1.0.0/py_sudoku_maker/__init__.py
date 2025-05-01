import random

def generate_sudoku() -> list[list[int]]:
    sudoku = [[],[],[],[],[],[],[],[],[]]
    sudoku = fill_line(sudoku)
    sudoku = fill_rest_row(sudoku)
    sudoku = shuffle_sudoku(sudoku)
    return sudoku

def fill_line(sudoku: list[list[int]]) -> list[list[int]]:
    nums = [1,2,3,4,5,6,7,8,9]
    for i in range (0, 9):
        if len(nums) > 1:
            temp = nums[random.randint(1, len(nums) - 1)]
            sudoku[0].append(temp)
            nums.remove(temp)
        else:
            temp = nums[0]
            sudoku[0].append(temp)
    
    return sudoku

def fill_rest_row(sudoku: list[list[int]]) -> list[list[int]]:
    for i in range (1, 9):
        if i%3 == 0:
            for j in range(0, 9):
                if j+1 == 9:
                    sudoku[i].append(sudoku[i-1][0])
                else:
                    sudoku[i].append(sudoku[i-1][j+1])
        else:
            for j in range(0, 9):
                if j+3 >= 9:
                    sudoku[i].append(sudoku[i-1][j-6])
                else:
                    sudoku[i].append(sudoku[i-1][j+3])
    
    return sudoku

def shuffle_sudoku(sudoku: list[list[int]]) -> list[list[int]]:
    swap1 = [1,2,3,4,5,6,7,8,9]
    swap2 = [1,2,3,4,5,6,7,8,9]

    while len(swap1) != 0 and len(swap2) != 0:
        if len(swap1) > 1:
            num1 = swap1[random.randint(1, len(swap1) - 1)]
            swap1.remove(num1)
            num2 = swap2[random.randint(1, len(swap2) - 1)]
            swap2.remove(num2)
        else:
            num1 = swap1[0]
            num2 = swap2[0]
            swap1.remove(num1)
            swap2.remove(num2)
        for i in range(0,9):
            temp1 = sudoku[i].index(num1)
            temp2 = sudoku[i].index(num2)
            sudoku[i][temp1] = num2
            sudoku[i][temp2] = num1
    
    return sudoku

def print_sudoku():
    sudoku = generate_sudoku()
    out = ["","","","","","","","",""]
    for i in range(0, len(sudoku)):
        for j in range (0, len(sudoku[i])):
            out[i] += str(sudoku[i][j])
            if (j + 1) % 3 == 0:
                out[i] += "  "
            else:
                out[i] += " "

    for line in range(0, len(out)):
        print(out[line])
        if (line + 1) % 3 == 0:
            print("")
