s = input()
orig = input().split()
orig = [int(item) for item in orig]
answer_list = list()
first_index=0
a = 0
all_zero = False
for i in orig:
    if i == 0:
        a += 1
    else:
        continue
if a == len(orig):
    all_zero = True
for index, item in enumerate(orig):
    if sum(orig[first_index:index+1]) != 0:
       continue
    else:
        if index == 0 and sum(orig[first_index:index]) != 0:
            answer_list.append(str(first_index+1) + ' ' + str (index+1))
            continue
        #answer_list.append(str(first_index+1) + ' ' + str (index))
        if sum(orig[slice(index,len(orig))]) != 0:
            answer_list.append(str(index+1) + ' ' + str(len(orig)))
            break
        else:
            first_index = index
        print('s') 
if len(answer_list)>0 and not all_zero:
    print("YES")
    for item in answer_list:
        print(item)    
elif len(answer_list)==0 and not all_zero:
    print("YES")
    for index, item in enumerate(orig):
        print(str(index+1) + ' '+ str(index+1))
else:
    print("NO")