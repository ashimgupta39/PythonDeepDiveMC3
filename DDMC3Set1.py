import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("api_key")
url = 'https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales?offset=1&limit=30'
allrecords=[]
headers = {
    'accept':'accept: application/json',
    'access_token': api_key
}
for offset in range(0,500,100):
    params={
        'offset':offset,
        'limit':100
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        data = response.json()
        allrecords.extend(data['data'])


# In[5]:


import pandas as pd
dd = pd.json_normalize(allrecords)
import datetime as dt


dd['order_purchase_date'] = pd.to_datetime(dd['order.order_purchase_date'],format='%Y-%m-%d')

data_datetime=pd.to_datetime(dd['order.order_purchase_date'])


dd['day_of_week']= data_datetime.dt.strftime('%A')
dd['no_of_sizes']=dd['product.sizes'].str.split(',').apply(len)


maxx=max(dd['no_of_sizes'])


dd[dd['no_of_sizes']==maxx]['product.product_name']




dd[dd['product.product_name']=='Mitel 5320 IP Phone VoIP phone']['no_of_sizes']


dd['Month']= data_datetime.dt.strftime('%B')


# In[25]:


fn = lambda Metric: dd.groupby('Month')[Metric].sum()


# In[26]:


fn('sales_amt')


# In[28]:


dd['profit'] = dd['profit_amt'].replace('null',None)


# In[29]:


fn('profit')


# In[31]:


dd['profit_margin'] = (dd['profit']/dd['profit'].sum())*100


# In[38]:


profit_margins_month_wise=fn('profit_margin')


# In[39]:


profit_margins_month_wise[profit_margins_month_wise>20]


# In[40]:


dd.columns


# In[43]:


replaceNull = lambda x: x.replace('null',None)


# In[44]:


dd['order_delivered_customer_date'] = pd.to_datetime(replaceNull(dd['order.order_delivered_customer_date']))


# In[46]:


dd['order_estimated_delivery_date'] = pd.to_datetime(replaceNull(dd['order.order_estimated_delivery_date']))


# In[47]:


dd['isDelay'] = dd['order_delivered_customer_date']>dd['order_estimated_delivery_date']


# In[49]:


dd['isDelay']=dd['isDelay'].astype(int)


# In[50]:


dd['isDelay'].value_counts()


# In[52]:


dd.groupby('order.vendor.VendorID')['isDelay'].sum()


# In[61]:


dd.drop_duplicates(subset='order.customer.customer_id', inplace=True)


# In[62]:


first_name = [name.split()[0] for name in dd['order.customer.customer_name']]


# In[63]:


Alans = [name for name in first_name if name=='Alan']


# In[64]:


len(Alans)


# In[65]:


Alans


# In[ ]:




