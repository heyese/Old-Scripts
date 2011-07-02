

print "Welcome to Ghost\n\n"

# Function to get player names
def get_players():
    number = int(raw_input("Enter number of players"));
    print "The number of players is ",number
    player = [];
    for num in range(1,number + 1,1):
#        print num
        name = raw_input("Enter name of player " + repr(num));
        print "name is ",name
        player.insert(num,name);
    print "The players are: ", player
    return;


get_players();    