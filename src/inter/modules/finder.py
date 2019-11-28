import os
import sys
import src.misc.primitives as primitives


# Allow us to import the client
this_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(this_dir)

message = "find:this16digittoken"


def led_on(shelf_num):
    pass
    #shelf_num
    #interface led
    #RPI GPIO module



def respond_start(message, sub_node, log_level):
    Primitives = primitives.Primitives(sub_node, log_level)

    arguments = Primitives.parse_cmd(message)
    print(arguments)
    part_number = arguments[1]
    print(part_number)
    """
    if part_number in inventory:
        part
    except:
        this pi does not have the part
    
    """

    ###


    """Called by the client's listener_thread when it received a [name]: flag"""

    #find shelf for item num
    return part_number

