import math
import evdev
import _thread
import time

from Stepper import stepper

def print_time(threadName, delay,s,steps, dir,speed):
   count = 1
   while count >=1:
      time.sleep(delay)
      count -= 1
      #print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
      testStepper = stepper(s)
      testStepper.step(steps, dir,speed);
      
#[stepPin, directionPin, enablePin]
s1=[2,3,4]     #3,5,7--Rpi pins
s2=[17,27,22]  #11,13,15
s3=[10,9,11]   #19,21,23

######### Link Lenghts in cm.
l1=42
l2=36
######## Coordinates in xy frame in cm

ox = 66.4
oy = 4.6
oz = 0

#######Inverse Kinematics Equation for obtaining th joint angles -

oldtheta2=-math.degrees(math.acos((ox*ox+oy*oy-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
oldtheta1=math.degrees(math.atan(oy/ox) - math.atan((l2*math.sin(oldtheta2*math.pi/180))/(l1 + l2*math.cos(oldtheta2*math.pi/180))))
oldtheta3=math.degrees(math.acos(oz/(l1*math.cos(oldtheta1*math.pi/180) + l2*math.cos((oldtheta2 + oldtheta1)*math.pi/180))))

print(str(oldtheta1)+" oldtheta2:"+str(oldtheta2)+ " oldtheta3:"+str(oldtheta3))

ppr=1600  # Pulse Per Revolution

x = 17.8
y = 18.4
z = 0

theta2=-math.degrees(math.acos((x*x+y*y-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
theta1=math.degrees(math.atan(y/x) - math.atan((l2*math.sin(theta2*math.pi/180))/(l1 + l2*math.cos(theta2*math.pi/180))))
theta3=math.degrees(math.acos(z/(l1*math.cos(theta1*math.pi/180) + l2*math.cos((theta2 + theta1)*math.pi/180))))

# angles to be moved
a1=theta3 - oldtheta3 #base
a2=theta1 - oldtheta1 #link 1
a3=theta2 - oldtheta2 #link 2

print(str(theta1)+" theta2:"+str(theta2)+ " theta3:"+str(theta3))
print(str(a1)+" a2:"+str(a2)+ " a3:"+str(a3))

##a1=0  #base
##a2=-39  #link 1
##a3=0  #link 2

## Gear Ratios
g1=12.2  # base
g2=10   #link 1
g3=10    #link 2

# Calculation for step and Speed
step1=(ppr/360)*a1*g1  # base
step2=(ppr/360)*a2*g2  #link 1
step3=(ppr/360)*a3*g3  #link 2

# Calculation of timedelay for differnt motors
execTime=20

##----------------------------------------------
if (step1 == 0):
    td1 = 0
else :
    td1=abs((execTime-(step1*0.002))/step1)

if (step2 == 0):
    td2 = 0
else:
    td2=abs((execTime-(step2*0.002))/step2)

if (step3 == 0) :
    td3 = 0
else:
    td3=abs((execTime-(step3*0.002))/step3)
##---------------------------------------------------------------
if step1<0:
    dir1="r"
else:
    dir1="l"
    
if step2<0:
    dir2="l"
else:
    dir2="r"

if step3<0:
    dir3="l"
else:
    dir3="r"

_thread.start_new_thread( print_time, ("stepper-1", 0.2, s1,abs(step1),dir1,td1))
_thread.start_new_thread( print_time, ("stepper-3", 0.2, s3,abs(step3),dir3,td3)) 
_thread.start_new_thread( print_time, ("stepper-2", 0.2, s2,abs(step2),dir2,td2))
