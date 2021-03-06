from pymongo import MongoClient
import schedule
import time

##############
## This script will be deployed in bluemix with --no-route set to true
## This script performs a cron job which finds the most eligible customer for filling the seats in a particular time slots

##############
con = MongoClient("mongodb://abcd:qwerty@ds111798.mlab.com:11798/have_a_seat")
db = con.have_a_seat

cursor = db.Bookings.find()

#Bookings is {customerName:"", customerEmail: "", customerPhone: "", Slot: ""}

dict = {}

def analytics():
    global dict
    db.Exploration.delete_many({})
    db.Exploitation.delete_many({})
    for i in range(4): #Finding for all slots
        for c in cursor:
            if c['Slot'] == i and c['customerEmail'] not in dict.keys():
                dict[c['CustomerEmail']] =1

            elif c['Slot'] == i and c['customerEmail'] in dict.keys():
                dict[c['CustomerEmail']] +=1

        tuples_list = sorted(dict.items(), key=lambda x: x[1], reverse=True)


        print 'Completed for slot ',i

        db.Exploitation.insert({'Slot':i, 'customerEmail': tuples_list[0][0], 'customerName':db.Bookings.find_one({'customerEmail':tuples_list[0][0]})['customerName']})
        db.Exploration.insert({'Slot':i, 'customerEmail': tuples_list[len(tuples_list)-1][0], 'customerName':db.Bookings.find_one({'customerEmail':tuples_list[len(tuples_list)-1][0]})['customerName']})
    print 'All done'


    #Analytics is done at 2 am in the morning to calculate the results for targeted marketing.
    #Assumption is that it is highly improbable that the person eating in one time-slot will eat in another time-slot on the same day.
schedule.every().day.at("2:00").do(analytics)

while True:
   schedule.run_pending()
   time.sleep(1)
