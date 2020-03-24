#!/usr/bin/env python3

# *** Use this for auto-contained examples ***
from OpenIDClient import OpenIDClient
def main():
    
    a = OpenIDClient(None,'openid%20profile%20email',None,None,'kbyuFDidLLm280LIwVFiazOqjO3ty8KH')
    a.testLib()
    a.requestCodeAuth('https://google.com','GET')
    print('stoppp')
    

if __name__ == "__main__":
    main()
