
if __name__ == "__main__":
    '''string = "Python is interesting."
    byteArray = bytearray(string, 'utf-8')
    print("Value of byteArray = ", byteArray)
    print("Type of byteArray = ", type(byteArray))

    stringCreated = byteArray.decode()
    print("Value of stringCreated = ", stringCreated)
    print("Type of stringCreated = ", type(stringCreated))'''


    str = "file:/home/kautuk/Desktop/Reasoning-work/streaming_reasoning/datafiles/test2.txt"
    index = str.rindex('/')
    print(str[index + 1 : ])
