import os
from tkinter import *
from termcolor import colored
from pyfiglet import figlet_format
import shutil
import maskpass
import time

columns = shutil.get_terminal_size().columns

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_curr_medicines(name):
    try:
        with open(f'users/{name}/medicines.txt') as f_in:
            medicines = f_in.readlines()
    except FileNotFoundError:
        medicines = []
        pass
    return medicines

def update_sched(name, fullsched):
    for i in range(len(fullsched)):
        with open(f'users/{name}/schedules/schedule{i}.txt', 'w') as f_out:
            for j in range(len(fullsched[i])):
                f_out.write(f'{fullsched[i][j]}')

def get_current_sched(name):

    full_sched = []
    for i in range(4):
        with open(f'users/{name}/schedules/schedule{i}.txt') as f_in:
            temp_sched = f_in.readlines()
        
        full_sched.append(temp_sched)
    return full_sched

def medicine_view(name, medicines):
    print(colored('These are all your current Medicines', 'red').center(columns))
    print(colored('Enter R to return to previous tab', 'blue').center(columns))
    print(colored('Enter Q to quit the program', 'blue').center(columns))
    for i in range(len(medicines)):
        print(f'{i + 1} - {medicines[i]}')
    print('\n')
    enter_in = input()
    while enter_in != 'R' and enter_in != 'Q':
        enter_in = input()
    clear()
    if enter_in == 'R':
        medicinesf(name)
    else:
        return

def medicine_edit(name, medicines):
    medicines = get_curr_medicines(name)
    print(colored('Enter A to Add a Medicine | Enter D to Remove a Medicine', 'red').center(columns))
    print(colored('Enter R to return to previous tab', 'blue').center(columns))
    print(colored('Enter Q to quit the program', 'blue').center(columns))
    enter_in = input()
    while enter_in != 'A' and enter_in != 'D' and enter_in != 'R' and enter_in != 'Q':
        enter_in = input()
    clear()
    if enter_in == 'A':
        clear()
        med_name = input('Enter Medicine Name : ')
        with open(f'users/{name}/medicines.txt', 'a') as f_out:
            f_out.write(f'{med_name}\n')
        print(colored('Medicine Successfully Added', 'red').center(columns))
        time.sleep(3)
        clear()
        medicine_edit(name, medicines)
    elif enter_in == 'D':

        print(colored('Select the Medicine by number, which you want to remove', 'red').center(columns))
        for i in range(len(medicines)):
            print(f'{i + 1} - {medicines[i]}')
        print('\n')

        chosen_med = int(input())
        print(colored('Medicine Successfully Removed', 'red').center(columns))
        medicines.pop(chosen_med - 1)
        with open(f'users/{name}/medicines.txt', 'w') as f_out:
            for med in medicines:
                f_out.write(med)
        time.sleep(3)
        clear()
        medicine_edit(name, medicines)

    elif enter_in == 'R':
        medicinesf(name)
    else:
        return

def schedule_view(name, medicines):
    clear()
    full_sched = get_current_sched(name)

    window = Tk()
    window.title("Schedule")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.configure(background="white")

    height = len(full_sched)
    width = len(full_sched[0])
    for i in range(height):
        for j in range(width):

            if i == 0:
                b = Label(window, text=full_sched[i][j], width=15, height=7, borderwidth=2, relief="solid", bg="white", font=("Arial Bold", 18), fg="red" )
                b.grid(row=i, column=j)
            elif j == 0:
                b = Label(window, text=full_sched[i][j], width=15, height=7, borderwidth=2, relief="solid", bg="white", font=("Arial Bold", 18), fg="blue" )
                b.grid(row=i, column=j)
            else:
                b = Label(window, text=full_sched[i][j], width=15, height=7, borderwidth=2, relief="solid", bg="white", font=("Arial Bold", 18), fg="black" )
                b.grid(row=i, column=j)

    window.mainloop()
    clear()
    schedules(name)

def schedule_edit(name, medicines):
    full_sched = get_current_sched(name)
    print(colored('Enter A to Add an Entry | Enter D to Remove an Entry', 'red').center(columns))
    print(colored('Enter R to return to previous tab', 'blue').center(columns))
    print(colored('Enter Q to quit the program', 'blue').center(columns))
    enter_in = input()
    while enter_in != 'A' and enter_in != 'D' and enter_in != 'R' and enter_in != 'Q':
        enter_in = input()
    clear()
    if enter_in == 'A':
        clear()
        print(colored('Pick the day for the entry according to the number', 'red').center(columns))
        for i in range(1, len(full_sched[0])):
            print(f'{i} - {full_sched[0][i]}')
        
        day_p = int(input())

        clear()

        print(colored(f'Pick the time for the entry according to the number on {full_sched[0][day_p]}', 'red').center(columns))
        for i in range(1, len(full_sched)):
            print(f'{i} - {full_sched[i][0]}')
        
        time_p = int(input())

        clear()

        if len(medicines):
            print(colored(f'Pick the medicine according to the number for {full_sched[0][day_p]} {full_sched[time_p][0]}', 'red').center(columns))
            for i in range(len(medicines)):
                print(f'{i + 1} - {medicines[i]}')
            
            med_p = int(input())

            full_sched[time_p][day_p] = medicines[med_p - 1]

            update_sched(name, full_sched)

            print(colored('Entry Successfully Added', 'red').center(columns))
            time.sleep(3)
            clear()
            schedule_edit(name, medicines)
        else:
            print(colored('No medicines in database. Add a new medicine', 'red').center(columns))
            time.sleep(3)
            clear()
            schedule_edit(name, medicines)

    elif enter_in == 'D':
        clear()
        print(colored('Pick the day to remove the entry from according to the number', 'red').center(columns))
        for i in range(1, len(full_sched[0])):
            print(f'{i} - {full_sched[0][i]}')
        
        day_p = int(input())

        clear()

        print(colored(f'Pick the time to remove the entry from according to the number on {full_sched[0][day_p]}', 'red').center(columns))
        for i in range(1, len(full_sched)):
            print(f'{i} - {full_sched[i][0]}')
        
        time_p = int(input())

        clear()

        full_sched[time_p][day_p] = '\n'

        update_sched(name, full_sched)

        print(colored('Entry Successfully Removed', 'red').center(columns))
        time.sleep(3)
        clear()
        schedule_edit(name, medicines)

    elif enter_in == 'R':
        schedules(name)
    else:
        return         
        
def medicinesf(name):
    medicines = get_curr_medicines(name)

    print(colored('Enter V to View your Medicines | Enter E to Edit your Medicines', 'red').center(columns))
    print(colored('Enter R to return to previous tab', 'blue').center(columns))
    print(colored('Enter Q to quit the program', 'blue').center(columns))
    enter_in = input()
    while enter_in != 'V' and enter_in != 'E' and enter_in != 'R' and enter_in != 'Q':
        enter_in = input()
    clear()
    if enter_in == 'V':
        medicine_view(name, medicines)
    elif enter_in == 'E':
        medicine_edit(name, medicines)
    elif enter_in == 'R':
        home(name)
    else:
        return

def schedules(name):

    try:
        with open(f'users/{name}/medicines.txt') as f_in:
            medicines = f_in.readlines()
    except FileNotFoundError:
        medicines = []
        pass

    basic_data = [["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                ["Morning", "", "", "", "", "", "", ""],
                ["Afternoon", "", "", "", "", "", "", ""],
                ["Evening", "", "", "", "", "", "", ""]]
    try:
        os.mkdir(f'users/{name}/schedules')
    except FileExistsError:
        pass

    for i in range(len(basic_data)):

        if os.path.exists(f'users/{name}/schedules/schedule{i}.txt'):
            pass
        else:
            with open(f'users/{name}/schedules/schedule{i}.txt', 'w') as f_out:
                for j in range(len(basic_data[i])):
                    f_out.write(f'{basic_data[i][j]}\n')
    
    print(colored('Enter V to View Schedule | Enter E to Edit Schedule', 'red').center(columns))
    print(colored('Enter R to return to previous tab', 'blue').center(columns))
    print(colored('Enter Q to quit the program', 'blue').center(columns))
    enter_in = input()
    while enter_in != 'V' and enter_in != 'E' and enter_in != 'R' and enter_in != 'Q':
        enter_in = input()
    clear()
    if enter_in == 'V':
        schedule_view(name, medicines)
    elif enter_in == 'E':
        schedule_edit(name, medicines)
    elif enter_in == 'R':
        home(name)
    else:
        return

def home(name):
    print(colored('Enter S for Schedule options | Enter M for Medicine options', 'red').center(columns))
    print(colored('Enter R to return to previous tab', 'blue').center(columns))
    print(colored('Enter Q to quit the program', 'blue').center(columns))
    enter_in = input()
    while enter_in != 'S' and enter_in != 'M' and enter_in != 'R' and enter_in != 'Q':
        enter_in = input()
    clear()
    if enter_in == 'S':
        schedules(name)
    elif enter_in == 'M':
        medicinesf(name)
    elif enter_in == 'R':
        main()
    else:
        return

def existing():
    try:
        users = os.listdir('users')
        if len(users):
            pass
        else:
            print(colored('No Existing Users. Create a New User', 'red').center(columns))
            time.sleep(3)
            main()
    except FileNotFoundError:
        print(colored('No Existing Users. Create a New User', 'red').center(columns))

    print(colored('Select your name by entering the corresponding number\n\n', 'red').center(columns))

    for i in range(len(users)):
        print(colored(f'{i + 1} - {users[i]}'))

    print('\n')

    chosen_user = int(input())
    password = maskpass.askpass(prompt = f'Enter the password for {users[chosen_user - 1]} : ', mask = '*')

    with open(f'users/{users[chosen_user - 1]}/password.txt') as f_in:
        actual_password = f_in.readline()

    if password == actual_password:
        clear()
        home(users[chosen_user - 1])
    else:
        print(colored('Incorrect Password', 'red').center(columns))
        time.sleep(3)
        clear()
        main()

def newacc():
    name = input('Enter your name : ')
    password = maskpass.askpass(prompt = f'Enter the password you will use for {name} : ', mask = '*')

    try:
        os.mkdir(f'users/{name}')
        with open(f'users/{name}/password.txt', 'w') as f_out:
            f_out.write(password)
    except FileExistsError:
        print('Contact Already Exists')
    
    print(colored(f'\nUser {name} created. Please choose existing user to log in', 'red').center(columns))
    time.sleep(3)
    clear()
    main()

def main():
    clear()
    try:
        os.mkdir('users')
    except FileExistsError:
        pass

    print(colored(figlet_format('MedTrack', font='big'), 'red').center(columns))
    print(colored('Enter E for existing user | Enter N for New User', 'red').center(columns))
    enter_in = input()
    while enter_in != 'E' and enter_in != 'N':
        enter_in = input()
    clear()
    if enter_in == 'E':
        existing()
    elif enter_in == 'N':
        newacc()

if __name__ == "__main__":
    main()
