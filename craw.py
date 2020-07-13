import malshare
#import malwares
import maldomain

from enum import Enum
import json
import os

class craw_menu(Enum):
    malwares = '0'
    mal_domain = '1'
    malshare = '2'
    contagio = '3'
    contagio_mobile = '4'
    thezoo = '5'
    packet_ = '6'

if __name__ =='__main__':
    try:
        if not os.path.exists('/home/jbs/mal'):
            os.makedirs('/home/jbs/mal')
    except OSError:
        print('Error: Creating directory. '+'/home/jbs/mal')
    #mal_share = malshare()
    #mal_domain = maldomain()
    #mal_wares = malwares()
    print('-'*60 +'\n0.malwares\n1.mal_domain\n2.malshare\n3.contagio\n4.contagio_mobile\n5.thezoo\n6.\n( -1 : 종료)\n'+'-'*60)
    print('입력 :',end =' ')
    value = input()
    if value >= '0' and value <= '6':
        select = craw_menu(value).name

    if select == 'malwares':
        os.system('python3 malwares.py')
    elif select == 'mal_domain':
        #result = mal_domain.domain_run()
        #print(result)
        os.system('python3 maldomain.py')    
    elif select == 'malshare':
        os.system('python3 malshare.py')
    elif select == 'contagio':
        os.system('python3 contagio.py')
    #elif select == 'contagio_mobile':
        #os.system('python3 contagio_mobile.py')
    elif select == 'thezoo':
        os.system('python3 thezoogit.py')
    elif select == 'packet':
        os.system('python3 .py')