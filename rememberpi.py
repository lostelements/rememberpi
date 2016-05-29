
import datetime
import RPi.GPIO as GPIO
from time import sleep

# Define the start week
startdate = datetime.date(2016,5,2)

# Define the led 4 led pins
blackled = 18
greenled = 17
brownled = 22
patchled = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(blackled,GPIO.OUT)
GPIO.setup(greenled,GPIO.OUT)
GPIO.setup(brownled,GPIO.OUT)
GPIO.setup(patchled,GPIO.OUT)


# Define  the button  pin
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#Define the 4 varibles for the timings
# array   colour,day, wwekly bi or monthly, time day monday=1
recycle = [greenled,7,'FT',10,'recycle']
rubbish = [blackled,7,'SF',10,'rubbish']
garden = [brownled,7,'FT',11,'garden']
patch1 = [patchled,1,'W',9,'patch1']
patch2 = [patchled,7,'W',12,'patch2']
whatled =[recycle,rubbish,garden,patch1,patch2]
           
# Turn on Each Led witrh a 2 second gap in between then turn off
GPIO.output(blackled,GPIO.HIGH)
sleep(2)
GPIO.output(greenled,GPIO.HIGH)
sleep(2)
GPIO.output(brownled,GPIO.HIGH)
sleep(2)
GPIO.output(patchled,GPIO.HIGH)
sleep(2)
GPIO.output(blackled,GPIO.LOW)
sleep(2)
GPIO.output(greenled,GPIO.LOW)
sleep(2)
GPIO.output(brownled,GPIO.LOW)
sleep(2)
GPIO.output(patchled,GPIO.LOW)

# defiune the led off function
def turn_off(channel):
    if (channel == 16):
        #turn off led
        GPIO.output(blackled,GPIO.LOW)
        print ("black")
    elif (channel == 19):
        GPIO.output(greenled,GPIO.LOW)
        print ("green")
    elif (channel == 20):
        GPIO.output(brownled,GPIO.LOW)
        print ("brown")
    else:
        GPIO.output(patchled,GPIO.LOW)
        print ("patch")
        
    

# add the event detect
GPIO.add_event_detect(16, GPIO.FALLING, callback=turn_off, bouncetime=200)
GPIO.add_event_detect(19, GPIO.FALLING, callback=turn_off, bouncetime=200)
GPIO.add_event_detect(20, GPIO.FALLING, callback=turn_off, bouncetime=200)
GPIO.add_event_detect(26, GPIO.FALLING, callback=turn_off, bouncetime=200)





def main():
# main loop
    startloop = 1
    while (startloop == 1) :
# get the current tie  (now)
               nowtime = datetime.datetime.now()
               nowdate = datetime.date.today()
               nowweekday = nowdate.isoweekday()
               #Calculate the number of weeks
               monday1 = (startdate - datetime.timedelta(days=startdate.weekday()))
               monday2 = (nowdate - datetime.timedelta(days=nowdate.weekday()))
               weekcount= (monday2 - monday1).days / 7
               nowday = nowdate.day
               nowhour = nowtime.hour
               howmany = len(whatled)
               count = 0
               print (nowhour,nowday,howmany,weekcount,nowweekday)
               while ( count < howmany):
                   
# check if day and hour are correct
                 print (whatled[count][1])
                 print (whatled[count][3])
                
                 if (whatled[count][1] == nowweekday) and (whatled[count][3] == nowhour):
#rtest is led already on (1 = off)
                     print ("got hour")
                     if (GPIO.input(whatled[count][0]) == 0):
                         print ("led off")
                         if (whatled[count][2] == "W"):
                             #every week
                             GPIO.output(whatled[count][0],GPIO.HIGH)
                         elif (weekcount % 2 == 0):
                             #even weeks
                             GPIO.output(whatled[count][0],GPIO.HIGH)
                         else:
                             #odd weeks
                             GPIO.output(whatled[count][0],GPIO.HIGH)
                             
#test for the correct week now using odd and even weeks
# trurn led on
# set deetect button
                    
                 count=count+1
                    
# wait 1 hour before retesting
               sleep(3600)
           
	
    return 0

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterupt:
        print ("key clean")
    except:
        print ("other error")
    finally:
        GPIO.cleanup()
