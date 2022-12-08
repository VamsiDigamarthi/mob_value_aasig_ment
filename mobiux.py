import requests
import datetime as dt
import json

URL = "https://mobiux.in/assignment/sales-data.txt"
response_data = requests.get(URL)
main_datas = response_data.text.strip()


class MonthValues():
    
    def __init__(self, name):
        
        self.month_name = name
        self.month_total = 0
        self.articles = {}
        #print(self.articles)
        #print(self.month_total)
        #print(self.month_name)
    def articles_update(self, quantity, sku):
        if sku in self.articles:
            self.articles[sku].append(quantity)
        else:
            self.articles[sku] = list()
        
    def add_total(self, amount):
        self.month_total = int(self.month_total) + int(amount)
    

months = []
poin_month = []
articles = {}

for each in main_datas.split('\n')[1:]:
    Date,SKU,Unit_Price,Quantity,Total_Price = each.split(',')
    
    Date = dt.datetime.strptime(Date, "%Y-%m-%d").date()
    
    if str(Date.strftime('%b')) not in months:
        month_obj = MonthValues(str(Date.strftime('%b')))
        
        months.append(Date.strftime('%b'))
        
        poin_month.append(month_obj)

    month_obj.add_total(Total_Price)
    
    if SKU not in articles.keys():
        articles.update({ SKU : int(Unit_Price) })
    
    month_obj.articles_update(int(Quantity), SKU)


total = 0
month_wise = {}

for x in poin_month:
    total += x.month_total
    
    month_wise.update({ x.month_name : {"Month_total" : x.month_total }})
    
    
    most_sold_imt = 0
    most_revenue_name = ''
    
    
    quantity = 0
    most_sold_name = ''
    
    
    for each in x.articles.items():
        temp1,temp2 = each
        
        total_sold = int(sum(temp2))
        
        if total_sold > quantity:
            most_sold_name = temp1
            quantity = total_sold
            
        if total_sold*int(articles[temp1]) > most_sold_imt:
            most_revenue_name = temp1
            most_sold_imt = total_sold*int(articles[temp1])
            
    month_wise[x.month_name].update(
        {
            'Most_sold_name' : most_sold_name,
            'Most_sold_quantity' : quantity,
            'Most_sold_min' : min(x.articles.get(most_sold_name)),
            'Most_sold_max' : max(x.articles.get(most_sold_name)),
            'Most_sold_avg': sum(x.articles.get(most_sold_name))/len(x.articles.get(most_sold_name))
        }
        )
    month_wise[x.month_name].update(
        {
            'Most_revenue_name' : most_revenue_name,
            'Total_revenue' : most_sold_imt,
            'Percentage_amount' : str(round((most_sold_imt/x.month_total)*100,1)) + '%'
        }
        )

for key,value in month_wise.items():
    print(key,' : ',json.dumps(value, indent = 4))