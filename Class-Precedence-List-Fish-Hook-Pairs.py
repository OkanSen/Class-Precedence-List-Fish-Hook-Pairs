from copy import deepcopy


     ###################### SEVERAL METHODS ######################
#######################################################################
def print_list(list):

    for item in list:
        print(item)
        print()

def assert_class(list,node):
    if not node in list:
        list.append(node)


def find_exposed(list,procedures,CPL):
    exposed_list = []

    for temp_node in list:
        referenced = False

        # This short loop checks if the current class is in another fish hook's right side
        # If yes, it is maked as referenced
        for temp_node2 in list:
            if (temp_node[0] == temp_node2[1]):
                referenced = True
                break

        if not referenced:
            # Here we will store current exposed classes
            # There might be multiple exposed classes
            if not temp_node[0] in exposed_list:
                exposed_list.append(temp_node[0])
    print("CPL ",CPL)
    #print(exposed_list)
    # If we have more than one exposed classes we need
    # to figure out which one to use
    if (len(exposed_list) > 1):
        # Rightmost class in CPL, iterate from right to left
        if len(CPL) != 0:
            for i in reversed(CPL):
                # Check for all current exposed classes
                for exposed in exposed_list:
                    search_node = [i,"ako",exposed]
                    search_node2 = [i,"is-a",exposed]
                    
                    if search_node in procedures:
                        return exposed
                    if search_node2 in procedures:
                        return exposed
        else:
            # If CPL is empty return first exposed
            return exposed_list[0]
    else:
        # If CPL has only 1 element in it, then return that element
        return exposed_list[0]
    

               
 ###################### FISH HOOK ALGORITHM ######################
##################################################################
def fish_hook(SquaresProcedure):
    squares_copy = deepcopy(SquaresProcedure)
    fish_list = []

    # Iterate through the given example
    while (squares_copy):
        # Store first index
        item = squares_copy[0]
        
        tmp_name = item[0]
        check_name = item[2]
        
        hook = (tmp_name,check_name)
        # Add the hook to the fish list and pop first index
        fish_list.append(hook)
        squares_copy.pop(0)

        # If there are other children of the popped class, we store the first child name of
        # popped class and with this way we start creating a fish hook like structure
        count = 0
        for item2 in squares_copy:
            
            if item2[0] == tmp_name:
                hook = (check_name,item2[2])
                fish_list.append(hook)
                check_name = item2[2]
                squares_copy.pop(count)
                count -= 1
            count += 1
    return fish_list   



   ###################### CPL ALGORITHM ######################
##################################################################


def CPL_Algo(SquaresProcedure,fish_list):
    CPL = []
    squares_copy = deepcopy(SquaresProcedure)
    fish_copy = deepcopy(fish_list)

    # This loop will continue until all indexes are popped
    while fish_copy:
        # Call method to find all exposed classes, which returns only one exposed class
        # according to Winston's rules. see pg 191
        exposed = find_exposed(fish_copy,squares_copy,CPL)
        assert_class(CPL,exposed)   # add this exposed class to CPL
        index = 0
        print("exposed is ",exposed)

        # Iterate through all the fish list and pop all the instances where exposed class is mentioned at left side
        while (1):
            # Size check for loop break
            if index > len(fish_copy)-1:
                break
            item = fish_copy[index]
            if item[0]==exposed:
                last_node = fish_copy.pop(index)

                # This if is only used for the last index is popped
                # So to store and add the last class to the CPL
                if not fish_copy:
                    assert_class(CPL,last_node[1])

                index -= 1
            index += 1
        print()
    return CPL




    
#######################################################################
        ###################### MAIN ######################

# All examples are stored in a big list. Each example is in a separate index
SquaresProcedures = [[["Squares","ako","Rectangles"], 
        ["Squares","ako","Rhombuses"], 
        ["Rectangles","ako","Isosceles Trapezoids"], 
        ["Rectangles","ako","Parallelograms"],
        ["Rhombuses","ako","Parallelograms"],
        ["Rhombuses","ako","Kites"],
        ["Isosceles Trapezoids","ako","Cyclic Quadrilaterals"],
        ["Isosceles Trapezoids","ako","Trapezoids"],
        ["Parallelograms","ako","Trapezoids"],
        ["Cyclic Quadrilaterals","ako","Quadrilaterals"],
        ["Trapezoids","ako","Quadrilaterals"],
        ["Kites","ako","Quadrilaterals"]],


                    [["Squares","ako","Rectangles"],
                    ["Squares","ako","Rhombuses"], 
                    ["Rectangles","ako","Parallelograms"],
                    ["Rhombuses","ako","Parallelograms"],
                    ["Parallelograms","ako","Quadrilaterals"],
                    ["Rhombuses","ako","Kites"],
                    ["Kites","ako","Quadrilaterals"],
                    ["Rectangles","ako","Cyclic Quadrilaterals"],
                    ["Cyclic Quadrilaterals","ako","Quadrilaterals"],
                    ["Isosceles Trapezoids","ako","Cyclic Quadrilaterals"],
                    ["Isosceles Trapezoids","ako","Trapezoids"],
                    ["Trapezoids","ako","Quadrilaterals"]],

                    [["Crazy","is-a","Professors"],
                    ["Crazy","is-a","Hackers"],
                    ["Professors","ako","Eccentrics"],
                    ["Professors","ako","Teachers"],
                    ["Hackers","ako","Eccentrics"],
                    ["Hackers","ako","Programmers"],
                    ["Eccentrics","ako","Dwarfs"],
                    ["Teachers","ako","Dwarfs"],
                    ["Programmers","ako","Dwarfs"],
                    ["Dwarfs","ako","Everything"],
                    ["Jacque","is-a","Weightlifters"],
                    ["Jacque","is-a","Shotputters"],
                    ["Jacque","is-a","Athletes"],
                    ["Weightlifters","ako","Athletes"],
                    ["Weightlifters","ako","Endomorphs"],
                    ["Shotputters","ako","Athletes"],
                    ["Shotputters","ako","Endomorphs"],
                    ["Athletes","ako","Dwarfs"],
                    ["Endomorphs","ako","Dwarfs"]]]

# Call fish hook and CPL methods for each index 
count = "A"
for procedure in SquaresProcedures:
    procedure_fish_hook_list = fish_hook(procedure) 
    print("\n\n")
    print("###########################################################################################")
    print("###########################################################################################")
    print("------------------------ Fish Hook List for Example ", count, " ------------------------")
    
    print_list(procedure_fish_hook_list)
    print("\n\n")
    
    
    CPL = CPL_Algo(procedure,procedure_fish_hook_list)

    print("------------------------ Class Precedence List for Example ", count, " ------------------------")

    print_list(CPL)
    print("###########################################################################################")
    print("###########################################################################################")
    print("\n\n")
    count = ord(count[0])
    count += 1
    count = chr(count)



 