import requests
import datetime as dt
import json

URL = "https://mobiux.in/assignment/sales-data.txt"
response_data = requests.get(URL)
main_data = response_data.text.strip()
#######################################################################################################################
class MonthData():
    
    def __init__(self, name):
        
        self.month_name = name
        self.month_total = 0
        self.articles = {}
        
    def articles_update(self, quantity, sku):
        if sku in self.articles:
            self.articles[sku].append(quantity)
        else:
            self.articles[sku] = list()
        
    def add_total(self, amount):
        self.month_total = int(self.month_total) + int(amount)
    

#   %Y-%m-%d
#######################################################################################################################
months = []
pointers_month = []
#main_list = []
articles = {}


for each in main_data.split('\n')[1:]:
    Date,SKU,Unit_Price,Quantity,Total_Price = each.split(',')
    
    Date = dt.datetime.strptime(Date, "%Y-%m-%d").date() #2019-02-20
    
    if str(Date.strftime('%b')) not in months:
        month_obj = MonthData(str(Date.strftime('%b')))
        months.append(Date.strftime('%b'))
        
        pointers_month.append(month_obj)

    month_obj.add_total(Total_Price)
    
    if SKU not in articles.keys():
        articles.update({ SKU : int(Unit_Price) })
    
    month_obj.articles_update(int(Quantity), SKU)

#    main_list.append({
#        'Date' : Date,
#        'SKU' : SKU,
#        'Unit_Price' : Unit_Price,
#        'Quantity' : Quantity,
#        'Total_Price' : Total_Price.strip()
#    })
#######################################################################################################################
TOTAL_SALES = 0
month_wise = {}

for x in pointers_month:
    TOTAL_SALES += x.month_total
    
    month_wise.update({ x.month_name : {"Month Total" : x.month_total }})
    
    #Most revenue
    most_sold_amt = 0
    most_revenue_name = ''
    
    #Most Popular
    quantity = 0
    most_sold_name = ''
    
    
    for each in x.articles.items():
        temp1,temp2 = each
        
        total_sold = int(sum(temp2))
        
        if total_sold > quantity:
            most_sold_name = temp1
            quantity = total_sold
            
        if total_sold*int(articles[temp1]) > most_sold_amt:
            most_revenue_name = temp1
            most_sold_amt = total_sold*int(articles[temp1])
            
    month_wise[x.month_name].update(
        {
            'Most Sold Name' : most_sold_name,
            'Most Sold Quantity' : quantity,
            'Most Sold Min' : min(x.articles.get(most_sold_name)),
            'Most Sold Max' : max(x.articles.get(most_sold_name)),
            'Most Sold Avg': sum(x.articles.get(most_sold_name))/len(x.articles.get(most_sold_name))
        }
        )
    month_wise[x.month_name].update(
        {
            'Most Revenue Name' : most_revenue_name,
            'Total_Revenue' : most_sold_amt,
            'Percentage Amount' : str(round((most_sold_amt/x.month_total)*100,1)) + '%'
        }
        )

for key,value in month_wise.items():
    print(key,' : ',json.dumps(value, indent = 4))
    
    
print('\n\n',json.dumps(articles, indent = 4))
