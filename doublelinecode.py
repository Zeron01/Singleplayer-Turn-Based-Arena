import time
import sys
import os
def alphalinewriter(words,delay = 0.004):
    amountofwords = len(words)
    word1 = ''
    word2 = ''
    word3 = ''
    word4 = ''
    word5 = ''
    word6 = ''
    word7 = ''
    word8 = ''
    x=0
    os.system('cls')
    longestword = max(words,key=len)
    longestword = len(longestword)

    for num in range(0,longestword):
        if (word1 == words[0]) and (word2 == words[1]) and (word3==words[2]) and (word4 == words[3]) and (word5 == words[4])and (word6 == words[5]) and (word7==words[6]) and (word8 == words[7]):
            break
        if num >= len(words[0]):
            word1+=""
        else:
            word1+=words[0][num]
        try:
            if num >= len(words[1]):
                word2+=""
            else:
                word2+=words[1][num]
            try:

                if num >= len(words[2]):
                    word3+=""
                else:
                    word3+=words[2][num]
                try:
                    if num >= len(words[3]):
                        word4+=""
                    else:
                        word4+=words[3][num]
                    try:
                        if num>= len(words[4]):
                            word5+=""
                        else:
                            word5+=words[4][num]
                        try:
                            if num>= len(words[5]):
                                word6+=''
                            else:
                                word6+=words[5][num]
                            try:
                                if num>= len(words[6]):
                                    word7+=''
                                else:
                                    word7+=words[6][num]
                                try:
                                    if num >= len(words[7]):
                                        word8+=''
                                    else:
                                        word8+=words[7][num]
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass

            except:
                pass
        except:
            pass
        print(f'{word1}\n{word2}\n{word3}\n{word4}\n{word5}\n{word6}\n{word7}\n{word8}')
        time.sleep(delay)
        os.system('cls')
    print(f'{word1}\n{word2}\n{word3}\n{word4}\n{word5}\n{word6}\n{word7}\n{word8}')
