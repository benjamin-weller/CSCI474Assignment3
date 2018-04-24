import datetime


def read_in_files(path):
    file = open(path)
    str = file.read()
    returned = str.split(",")
    print(returned)
    return returned


def round_robin(list_of_processes):
    pass



































































class ClockItem():
    number = None
    just_used = False
    def __init__(self, number):
        self.number = number


    # def flip(self):
    #     if self.justUsed:
    #         self.justUsed = False
    #     else:
    #         self.justUsed = True














class LRUItem():
    number = None
    last_update = None

    def __init__(self, number):
        self.number = number
        self.last_update = datetime.now()

    def update(self):
        self.last_update = datetime.now()





def check_for_LRU_item(list, number):
    for index, x in enumerate(list):
        if x.number == number:
            return index
    return -1

def first_to_back(list):
    list.append(list.pop())

class Process:
    in_memory_list = []
    max_length = 3
    number_of_faults = 0
    full_list = []

    def fifo_repalcement(self, number):
        if len(list) == self.max_length:
            if number not in self.list:
                list.pop(0)
                list.append(number)
        else:
            list.append(number)


    def lru_replacement(self, number):
        if len(list) == self.max_length: #If the buffer is maxed out
            index = check_for_LRU_item(self.in_memory_list, number)
            if index == -1:
                #Do LRU replacement
                self.in_memory_list.sort(key=lambda x: x.last_update)
                #Grab the last element, toss it
                self.in_memory_list.pop()
                #Add our new element to the list
                self.in_memory_list.append(LRUItem(number))
        else: #If there's space in the buffer
            #Create a new LRU item, and add it to the list
            self.in_memory_list.append(LRUItem(number))

    def clock_replacement(self, number):
        """. When a page is replaced, the pointer is set to indicate the next frame in the buffer after the one just updated."""
        if len(list) == self.max_length:  # If the buffer is maxed out

            # Check to see if the number is in there already????
            # If it is end the method
            for x in self.in_memory_list:
                if x.number == number:
                    x.just_used = True;
                    return

            """If we find any pages that have a 0s we should replace then. If we have all 1s you should flip them as you find them, and if you loop all the way, then just replace the one you started at."""
            dirty_list = self.in_memory_list #Hack way to get around modifying while itereating
            for x in dirty_list:
                if x.number == number: #Get our number, and indicate the element was just used, send it to the back.
                    x.just_used = True
                    first_to_back(self.in_memory_list)
                    return
                elif not x.just_used:
                    #Replace the page and reuturn

                else:
                    x.just_used = False
                    first_to_back(self.in_memory_list)

            # If we iterate through the entire list, and somehow can't manage to find the number,
            # then remove the first one and add our new number to the last slot.
            self.in_memory_list.pop(0)
            addMe = ClockItem(number)
            addMe.just_used = True
            self.in_memory_list.append(addMe)
            self.number_of_faults += 1
        else: #If there's space in the buffer
            addMe = ClockItem(number)
            addMe.just_used = True
            self.in_memory_list.append(addMe)

    def optimal_replacement(self, number):
        pass






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


