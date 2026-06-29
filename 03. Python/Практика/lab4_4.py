def dissipateArray(input_data):
    """
    >>> dissipateArray("0 0 1 0")
    YES
    1
    1 4
    >>> dissipateArray("0 0 -4 0 0")
    YES
    1
    1 5
    >>> dissipateArray("0 0 0 3")
    YES
    1
    1 5
    >>> dissipateArray("0 0 -4 0 0")
    YES
    1
    1 5
    >>> dissipateArray("5 0 0")
    YES
    1
    1 3
    >>> dissipateArray("1 2 3 -5")
    YES
    4
    1 1
    2 2
    3 3
    4 4

    >>> dissipateArray("0 0 5 -5")
    YES
    2
    1 3
    4 4
    >>> dissipateArray("9 -12 3 4 -4 -10 7 3")
    YES
    2
    1 1
    2 8
    >>> dissipateArray("1 2 -3") 
    YES
    2
    1 1
    2 3
    >>> dissipateArray("0")
    NO
    >>> dissipateArray("0 5 -5")
    YES
    2
    1 2
    3 3
    >>> dissipateArray("0 0 0")
    NO
    """
    #n = int(input())
    orig = [int(item) for item in input_data.split()]
    first_non_zero_index = None
    answers = []
    for index, item in enumerate(orig):
        if item != 0:
            first_non_zero_index = index + 1
            break
    if first_non_zero_index == None:
        answers.append("NO")
    if sum(orig[0:first_non_zero_index]) != 0 and sum(orig[first_non_zero_index:len(orig)]) != 0:
        answers.append("1 " + str(first_non_zero_index))
        answers.append(str(first_non_zero_index+1) +" "+ str(len(orig)))
    if("NO" not in answers and len(answers) == 0):
        acc_sum = 0
        first_index = 0
        for i in range(1,len(orig)+1):
            acc_sum += orig[i-1]
            if acc_sum != 0:
                answers.append(str(first_index+1) + ' ' + str(i))
                first_index = i
                acc_sum = 0
            elif i == len(orig) and acc_sum==0 and  len(answers)>0:
                x = answers.pop()
                answers.append(x.split()[0] + " " + str(i))
            if i == len(orig) and acc_sum==0 and len(answers)==0:
                answers.append("1" + ' ' + str(len(orig)))
            
    if "NO" not in answers:
        print("YES")
        print(str(len(answers)))
        for item in answers:
            print(item)
    else:
        print("NO")

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    
    
