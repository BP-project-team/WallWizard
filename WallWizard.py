def wall_placement(wall_location1,wall_location2):
    print("salam")
def movement(kind_of_move):
    print("chetoriayi")
def movement_choice():
    choice=input("To place a wall type(wall) or if you want to move, type(move): ")
    if choice == "move":
        try:
            true=1
            while true:
                kind_of_move=input("type(w) to go forward,(d) to go right,(a) to go left and (s) to go bottom: ")
                if kind_of_move in ["w","d","a","s"]:
                    if kind_of_move=="w":
                        true-=1
                        movement("w")
                    if kind_of_move=="d":
                        true-=1
                        movement("d")
                    if kind_of_move=="a":
                        true-=1
                        movement("a")
                    if kind_of_move=="s":
                        true-=1
                        movement("s")     
                else:
                    print("When you choose to move your choice are limited to go forward(w) or right(d) or left(a) or bottom(s).")
        except:
            print("When you choose to move your choice are limited to go forward(w) or right(d) or left(a) or bottom(s).")
            return movement_choice()
    if choice=="wall":
        try:
            true=1
            while true:
                wall_location1=map(int,input("Enter first coordinate in form of (x y) like 2 0:").split())
                if not wall_location1.isdigit():
                    print("Cordinates should be in form of (x, y) like 0 2.")
                wall_location2=map(int,input("Enter second coordinate in form of (x y) like 2 1:").split())
                if not wall_location2.isdigit():
                    print("Cordinates should be in form of (x, y) like 0 2.")
                else:
                    true-=1
                wall_placement(wall_location1,wall_location2)
        except: 
            print("Cordinates should be in form of (x, y) like 0 2.")
            return movement_choice()