import datetime # for date to day of week conversion, day arithmetic
import string   # for forming lists from csv
import operator # for object sorting

total = []  # will hold the sale object instances

class item:
    def __init__(self,name,date,time,buyer,recipient,price,com,dist,net):
        """ all data is stored as stings"""
        
        self.name = name
        self.date = date #year-month-day (yyyy-mm-dd)
        self.time = time
        self.buyer = buyer
        self.recipient = recipient
        self.price = price
        self.comission = com
        self.distribution = dist
        self.netincome = net

def oldsales(filename):
    """ Creates sale objects from old format"""
    
    filename.readline()     # This is to skip the first line of the file
    for line in filename:   # Here we are going to go through line
        csvlist = string.split(line[:-1],',') # excluding the new line character at the end
        # Date, Sale_ID, Vendor, Region, X, Y, Z, Item, Buyer, Delivered_To, SLL_Amount, SLL_Commission
        name = csvlist[7][1:-1]      # excluding the quotations
        date = csvlist[0][0:10]
        time = csvlist[0][11:19]
        buyer = csvlist[8][1:-1]     # excluding the quotations
        recipient = csvlist[9][1:-1] # excluding the quotations
        price = csvlist[10]          # this is also a fixed value which is 50, there can be failed sales
        com = csvlist[11]
        dist = '0'                   # no distribution value
        if price !='0': net = '47'   # fixed net income for all old sales, 'if' is for failed sales
        else: net = '0'
        global total
        total.append(item(name,date,time,buyer,recipient,price,com,dist,net))

def newsales(filename):
    """ Creates sale objects from new format"""
    
    filename.readline()     # This is to skip the first line of the file
    for line in filename:   # Here we are going to read everyline
        csvlist = string.split(line[:-1],',') # excluding the new line character at the end
        # Date,Order #,SKU,Item,Order Item ID,Buyer,Recipient,Price,State,Commission,Distributions,Net amount
        name = csvlist[3][1:-1]      # excluding the quotations
        date = csvlist[0][1:-1][0:10]  # first element of the list, exclude quotations, then selection
        time = csvlist[0][1:-1][11:19]
        buyer = csvlist[5][1:-1]       # excluding the quotations
        recipient = csvlist[6][1:-1]   # excluding the quotations
        price = csvlist[7]            
        com = csvlist[9]
        dist = csvlist[10]            
        net = csvlist[11]             
        global total
        total.append(item(name,date,time,buyer,recipient,price,com,dist,net))

file = open('/home/argand/Desktop/st/oldsales.txt','r')
oldsales(file)
file.close()

file = open('/home/argand/Desktop/st/sales.txt','r')
newsales(file)
file.close()
#################################################
##    Those are the statistical functions      ## 
#################################################
#
# we start by sorting the 'total' list according to date and time
total = sorted(total, key = operator.attrgetter('date','time')) 

def profit():
    """ total net income"""
    
    sum = 0
    for item in total:
        sum += int(item.netincome)
    return sum

def shared():
    """total shared monet""" 
    sum = 0
    for item in total:
        sum += int(item.distribution)
    return sum

def weekday(date):
    """this function returns the day of the week, starting from 0 to 6, from \
    monday"""
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    return datetime.date(year,month,day).weekday()
        
def weekdaydist():
    """returns the list of daily distribution of total sales (starts with \
    monday)"""
    distribution = [0,0,0,0,0,0,0]
    for item in total:
        dr = weekday(item.date)  # number of the day
        distribution[dr] += 1
    relative = []
    for nom in distribution:
        value = float(nom)/len(total)*100
        relative.append('%.2f' % value)
    return distribution, relative

def date2obj(date):
    """Takes the date attribute of the item and creates a date object from it"""
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    return datetime.date(year,month,day)
def obj2date(date):
    """takes the date object and returns a date string in format yyyy-mm-dd"""
    year = str(date.year)
    if date.month < 10: month = '0{0}'.format(date.month)
    else: month = str(date.month)
    if date.day < 10: day = '0{0}'.format(date.day)
    else: day = str(date.day)
    return '{0}-{1}-{2}'.format(year,month,day)
    
def histogram():
    """returns the histogram of total sales"""
    inventory = {}
    for item in total:
        inventory[item.name] = inventory.get(item.name,0) + 1
    return inventory

def dailysales():
    """Gives the total number of sales per day as a dictionary"""
    first = date2obj(total[0].date)
    last = date2obj(total[-1].date)
    daycount = (last - first).days + 1 #total days including the last and first
    increment = datetime.timedelta(days=1) # to count from first to the last day
    days = {}
    for i in range(daycount):
        now = first + increment * i
        nowstr = obj2date(now)
        days[nowstr] = 0
    for item in total:   
        days[item.date] = days.get(item.date,0) +1
    return days

def gifts():
    """ Calculates the number items sold as gift"""
    gift = 0
    for item in total:
        if item.buyer.lower() != item.recipient.lower():
            gift += 1
    percentage = '%.2f percent' %(float(gift)/len(total)*100)
    return gift, percentage

def plotter():
    """returns  3 lists, the date list, sale list, and average list in \
    chronological order"""
    hist = dailysales()
    days = sorted(hist) # chronologically sorted dates
    sales = []          # sales for each day above
    for i in days:
        sales.append(hist[i])
    aver = []           # total daily average, till that day
    for i in range(1,len(days)+1):
        value = sum(sales[:i])/float(i) # total average value of that day 
        aver.append(value)
    return days, sales, aver   
