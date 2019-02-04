#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 19:35:09 2018

@author: pongtit

Working Directory:
/Users/pongtit/Desktop/PythonCourse

Purpose:
To build a text adventure games for assignment, fun and learning!
Good to learn about this as my baby step of coding!!
"""

###############################################################################
############## Part 1: Launch the Star Fighter! ###############################
###############################################################################

"""
Docstrings:
    
    Introduction:
        
        In this game, you will play as a pilot from Rebell Alliance and fight
        against empire army. Your mission is going through the battlefield
        and destroy empire mother ship 'Imperial Star Destroyer'. However,
        it is not easy to go through the whole battlefield without facing any
        strong enemy. Therefore, you will face one of empire ace pilot called
        'Imperial Ace'.
        
    The stages of the game are as following:
        
        Stage 1: Introduction to mission
        Stage 2: Fighting against first enemy
            Nested Condition
        Stage 3: Fighting the enemy with your team
            Nested Condition
        Stage 4: Fighting enemy ace "Imperial Ace"
            While loop
            Nested Condition
        Stage 5: Destroy objective "Imperial Star Destroyer"
            While loop
            Nested Condition
        Fail: You lose the game
    
    Identify bug that are not yet worked out
        No bug founded yet.    
"""


def stage_1():
    
    print("\f")
    
    print("STAGE: Start your mission!")
    
    print("Welcome to Star Fighter please enter your pilot code")
    
    user_name = input("> ")
    
    print("\f")
    
    print(f"{user_name} affirmative! Pilot recognize and ready to initiate")
    
    input("Press Enter to start the engine!")
    
    print("\f")
    
    print(f"""Operator: \n\tPilot code {user_name} is ready to launch.
          \n\tYour mission is destroy the empire mother ship 
          \n\t"Imperial Star Destroyer"
          \n\tHope you success and return back to Rebellion Settlement safely.
          """)
    
    input(">Press Enter to launch Star Fighter!<")
    
    stage_2()

###############################################################################
################### Part 2: Facing first enemy! ###############################
###############################################################################

def stage_2():
    
    print("\f")
    
    print("STAGE: First enemy!")
    
    print("""\nNow you are in the middle of space war!
          \nThis is very challenging mission which you must success!!
          """)
    
    input(">Press Enter when you are ready to start your mission<")
    
    print("\f")
    
    print("""You are facing enemy Twin Ion Engine Fighter!!
          \nPlease select your action carefully
          """)
    
    print("\n1. Start firing one-on-one fight")
    
    print("\n2. Try to avoid the battle and escape with your fighter speed")
    
    print("\n3. Waiting for backup")
    
    choice = input("> ")
    
    if '1' in choice or 'ir' in choice :
        
        print("\f")
        
        print("You're losing against enemy and your Star fighter is destroyed")
        
        fail()
        
    elif '2' in choice or 'void' in choice :
        
        print("\f")
        
        print("You escape enemy with your speed!")
        
        input(">Press Enter to continue your mission<")
        
        stage_4()
        
    elif '3' in choice or 'ait' in choice :
        
        print("\f")
        
        print("You're making distance with enemy fighter and wait for backup")
        
        input(">Press Enter to contact your team")
        
        stage_3()
        
    else:
        
        print("\f")
        
        print("Invalid entry. Please try again")
        
        input(">Press Enter to retry<")
        
        stage_2()
        
###############################################################################
################# Part 3: Fight first enemy with team #########################
###############################################################################

def stage_3(): #If user decide to wait for back up they will come to this stage
    
    print("\f")
    
    print("STAGE: Together we strong!")
    
    print("\nYour team members are here!")
    
    print("\nWhat will you do?")
    
    print("\n1. Firing enemy fighter together with your team to beat him")
    
    print("\n2. Left the enemy to your team member and go after the mission")
    
    choice_2 = input("> ")
    
    if '1' in choice_2 or 'ir' in choice_2:
        
        print("\f")
        
        print("You successfully finish the enemy fighter!!")
        
        input(">Press Enter to continue your mission<")
        
        stage_4()
        
    elif '2' in choice_2 or 'eft' in choice_2:
        
        print("\f")
        
        print("Enemy fighter decide to fire you!")
        
        import random
        
        if random.randint(0,2) == 1:
        
            print("You could not dodge all of them!!!")
        
            input(">Press Enter to continue<")
            
            fail()
        
        else:
            
            print("You managed to dodge it!")
            
            stage_3()
        
    else:
        
        print("\f")
        
        print("invalid entry. Please try again")
        
        input(">Press Enter to retry")
        
        stage_3()
    
###############################################################################
################ Part 4: Face enemy ace pilot!! ###############################
###############################################################################

def stage_4(): 
    
    print("\f")
    
    print("Stage: Facing ace pilot!")
    
    print("""\nOperator: The enemy ace "Imperial Ace" is here! 
             \nYou could not proceed without destroying him!!
             \nPlease be careful because he is really strong.
          """)
    
    import random
    
    input(">Press Enter to start firing missiles!!<")
    
    print("\f")
    
    hp = 3 #player hp
    
    hp_2 = 3 #enemy hp
    
    rand = random.randint(0,5)
    
    while hp_2 > 0 and hp > 0:
        if rand == 0 or rand == 1 or rand == 2 or rand == 3:
            hp_2 -= 1
            rand = random.randint(0,5)
            print("\nYou hit the enemy!! Continue like this")
        else:
            hp -= 1
            rand = random.randint(0,5)
            print("\nYou missed, the enemy attacked you. Keep shooting!")
            
        input(">Press Enter to continue shooting<")
        print("\f")    
    
    if hp_2 == 0:
        
        print("\f")
        
        print("""Operator: You have successfully destroy "Imperial Ace"! 
          \nGood job! Now it is time to move on to your main mission.
          \nPlease proceed to destroy "Imperial Star Destroyer"
          """)
        input(">Press Enter to continue your mission")
        
        stage_5()
    
    elif hp == 0:
        
        print("\f")
        print("""The enemy "Imperial Ace" destroyed you.""")
        
        input(">Press Enter to continue<")
        
        fail()
        
    else:
        print("\f")
        print("invalid entry. Please try again")
        
        input(">Press Enter to retry")
        
        stage_4()

###############################################################################
############## Part 5: Time to destroy the objective ##########################
###############################################################################

def stage_5(): 
    
    print("\f")
    
    print("FINAL STAGE: Objective is here!")
    
    print("""\nOperator: Target confirmed! Your objective,
              \n"Imperial Star Destroyer" is in front of you. 
              \nPlease destroy the objective to complete mission.
          """)
    
    print("""Please select your action carefully!
          1. Launch missles to the "Imperial Star Destroyer"
          2. Run away from a mission
          """)
    
    choice_3 = input("> ")
    
    if '1' in choice_3 or 'aunch' in choice_3:
    
        print("\f")
    
        print("Operator: Good job! You destroyed enemy 'Imperial Star Destoryer'!!") 
    
        print("\nOperator: Mission Success. Please return to Rebellion Settlement")
        
        print("""
 _____                             _         _       _   _             _ 
/  __ \                           | |       | |     | | (_)           | |
| /  \/ ___  _ __   __ _ _ __ __ _| |_ _   _| | __ _| |_ _  ___  _ __ | |
| |    / _ \| '_ \ / _` | '__/ _` | __| | | | |/ _` | __| |/ _ \| '_ \| |
| \__/\ (_) | | | | (_| | | | (_| | |_| |_| | | (_| | |_| | (_) | | | |_|
 \____/\___/|_| |_|\__, |_|  \__,_|\__|\__,_|_|\__,_|\__|_|\___/|_| |_(_)
                    __/ |                                                
                   |___/                                                 
               __   __              _    _ _       _ _ _                 
               \ \ / /             | |  | (_)     | | | |                
                \ V /___  _   _    | |  | |_ _ __ | | | |                
                 \ // _ \| | | |   | |/\| | | '_ \| | | |                
                 | | (_) | |_| |   \  /\  / | | | |_|_|_|                
                 \_/\___/ \__,_|    \/  \/|_|_| |_(_|_|_)                
                                                                
                 """)
    
        
    elif '2' in choice_3 or 'un' in choice_3:
        
        print("\f")
        
        print("The enemy is attacking you while you try to run away")
        
        choice_4 = input("""You have to dodge the attack!
                         \n1. Dodge to the left
                         \n2. Dodge to the right
                         \n3. Do not dodge
                         \n>""")
        if '1' in choice_4 or 'eft' in choice_4:
            print("\f")
            
            print("You dodged the attack!")
            
            input(">Press Enter to continue<")
            
            stage_5()
            
        elif '2' in choice_4 or 'ight' in choice_4:
            print("\f")
            
            print("You dodge the attack but hit the big rock in front of you")
            
            print("\n'Imperial Star Destroyer' destroyed your fighter")
        
            input(">Press Enter to continue<")
        
            fail()
            
        elif '3' in choice_4 or 'not' in choice_4:
            print("\f")
            
            print("You could not dodge the attack!")
        
            print("\n'Imperial Star Destroyer' destroyed your fighter")
        
            input(">Press Enter to continue<")
        
            fail()
        
    else:
        
        print("\f")
        
        print("invalid entry. Please try again")
        
        input(">Press Enter to retry")
        
        stage_5()

###############################################################################
################# Part Fail: Unfortunately you failed... ######################
###############################################################################

def fail():
    
    print("\f")
    
    print("""                     
  _______      ___      .___  ___.  _______      ______   ____    ____  _______ .______      
 /  _____|    /   \     |   \/   | |   ____|    /  __  \  \   \  /   / |   ____||   _  \     
|  |  __     /  ^  \    |  \  /  | |  |__      |  |  |  |  \   \/   /  |  |__   |  |_)  |    
|  | |_ |   /  /_\  \   |  |\/|  | |   __|     |  |  |  |   \      /   |   __|  |      /     
|  |__| |  /  _____  \  |  |  |  | |  |____    |  `--'  |    \    /    |  |____ |  |\  \----.
 \______| /__/     \__\ |__|  |__| |_______|    \______/      \__/     |_______|| _| `._____|
                                                                                             
       """)
    
    print("""\nThank you for playing
          \nPress 1 to play again
          \nPress 2 to exit
          """)
    
    fail_choice = input("> ")
    
    if fail_choice == "1":
        stage_1()
        
    elif fail_choice == "2":
        exit(0)
    
    else:
        print("\f")
        
        print("invalid entry. Please try again")
        
        input(">Press Enter to retry")
    
        fail()

stage_1() #start the game