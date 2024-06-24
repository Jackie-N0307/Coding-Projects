import os
from random import randrange

# just giving possible options 
print('Hello Jackie, what would you like to do today?')
print('1. View the "to do" list')
print('2. Add something to the list?')
print('3. Check off something done')
print('4. Feel inspired to do something')

user_choice = int(input("So what is your choice?:"))
print("---------------------------")


#opening the file to read it
def read_list():
    file_path = r"To Do List Project\to.do.list.txt"

    with open(file_path,'r') as file_r:
        count = 1
        print("** Jackie's To Do List**")

        for line in file_r:
            print(f"{count}. {line}",end = '')
            count += 1
    print("---------------------------")
# function for adding something to the list
def add_list(rank, activity):
    current_line = 1
    rank = int(rank)
    activity = str(activity)
    file_path = r"To Do List Project\to.do.list.txt"

    with open(file_path,'r') as file_r:
        with open(r"To Do List Project\to.do.list.new.txt",'w') as file_w:

            #rewrites the to do list until it reaches line of desired new string
            for line in file_r:
                
                if current_line == rank:
                    file_w.write(f"{activity}\n")

                file_w.write(line)
                current_line += 1

            if rank >= len(file_r.readlines()):
                file_w.write(f"{activity}\n")

    #getting rid of the old list and updating it 
    os.remove(r"To Do List Project\to.do.list.txt")
    old_name = r"To Do List Project\to.do.list.new.txt"
    new_name = r"To Do List Project\to.do.list.txt"

    os.rename(old_name,new_name)
    read_list()                    



def delete(rank):
    current_line = 1
    rank = int(rank)

    #opening the files
    with open(r"To Do List Project\to.do.list.txt",'r') as file_r:
        with open(r"To Do List Project\to.do.list.new.txt",'w') as file_w:

            #rewrites the to do list until it reaches line of desired new string
            for line in file_r:
                
                if current_line == rank:
                    #wont do anything if correct number 
                    current_line += 1
                    pass
                
                else:
                    #rewriting 
                    file_w.write(line)
                    current_line += 1

    # since a new one is made the old must be deleted
    os.remove(r"To Do List Project\to.do.list.txt")
    old_name = r"To Do List Project\to.do.list.new.txt"
    new_name = r"To Do List Project\to.do.list.txt"
    os.rename(old_name,new_name)
    read_list()

def motivation():
    random_line = randrange(1,100)
    count = 1

    #keeps reading through each line until it reaches desired random number
    with open(r'To Do List Project\motivational.txt','r') as file_r:
        for line in file_r:
            if count == random_line:
                print(line,end = '')
                break
            else:
                count +=1 
    print("---------------------------")





def question():
    global user_choice
    if user_choice == 1:
        read_list()

    if user_choice == 2:
        new_item = str(input("What would you like to add to your to do list?:"))
        ranking = int(input("And what rank should I place it at?:"))
        add_list(ranking,new_item)

    if user_choice == 3:
        removed_item = int(input("What item would you like to remove?:"))
        delete(removed_item)

    if user_choice == 4:
        motivation()

        
    new_decision = str(input("Are you satisfied?:"))

    if new_decision == "No" or new_decision == "no":
        user_choice = int(input("What would you like to do now?:"))
        question()

    else:
        print("Have a great day :DDD ")
        

question()


        
