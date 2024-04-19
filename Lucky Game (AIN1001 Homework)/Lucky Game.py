import time
import random
print("\n")

print("\033[4mFor 1st player: \033[0m")
time.sleep(0.5)
p1lucky1 = int(input("Please choose your first lucky number between 11 - 99\n"))
p1lucky2 = int(input("Please choose your second lucky number between 11 - 99\n"))
p1penalty1 = int(input("Please choose your first penalty number between 11 - 99\n"))
p1penalty2 = int(input("Please choose your second penalty number between 11 - 99\n"))

print("\033[4mFor 2nd player: \033[0m")
time.sleep(0.5)
p2lucky1 = int(input("Please choose your first lucky number between 11 - 99\n"))
p2lucky2 = int(input("Please choose your second lucky number between 11 - 99\n"))
p2penalty1 = int(input("Please choose your first penalty number between 11 - 99\n"))
p2penalty2 = int(input("Please choose your second penalty number between 11 - 99\n"))

print("\n")

while (11<=p1lucky1<=99) and (11<=p1lucky2<=99) and (11<=p1penalty1<=99) and (11<=p1penalty2<=99) and (11<=p2lucky1<=99) and (11<=p2lucky2<=99) and (11<=p2penalty1<=99) and (11<=p2penalty2<=99):

    p1_loc = 1
    p2_loc = 1

    while (p1_loc < 100) and (p2_loc < 100):
        dice1 = random.randint(1,6)
        print("\033[4mP1's Turn\033[0m")
        time.sleep(0.5)
        cmd1 = input("Press enter to roll the dice")
        p1_loc += dice1
        time.sleep(1)
        print("Rolling...")
        time.sleep(2)
        if (p1_loc == p1lucky1) or (p1_loc == p1lucky2):
            p1_loc += 10
            print("\033[3m(+10) Lucky YAY :)\033[0m")
        elif (p1_loc == p1penalty1) or (p1_loc == p1penalty2):
            p1_loc -= 10
            print("\033[3m(-10) Unlucky :(\033[0m")
        print("P1's Location: ", p1_loc, "\n")
    
        print("\033[4mP2's Turn\033[0m")
        dice2 = random.randint(1,6)
        time.sleep(0.5)
        cmd2 = input("Press enter to roll the dice")
        p2_loc += dice2
        time.sleep(1)
        print("Rolling...")
        time.sleep(2)
        if (p2_loc == p2lucky1) or (p2_loc == p2lucky2):
            p2_loc += 10
            print("\033[3m(+10) Lucky YAY :)\033[0m")
        elif (p2_loc == p2penalty1) or (p2_loc == p2penalty2):
            p2_loc -= 10
            print("\033[3m(-10) Unlucky :(\033[0m")
        print("P2's Location: ", p2_loc, "\n")

    else:
        if (p1_loc >= 100) and (p1_loc > p2_loc):
            print("\033[1mP1 WINS\033[0m")
        elif (p1_loc == p2_loc):
            print("\033[1mBOTH PLAYER WINS\033[0m")
        else:
            print("\033[1mP2 WINS\033[0m")
        print("\n")
    break

else:
    print("...")
    time.sleep(2.5)
    print("\n", "Sorry, you didn't follow the rules correctly, next time read the instructions better...", "\n")

