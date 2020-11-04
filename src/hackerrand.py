import math
import sys

def kangaroo(x1, v1, x2, v2):
    should_continue = True

    while should_continue:
        if x1==x2:
            return "YES"
        x1+=v1
        x2+=v2
        if x1>x2:
            should_continue = False
        elif (x2 >= x1) & (v2 >= v1):
            should_continue = False
    return "NO"

def getTotalX(n, m, arr, brr):
    # Write your code here
    begin = max(arr)
    end = max(brr)+1
    count = 0
    for i in range(begin, end):
        multiple_of_arr = True
        divider_of_brr = True

        for a in arr:
            if (i % a != 0):
                multiple_of_arr = False
                break
        if(multiple_of_arr):
            for b in brr:
                if (b % i != 0):
                    divider_of_brr = False
                    break

        if (multiple_of_arr) & (divider_of_brr):
            count += 1

    return count


if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    #first_multiple_input = input().rstrip().split()

    n = 1

    m = 1

    arr = [1]

    brr = [100]

    total = getTotalX(n, m, arr, brr)

    print(str(total))

    #fptr.close()
