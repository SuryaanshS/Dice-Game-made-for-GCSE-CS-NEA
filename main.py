from random import randint

validUsernames = []
validPasswords = []

#Retrieves login credentials and stores usernames and passwords in separate lists
with open("AuthorisedUsers.txt") as file:
    for line in file:
        username, password = line.rstrip("\n").split(",")
        validUsernames.append(username.upper())
        validPasswords.append(password)

def login():
    while True:
        user = input("ENTER YOUR USERNAME: ").upper()
        if user in validUsernames:
            print("USERNAME AUTHORISED")
            print("================================")
            #Matches the username to its specific password by finding the index of the list
            index = validUsernames.index(user)
            password = input("ENTER YOUR PASSWORD: ")
            if password == validPasswords[index]:
                print("PASSWORD AUTHORISED. WELCOME")
                print("================================")
                return user
            else:
                print("INCORRECT PASSWORD")
                print("================================")
        else:
            print("INCORRECT USERNAME")
            print("================================")

def calcPoints(score):
    dice1 = randint(1,6)
    dice2 = randint(1,6)
    print(f"You rolled {dice1} and {dice2}")
    #Uses modulo to check if the sum of the dice is even or odd
    if (dice1 + dice2) % 2 == 0:
        print("THE SUM IS EVEN")
        points = dice1 + dice2 + 10
        if dice1 == dice2:
            print("YOU ROLLED DOUBLES! ROLL ANOTHER DICE")
            dice3 = randint(1,6)
            points += dice3
    else:
        print("THE SUM IS ODD")
        points = dice1 + dice2 - 5
    if score + points < 0:
        return 0, points
    else:
        return score + points, points

def tiebreaker(player1, player2):
    print("\n================================")
    print("IT'S A TIE. ROLL ONE MORE DICE EACH:")
    score1 = randint(1,6)
    print("PLAYER 1:")
    print(f"You rolled {score1}")
    score2 = randint(1,6)
    print("PLAYER 2:")
    print(f"You rolled {score2}")
    #Uses indirect recursion to find the new winner using the tiebreaker score
    return findWinner(player1, player2, score1, score2)

def findWinner(player1, player2, score1, score2):
    if score1 > score2:
        return player1
    elif score2 > score1:
        return player2
    else:
        return tiebreaker(player1, player2)

def getLeaderboard():
    scores = []
    with open("Leaderboard.txt") as file:
        for line in file:
            user, score = line.rstrip("\n").split(",")
            #Stores the line's data as a tuple to sort by the score
            scores.append((int(score), user))
        scores.sort(reverse=True)
        for x in range(5):
            #Prevents 'out of range' error
            if x + 1 <= len(scores):
                print(f"{x+1}. {scores[x][1]}: {scores[x][0]}")
            else:
                #Causes remaining leaderboard slots to display 'N/A' if no data exists
                print(f"{x+1}. N/A")

def main():
    print("================================")
    print("LOGIN FOR PLAYER 1:")
    player1 = login()
    print("\n================================")
    print("LOGIN FOR PLAYER 2:")
    player2 = login()
    #Prevents player 1 and player 2 from logging into the same account
    while player2 == player1:
        print("INVALID. PLAYER 1 AND PLAYER 2 CANNOT BE THE SAME. LOGIN AGAIN PLAYER 2:")
        player2 = login()
    score1 = 0
    score2 = 0
    for i in range(1, 6):
        print("\n================================")
        print(f"ROUND {i}:")
        print("PLAYER 1:")
        score1, points1 = calcPoints(score1)
        print(f"YOU GOT {points1} POINTS THIS ROUND. YOUR TOTAL SO FAR IS: {score1}")
        print("PLAYER 2:")
        score2, points2 = calcPoints(score2)
        print(f"YOU GOT {points2} POINTS THIS ROUND. YOUR TOTAL SO FAR IS: {score2}")
        print("================================")
    winner = findWinner(player1, player2, score1, score2)
    print("\n================================")
    print(f"WINNER: {winner.upper()}")
    print("================================")
    with open("Leaderboard.txt", "a") as file:
        if winner == player1:
            file.write(f"{winner.upper()},{score1}\n")
        else:
            file.write(f"{winner.upper()},{score2}\n")
    print("\n================================")
    print("        TOP 5 LEADERBOARD        ")
    print("================================")
    getLeaderboard()
    print("================================")

main()