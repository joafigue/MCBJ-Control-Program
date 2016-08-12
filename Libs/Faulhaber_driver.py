###################################
## Driver written by M.L. Perrin ##
## contact: m.l.perrin@tudelft.nl #
###################################

from visa import *
pitch = 150   # pitch of the differential screw, for exact value ask Mascha
gearbox = 246

##### GENERAL #######
def Faulhaber_command(command):
    # Sends a command through COM1 to the Faulhaber motor controller

    motor = SerialInstrument("COM3")
    motor.baud_rate = 9600   #57600             #### remember to set COM1 port to this baudrate!!!!!!!!!!!
    output = motor.ask(command)
    if command == 'pos':
        try:
            int(output)
        except:
            motor = SerialInstrument("COM3")
            motor.baud_rate = 9600             #### remember to set COM1 port to this baudrate!!!!!!!!!!!
            output = motor.ask(command)

    return output

def Faulhaber_convert_ums_to_rpm(ums):
    # Converts motor speed from um/s to rpm
    rpm = ums / pitch * gearbox * 60
    return rpm

def Faulhaber_convert_rpm_to_ums(rpm):
    # Converts motor speed from rpm to um/s
    ums = rpm / 60 / gearbox * pitch
    return ums

def Faulhaber_convert_um_to_counts(um):
    # Converts motor displacement from um to counts
    count = um / pitch * gearbox * 3000
    return count

def Faulhaber_convert_counts_to_um(count):
    # Converts motor displacement from counts to um
    um = count / 3000 / gearbox * pitch
    return um

def Faulhaber_step_motor(um,ums,direction):
    # Moves the motor . um = number of microns, ums = displacement speed (um/s), motor direction: breaking?
    Faulhaber_command('en')
    old_pos = int(Faulhaber_command('pos'))
    print "old pos : %1.0f" % old_pos
    step_count = Faulhaber_convert_um_to_counts(um)
    print "step count : %1.0f" % step_count

    speed = Faulhaber_convert_ums_to_rpm(ums)
    print "speed : %1.0f" % speed

    string = 'v '
    if direction:
        string = string + "%1.2f" % (-1*speed)
    else:
        string = string + "%1.2f" % speed

    Faulhaber_command(string)

    check = True

    while check:
        current_pos = int(Faulhaber_command('pos'))
        print "current pos : %1.0f" % current_pos
        if abs(current_pos - old_pos) >= step_count:
            Faulhaber_command('v 0')
            check = False

    Faulhaber_command('di')

    return

def Faulhaber_continuous(ums,breaking):
    # Moves the motor . um = number of microns, ums = displacement speed (um/s), motor direction: breaking?
    Faulhaber_command('en')
    speed = Faulhaber_convert_ums_to_rpm(ums)

    string = 'v '
    if breaking:
        string = string + "%1.2f" % (-1*speed)
    else:
        string = string + "%1.2f" % speed

    Faulhaber_command(string)

    return

def Faulhaber_move_to(pos, speed=2.0):
    pos = float(pos)
    # Moves the motor . um = number of microns, ums = displacement speed (um/s), motor direction: breaking?
    Faulhaber_command('en')
    speed = Faulhaber_convert_ums_to_rpm(speed)
    act_pos = int(Faulhaber_command('pos'))

    if abs(act_pos-pos) > 200:
        check= True
        if act_pos > pos:
            string = 'v ' + "%1.2f" % (-1*speed)

        else:
            string = 'v ' + "%1.2f" % speed

        Faulhaber_command(string)

        while check:
            act_pos = float(Faulhaber_command('pos'))
            print "pos = %d" % int(act_pos)
            if abs(act_pos-pos) < 300:
                check = False
                Faulhaber_command('v 0')
                print "pos = %d" % int(Faulhaber_command('pos'))
    else:
        print "pos = %d" % int(Faulhaber_command('pos'))

    Faulhaber_command('di')
    return

def Faulhaber_set_motor(pos):
    pos = float(pos)
    Faulhaber_command('en')
    Faulhaber_command('ho %d' % pos)
    print "new position %s" %Faulhaber_command('pos')
    Faulhaber_command('di')
    return
#print 'FaulHaber drivers loaded'
