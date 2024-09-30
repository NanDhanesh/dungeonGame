class Player:

    #The initialised attributes need to be passed on construction of an object - only health needs to be passed in this case
    def __init__(self, health) -> None:
        self.__Health = health
        self.__Location = None
        self.__Inventory = []

    #self shows method is changing self (the instance of the class)
    def AddItem(self, item) -> None: #None function annotation shows that function/method will return nothing
        self.__Inventory.append(item)

    #shows that the health for the self instance will be returned
    def GetHealth(self) -> int: #Int function annotation shows GetHealth will return an integer (which is health)
        return self.__Health

    def SetHealth(self, health) -> None:
        self.__Health = health

    def GetLocation(self) -> str: #Str function annotation shows GetLocation will return an string (which is location)
        return self.__Location


    def SetLocation(self, location) -> None:
        self.__Location = location
        print(self.__Location.GetDescription())

    def AdjustHealth(self, health) -> int:
        self.__Health += health
        return self.__Health




    def DoCommand(self, command)->str:
        if command == "QUIT":
            return True
        
        instructions = command.split(' ')

        if instructions[0] == "look":
            print(self.__Location.GetDescription())

        elif instructions[0] == "health":
            print("you have {} health".format(self.__Health))

        elif instructions[0] == "move" or instructions[0] == "go":
            if len(instructions) <= 1:
                print("Move where?")
            else:
                self.__Move(instructions[1])
        elif instructions[0] == "get" or instructions[0] == "take":
            self.__Inventory.append(self.__Location.RemoveItem(instructions[1]))
            #Can only examine what is in my inventory but not if the name has 2 words see notes below
        elif instructions[0] == "examine":
            if len(instructions) <= 1:
                print("Examine What?")
            else:
                for i in range(len(self.__Inventory)):
                    if instructions[1] == self.__Inventory[i].GetName():
                        print(self.__Inventory[i].GetDescription())
        elif instructions[0] == "eat":
            if len(instructions) <= 1:
                print("Eat What?")
            else:
                self.__Eat(instructions[1])
        elif instructions[0] == "inventory" or instructions[0] == "i":
            items = "\n"
            if len(self.__Inventory) > 0:
                if len(self.__Inventory) == 1:
                    items += "You have the following item: {}".format(self.__Inventory[0].GetName())
                else:
                    items += "You have the following items: {}".format(self.__Inventory[0].GetName())
                    for i in range(1,len(self.__Inventory)-1):
                        items += ", " + self.__Inventory[i].GetName()
                    items += " and {}".format(self.__Inventory[len(self.__Inventory)-1].GetName())
            else:
                items += "You aren't carrying anything"
            print(items)
        else:
            print("You can't do that")
            return False

    def __Move(self, direction)-> None:
        exits = self.__Location.GetDirections()
        directionFound = False

        for i in range(len(exits)):
            if direction == exits[i]:
                directionFound = True
                if not self.__Location.GetConnections()[i].GoThrough(self,direction):
                    print("You can't go {}".format(direction))
        if not directionFound:
            print("There is no exit to the {}".format(direction))

    #Double underscore indicates Eat method is private
    def __Eat(self,food):
        foodPosition = 0
        for i in range(len(self.__Inventory)): #All these attributes are also public
            if self.__Inventory[foodPosition].GetName() == "food":
                self.__Health += self.__Inventory[foodPosition].GetHeals()
                self.__Inventory.RemoveAt(foodPosition)

        

class Connection:
    def __init__(self, roomFrom, roomTo, direction) -> None:
        self.__RoomFrom = roomFrom
        self.__RoomTo = roomTo
        self.__Direction = direction

    def GoThrough(self,player, direction) -> bool:
        if player.GetLocation() == self.__RoomFrom and direction == self.__Direction:
            player.SetLocation(self.__RoomTo)
            return True
        else:
            return False
    
    def GetDirection(self):
        return(self.__Direction)




class Item:
    def __init__(self, name, description) -> None:
        #should these not be protected rather than private otherwise the subclass can
        #not access them - I have made protected SFO has not for C#
        self._Name = name 
        self._Description = description

    def GetHeals(self) -> int:
        return 0

    def GetName(self) -> str:
        return self._Name #Attributes are protected

    def SetName(self, name) -> None:
        self._Name = name
    
    def GetDescription(self) -> str:
        return self._Description

    def SetDescrption(self, description) -> str:
        self._Desription = description


class FoodItem(Item):
    def __init__(self, name, description, heals) -> None:
        super().__init__(name, description) #invoking the super constructor of the parent class
        #https://www.delftstack.com/howto/python/python-call-super-constructor/
        self.__HealAmount = heals #attribute is only in the child class

    def GetHeals(self) -> int:
        return self.__HealAmount


class Room:
    def __init__(self, description) -> None:
        self.__Description = description
        self.__Contents = []
        self.__Connections = []

    def AddItem(self,item) -> None:
        self.__Contents.append(item)

    def RemoveItem(self, name) -> str:
        for item in self.__Contents:
            if item.GetName() == name:
                self.__Contents.remove(item)
                print(name,"has been removed from the room and added to your inventory")#added this line
                return item
        return None
    
    def AddConnection(self, connection) -> None:
        self.__Connections.append(connection)


    def GetDirections(self) -> str:
        directions = []
        for connection in self.__Connections:
            directions.append(connection.GetDirection())
        return(directions)

    def GetConnections(self) -> list:
        return(self.__Connections)

    def GetDescription(self) -> str:
        items = "\n"
        if len(self.__Contents) > 0:
            if len(self.__Contents) == 1:
                items += "You can see the following item: {}".format(self.__Contents[0].GetName()) 
            else:
                items += "You can see the following item: {}".format(self.__Contents[0].GetName())
                for i in range(1,len(self.__Contents)-1):
                    items += ", " + self.__Contents[i].GetName()
                items += " and {}".format(self.__Contents[len(self.__Contents)-1].GetName())
        else:
            items = ""

        exits = "\n"
        if len(self.__Connections) > 0:
            if len(self.__Connections) == 1:
                exits += "There is an exit to the {}".format(self.__Connections[0].GetDirection())
            else:
                exits += "There are exits to the {}".format(self.__Connections[0].GetDirection())
                for i in range(1,len(self.__Connections)-1):
                    exits += ", " + self.__Connections[i].GetDirection()
                exits += " and {} ".format(self.__Connections[len(self.__Connections)-1].GetDirection())
        else:
            exits = "There are no visible exits"

        return self.__Description + items + exits

    def GetContents(self) -> list:
        return self.__Contents

    def SetDescription(self, description) -> None:
        self.__Description = description


command = ""
gameOver = False

# initialising the game
print("Welcome Message...")
startRoom = Room("You are in the starting cave.")
lavaRoom = Room("You are in a dark cave with a glowing river of lava.")
apple = FoodItem("apple", "a beautiful green apple, it looks delicious.",10)
redApple = FoodItem("Red apple", "a beautiful rosy red apple, it looks delicious.", 10)
stoneApple = Item("Stone apple", "a beautiful apple made of stone.")
water = Item("water", "Evian, the best!.")
glass = Item("glass", "glassy glass.")

startRoom.AddConnection(Connection(startRoom, lavaRoom, "north"))
lavaRoom.AddConnection(Connection(lavaRoom, startRoom, "south"))
startRoom.AddItem(apple)
startRoom.AddItem(glass)

pc = Player(100)



pc.SetLocation(startRoom)
pc.AddItem(redApple)
pc.AddItem(stoneApple)
pc.AddItem(apple)


while not gameOver:
    command = input("What would you like to do? ")
    gameOver = pc.DoCommand(command)

print("Thank you for playing Dunegon! See you again soon, brave dungeoneer.")

#Don't seem to be able to examine objects that have 2 words in their name e.g.
#can examine glass and apple but not Red apple
