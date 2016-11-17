# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":
    f = open("poetry.txt", "r")
    lines = f.readlines()
    f.close()

    print("{")
    print("\t\"poetry\": [")

    is_first_conversion = True
    for line in lines:
        line=line.strip('\n')
        conversation = line.split(' ');
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
                    print("\t\t\t\"%s\"," % history[-1]),
                    print("\n\t\t\t\"%s\"" % text),
                    flag = True
                    continue
                print(","),
                print("\n\t\t\t\"%s\"" % text)
            history.append(text) # 当前语句加入历史列表
        if True == flag:
            print("\n\t\t]"),
    print("\n\t]")
print("}")

