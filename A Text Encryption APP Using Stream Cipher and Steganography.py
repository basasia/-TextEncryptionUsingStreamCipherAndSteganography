"""
file: Text Encryption
Description: functions for text encryption
Created: 27/12/2020.
Updated: 20/1/2021.
Authors: Asia Benyadilok
"""
import random
import sympy as prime


#method: genComDiv
#parameters: int x and y
#Description: called when need to gcd between two numbers
def genComDiv(x,y):

    # euclidean algorithm
    while y > 0:

        temp = x
        x = y
        y = temp % y

    return x

#method: genPrime
#parameters: int p
#Description: called when need to generate prime number
def genPrime(p):
    found = False

    #find next prime number from input
    while found == False:
        p = prime.nextprime(p)

        #check condition
        if p % 4 == 3:
            found = True

    return p

#method: bbShub
#parameters: int bitLen
#Description: called when need to generate a random binary sequence
def bbShub(bitLen):

    #initailize variables
    p = 0
    q = 0
    outputKey = ""

    #seed
    xi = random.randint(1, 1e10)

    #find two big prime numbers that gcd between them is 1
    while (genComDiv(p,q) != 1):

        #generate big random prime numbers
        p = genPrime(random.randint(3e10,5e10))
        q = genPrime(random.randint(7e10,9e10))

    m = p*q

    #make sure that the seed is co-prime of m
    while (genComDiv(xi,m) != 1):
        xi = random.randint(1, 1e10)

    #generate key steam
    for i in range(bitLen):

        #blum blum shub equations
        xi = (xi**2) % m

        #parity bit output
        bit = (xi % 2)

        #save each bit to output
        outputKey += str(bit)

    return outputKey

#method: streamCipher
#parameters: String text, String key
#Description: called when need to encrypt text
def streamCipher(text,key):

    #initialize output
    binText = ""

    #convert text to binary (full bytes)
    for i in text:
        binText += ('{0:08b}'.format(ord(i),'b'))

    #encrypt text XOR with key
    encryptText = XOR(binText,key)

    return encryptText

#method: hideMessage
#parameters: String oMes, String sMes
#Description: called when need to hide a secret message in a original message
def hideMessage(oMes,sMes):

    #add fullstop at the end of original message
    oMes += "."

    # convert secret message to form of "." + white space
    for i in range(len(sMes)):

        # white space indicate "0"
        if sMes[i] == "0":
            oMes += " "

        #tab space indicate "1"
        else:
            oMes += "\t"

    return oMes

#method: extractHiddenMessage
#parameters: String mes
#Description: called when need to extract a hidden message from a original message
def extractHiddenMessage(mes):

    #initialize variables
    secretMes = ""

    #scan for the last dot that appear in the message
    for i in range(len(mes)):
        if (mes[i] == "."):
            startIndex = i

    #convert hidden message from white space back to binary
    for i in range(startIndex+1,len(mes)):

        # white space indicate "0"
        if mes[i] == " ":
            secretMes += "0"

        # tab space indicate "1"
        else:
            secretMes += "1"

    return secretMes

#method: binToInt
#parameters: int bin
#Description: called when need to convert binary to integer
def binToInt(bin):

    #initialize variables
    result = 0

    #convert binary to decimal
    for i in range(8):
        decimal = bin % 10
        result = result + (decimal*(2**i))
        bin = bin//10

    return result

#method: decryptMessage
#parameters: String secretMes, String key
#Description: called when need to decrypt a secret message with a key
def decryptMessage(secretMes,key):

    #initialize variables
    originMes = ""

    # XOR secret message with key
    originBin = XOR(secretMes,key)

    #convert binary back to string
    for i in range(0,len(originBin),8):
        integer = binToInt(int(originBin[i:i+8]))
        originMes +=  chr(integer)

    return originMes

#method: XOR
#parameters: String bin1, String bin2
#Description: called when need to decrypt a secret message with a key
def XOR(bin1,bin2):

    #initialize variable
    result =""

    #XOR process
    for i in range(len(bin1)):
        if bin1[i] == bin2[i]:
            result += "0"
        else:
            result += "1"

    return result

#method: main
#parameters: none
#Description: called when need to run a text encryption program
def main():
    #take input from user
    oMes = input("Enter original message: ")
    sMes = input("Enter secret message: ")

    #check if the input is empty or not
    if (len(oMes) != 0 and len(sMes) != 0):

        #generate key for encryption with the same length of bit as secret message
        key = bbShub(len(sMes)*8)

        #encryptText with key
        encryptText = streamCipher(sMes, key)

        #hide encrypted secret message in the original text
        hideMes = hideMessage(oMes, encryptText)

        #print output
        print("\nKey : ",key)
        print("Message with hidden message : "+hideMes)

        cipText = input("\nEnter cipher text: ")
        key = input("Enter key: ")

        #extract hidden message from meassage
        secretText = extractHiddenMessage(cipText)

        #decrypt scret message
        secretText = decryptMessage(secretText,key)

        print("Scret message is : ",secretText)

    else:
        print("Invalid input")


#run main method
main()


