



res_list = []
card = {'key':'val'}

def start():
    for val in range(10):
        card = {'key_'+str(val):{'name':val}}
        res_list.append(card)
    print('res_list:',res_list)
    for rval in res_list:
        for key in rval.keys():
            print('val:',key, rval.get(key))

    dict_val = {'ccc':'nnn','ccc1':'nnn1'}
    print('>>',dict_val.keys(),dict_val.get())


if __name__ == '__main__':
    start()
