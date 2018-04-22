def read_in_files(path):
    file = open(path)
    str = file.read()
    returned = str.split(",")
    print(returned)
    return returned



class Process:
    list = []
    time_read_in = None
    max_length = 3
    def fifo_repalcement(self, number):
        if len(list) == self.max_length:
            if number not in self.list:
                list.pop(0)
                list.append(number)
        else:
            list.append(number)

    def lru_replacement(self, number):
        new_list = list.sort(lambda x: x.time)

if __name__ == "__main__":
    files_to_read = ["C:\\Users\\Owner\\Google Drive\\CSCI 474\\Assignment 3\\p0PageRequest.txt",
    "C:\\Users\\Owner\\Google Drive\\CSCI 474\\Assignment 3\\p1PageRequest.txt",
    "C:\\Users\\Owner\\Google Drive\\CSCI 474\\Assignment 3\\p2PageRequest.txt",
    "C:\\Users\\Owner\\Google Drive\\CSCI 474\\Assignment 3\\p8PageRequest.txt",
    "C:\\Users\\Owner\\Google Drive\\CSCI 474\\Assignment 3\\p9PageRequest.txt"]

    process1 = read_in_files(files_to_read[0])
    process2 = read_in_files(files_to_read[1])
    process3 = read_in_files(files_to_read[2])
    process4 = read_in_files(files_to_read[3])
    process5 = read_in_files(files_to_read[4])
