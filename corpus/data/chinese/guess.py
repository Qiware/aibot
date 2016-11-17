# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":
    f = open("guess.txt", "r")
    lines = f.readlines()
    f.close()

    print("{")
    print("\t\"guess\": [")

    is_first_conversion = True
    for line in lines:
        line=line.strip('\n')
        conversation = line.split('谜底:');
        history = []
        flag = False
        for text in conversation:
            if history:
                if False == flag:
                    if is_first_conversion:
                        print("\t\t[")
                        is_first_conversion = False
                    else:
                        print(",")
                        print("\t\t[")
                    print("\t\t\t\"%s\"," % history[-1].strip('\n').strip('\r')),
                    print("\t\t\t\"%s\"" % text.strip('\n').strip('\r')),
                    flag = True
                    continue
                print(","),
                print("\t\t\t\"%s\"" % text.strip('\n').strip('\r')),
            history.append(text) # 当前语句加入历史列表
        if True == flag:
            print("\t\t]"),
    print("\t]")
print("}")

