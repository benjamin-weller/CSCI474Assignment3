import sys
from frameClasses import *
import copy

def read_in_files(path):
    file = open(path)
    str = file.read()
    return list(map(int, str.split(",")))

def first_to_back(list):
    list.append(list.pop())

def check_in_list(list, name, number):
    # Checks to see if a specific frame is in memory if it is, it returns true and the index
    for index, x in enumerate(list):
        if x.name == name and x.number == number:
            return True, index
    return False, 0


def optimal_replacement(remainder_of_frames, in_memory_list, name, number, max_length):
    is_in_list, index = check_in_list(in_memory_list, name, number)
    if is_in_list:
        return 0

    if len(in_memory_list) == max_length:
        #The number for this specific process isn't in the buffer
        #Thus loop through all frames in the buffer and check to see when they are next used in the stream
        next_use_list = []
        for x in in_memory_list:
            # If it exists, then append it's location, else just append a really large number.
            try:
                distance_to_next_access = remainder_of_frames.index(x.number)
                next_use_list.append(distance_to_next_access)
            except ValueError as ve:
                next_use_list.append(float("inf"))
            #Get the max value of the list, and then grab that index from the next use list
        max_value = max(next_use_list)
        index = next_use_list.index(max_value)
        #Using index now replace the value there
        in_memory_list[index] = BaseFrame(number, name)
    else:
        in_memory_list.append(BaseFrame(number, name))
    return 1


def optimal_replacement_rr(list_of_lists, in_memory_list, name, number, max_length):
    #I'm going to have to do things a bit differently here.
    #I'm going to name my frames the number of the list they correspond to.
    is_in_list, index = check_in_list(in_memory_list, name, number)
    if is_in_list:
        return 0

    if len(in_memory_list) == max_length:
        #Check optimality
        next_use_list = []
        for index, x in enumerate(in_memory_list):
            try:
                if list_of_lists[x.name]:
                    list_to_search = list_of_lists[x.name]
                    distance_to_next_access = list_to_search.index(x.number)
                    next_use_list.append(OptimalReplacementRR(index, distance_to_next_access))
            except ValueError as ve:
                # next_use_list.append(float("inf"))
                next_use_list.append(OptimalReplacementRR(index, float("inf")))

        replace_me_object = max(next_use_list, key=lambda x: x.distance_to_next_access)
        # Using index now replace the value there
        in_memory_list[replace_me_object.frame_index_in_memory] = BaseFrame(number, name)

    else:
        in_memory_list.append(BaseFrame(number, name))
    return 1



def fifo_repalcement(list, name, number, max_length):
    is_in_list, index = check_in_list(list, name, number)
    if is_in_list:
        return 0

    if len(list) == max_length:
        list.pop(0)
        list.append(BaseFrame(number, name))
    else:
        list.append(BaseFrame(number, name))
    return 1

def lru_replacement(list, name, number, max_length):
    is_in_list, index = check_in_list(list, name, number)
    if is_in_list:
        # Update the entry by putting it at the back of the queue.
        list.append(list.pop(index))
        return 0

    if len(list) == max_length: #If the buffer is maxed out
        #Do LRU replacement
        # in_memory_list.sort(key=lambda x: x.last_update)
        #Grab the first element, toss it
        list.pop(0)
        #Add our new element to the list
        list.append(BaseFrame(number, name))
    else: #If there's space in the buffer
        #Create a new Frame item, and add it to the list
        list.append(BaseFrame(number, name))
    return 1

def clock_replacement(list, name, number, max_length):
    is_in_list, index = check_in_list(list, name, number)
    if is_in_list:
        # Update the entry at the index
        list[index].just_used = True
        return 0

    """. When a page is replaced, the pointer is set to indicate the next frame in the buffer after the one just updated."""
    if len(list) == max_length:  # If the buffer is maxed out
        """If we find any pages that have a 0s we should replace then. If we have all 1s you should flip them as you find them, and if you loop all the way, then just replace the one you started at."""
        for x in list:
            if not x.just_used: #If the page hasn't been used since the last fault, then replace it.
                #Replace the page and reuturn
                list.pop(0)
                addMe = ClockItem(number, name)
                list.append(addMe)
                return 1
            else:
                x.just_used = False
                first_to_back(list)

        # If we iterate through the entire list, and somehow can't manage to find one that's unused,
        # then remove the first one and add our new number to the last slot.
        list.pop(0)
        addMe = ClockItem(number, name)
        list.append(addMe)
    else: #If there's space in the buffer
        addMe = ClockItem(number, name)
        addMe.just_used = True
        list.append(addMe)
    return 1

def consecutive_fifo(list_of_lists, max_length):
    #Going to get a list that contains lists
    faults = 0
    runs = 0
    for index, list in enumerate(list_of_lists):
        in_memory_list = []
        for x in list:
            faults += fifo_repalcement(in_memory_list, f"P{index}", x, max_length)
            runs += 1
    print(f"Our FIFO consecutive memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate.")

def consecutive_lru(list_of_lists, max_length):
    #Going to get a list that contains lists
    faults = 0
    runs = 0
    for index, list in enumerate(list_of_lists):
        in_memory_list = []
        for x in list:
            faults += lru_replacement(in_memory_list, f"P{index}", x, max_length)
            runs += 1
    print(f"Our LRU consecutive memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate.")

def consecutive_clock(list_of_lists, max_length):
    #Going to get a list that contains lists
    faults = 0
    runs = 0
    for index, list in enumerate(list_of_lists):
        in_memory_list = []
        for x in list:
            faults += clock_replacement(in_memory_list, f"P{index}", x, max_length)
            runs += 1
    print(f"Our Clock consecutive memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate.")

def consecutive_optimal(list_of_lists, max_length):
    #Going to get a list that contains lists
    faults = 0
    runs = 0
    for index, remainder_of_stream in enumerate(list_of_lists):
        in_memory_list = []
        for index_in_stream, x in enumerate(remainder_of_stream):
            stream_list = remainder_of_stream[index_in_stream:]
            faults += optimal_replacement(stream_list, in_memory_list, f"P{index}", x, max_length)
            runs += 1
    print(f"Our Optimal replacement consecutive memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate.")

def are_lists_unempty(list_of_lists):
    for list in list_of_lists:
        if list:
            return True #They do contain some values
    return False #They all are empty

def round_robin_fifo(list_of_lists, max_length):
    faults = 0
    runs = 0
    in_memory_list = []
    copy_of_lists = copy.deepcopy(list_of_lists)
    while(are_lists_unempty(copy_of_lists)):
        for index, list in enumerate(copy_of_lists):
            if list:
                faults += fifo_repalcement(in_memory_list, f"P{index}", list.pop(0), max_length)
                runs += 1
    print(f"Our FIFO round robin memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate")

def round_robin_lru(list_of_lists, max_length):
    faults = 0
    runs = 0
    in_memory_list = []
    copy_of_lists = copy.deepcopy(list_of_lists)
    while(are_lists_unempty(copy_of_lists)):
        for index, list in enumerate(copy_of_lists):
            if list:
                faults += lru_replacement(in_memory_list, f"P{index}", list.pop(0), max_length)
                runs += 1
    print(f"Our LRU round robin memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate")

def round_robin_clock(list_of_lists, max_length):
    faults = 0
    runs = 0
    in_memory_list = []
    copy_of_lists = copy.deepcopy(list_of_lists)
    while(are_lists_unempty(copy_of_lists)):
        for index, list in enumerate(copy_of_lists):
            if list:
                faults += clock_replacement(in_memory_list, f"P{index}", list.pop(0), max_length)
                runs += 1
    print(f"Our Clock round robin memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate")

def round_robin_optimal(list_of_lists, max_length):
    faults = 0
    runs = 0
    in_memory_list = []
    copy_of_lists = copy.deepcopy(list_of_lists)
    while(are_lists_unempty(copy_of_lists)):
        for index, list in enumerate(copy_of_lists):
            if list:
                faults += optimal_replacement_rr(list_of_lists, in_memory_list, index, list.pop(0), max_length)
                runs += 1
    print(f"Our Optimal round robin memory strategy with a buffer of size {max_length} ran with {(faults/runs)*100}% page fault rate")

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

    list_of_lists = [process1, process2, process3, process4, process5]
    consecutive_fifo(list_of_lists, 5)
    consecutive_lru(list_of_lists, 5)
    consecutive_clock(list_of_lists, 5)  # Apparently clock is off???
    consecutive_optimal(list_of_lists, 5)

    print("\n")
    consecutive_fifo(list_of_lists, 10)
    consecutive_lru(list_of_lists, 10)
    consecutive_clock(list_of_lists, 10)  # Apparently clock is off???
    consecutive_optimal(list_of_lists, 10)

    # Do round robin here
    print("\n")
    round_robin_fifo(list_of_lists, 5)  # Apparently doesn't work????
    round_robin_lru(list_of_lists, 5)  # Apparently doesn't work????
    round_robin_clock(list_of_lists, 5)  # Again doesn't work.....
    round_robin_optimal(list_of_lists, 5)  # Again doesn't work.....

    print("\n")
    round_robin_fifo(list_of_lists, 10)  # Apparently doesn't work????
    round_robin_lru(list_of_lists, 10)  # Apparently doesn't work????
    round_robin_clock(list_of_lists, 10)  # Again doesn't work.....
    round_robin_optimal(list_of_lists, 10)  # Again doesn't work.....

