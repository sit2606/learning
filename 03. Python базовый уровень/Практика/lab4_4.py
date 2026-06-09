def dissipateArray(input_data):
    """
    >>> dissipateArray("1 2 -3") 
    YES
    2
    1 2
    3 3
    >>> dissipateArray("0 0 5 -5")
    YES
    2
    1 3
    4 4
    >>> dissipateArray("9 -12 3 4 -4 -10 7 3")
    YES
    2
    1 2
    3 8
    >>> dissipateArray("0")
    NO
    >>> dissipateArray("1 2 3 -5")
    YES
    4
    1 1
    2 2
    3 3
    4 4
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
    n = len(orig)
    # 1. Проверяем самый частый и простой случай
    if sum(orig) != 0:
        print("YES")
        print(1)
        print(f"1 {n}")
    else:
        # 2. Если сумма 0, ищем первый ненулевой элемент
        split_idx = -1
        for i in range(n):
            if orig[i] != 0:
                split_idx = i
                break
                
        # 3. Если не нашли ни одного ненулевого элемента, значит, там одни нули
        if split_idx == -1:
            print("NO")
        else:
            # 4. Режем ровно один раз после первого ненулевого элемента
            print("YES")
            print(2)
            print(f"1 {split_idx + 1}")
            print(f"{split_idx + 2} {n}")

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    
    
