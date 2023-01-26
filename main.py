import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

finalProductData = []
alphabate=["j", "q"]
# , "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x","y","z","#",

storeUrl = "https://pharmeasy.in"
payload = {}
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cookie': 'HAB_Var=Apothecary; HAB_XDI=Apothecary; _cg=4000'
}

# def productFinder(jURL):
#     ''' This function will get the URL of
#         every products and process the data 
#         and get the data of fields and 
#         append that data in the finalProductData'''
#     try:
#         r1 = requests.get(jURL)
#         htmlContent1 = r1.text
#         soup = BeautifulSoup(htmlContent1, 'html.parser')
#         clsData = soup.find(name='h1', class_='MedicineOverviewSection_medicineName__dHDQi')
#         clsDataP = soup.find(name='div', class_='PriceInfo_ourPrice__jFYXr')
#         clsDataD = soup.find(name='p', class_='MedicalDescription_readMoreTarget__XSPzK')
#         byname = soup.find(name='div', class_='MedicineOverviewSection_brandName__rJFzE')
#         mUnit = soup.find(name="div", class_="MedicineOverviewSection_measurementUnit__7m5C3")
#         namedata = str(clsData.text)
#         finalProductData.append({"name": namedata, "price": str(clsDataP.text), "Description": str(clsDataD), "BYName": str(byname.text), "measurementUnit": str(mUnit.text)})
#     except Exception as e:
#         print(e)
#         print(jURL)


def productFinder(jURL):
    ''' This function will get the URL of
        every products and process the data 
        and get the data of fields and 
        append that data in the finalProductData'''
    try:
        r1 = requests.get(jURL)
        htmlContent1 = r1.text
        soup = BeautifulSoup(htmlContent1, 'html.parser')
        clsData = soup.find(
            name='h1', class_='MedicineOverviewSection_medicineName__dHDQi')
        summeryheaders = soup.findAll(
            name='td', class_='DescriptionTable_field__l5jJ3')
        summeryheadersvalues = soup.findAll(
            name='td', class_='DescriptionTable_value__0GUMC')
        clsDataP = soup.find(name='div', class_='PriceInfo_ourPrice__jFYXr')
        clsDataD = soup.find(
            name='p', class_='MedicalDescription_readMoreTarget__XSPzK')
        byname = soup.find(
            name='div', class_='MedicineOverviewSection_brandName__rJFzE')
        mUnit = soup.find(
            name="div", class_="MedicineOverviewSection_measurementUnit__7m5C3")
        namedata = str(clsData.text)
        summery = []
        summeryValues = []
        for data in summeryheaders:
          summery.append(data.text)
        for value in summeryheadersvalues:
          summeryValues.append(value.text)
        data = dict(zip(summery, summeryValues))
        finalProductData.append({"name": namedata, "price": str(clsDataP.text), "Description": str(clsDataD), "BYName": str(byname.text), "measurementUnit": str(mUnit.text), "Contains": str(data.get("Contains", "none")), "Uses": str(data.get("Uses", "none")), "Side effects": str(data.get("Side effects", "none")), "Therapy": str(data.get("Therapy", "none"))})
    except Exception as e:
        print(e)
        print(jURL)




def pages(hcData):
    htmlContent = hcData
    soup = BeautifulSoup(htmlContent, 'html.parser')
    cls = soup.findAll(class_="BrowseList_medicine__cQZkc")
    # product name and their URL Data holder
    productURLholder = []
    for link in cls:
        productURLholder.append({"name": link.text, "link": link.get('href')})
    # Product Link url pass to the productFinder
    for proURL in productURLholder:
        productFinder(storeUrl+proURL["link"])

# loop for the alphabate section
for value in alphabate:
    pageUrlwithAlphabate = []
    num=0
    datamod=["Data"]
    while datamod!=[]:
        url = f"https://pharmeasy.in/online-medicine-order/browse?alphabet={value}&page={num}"
        response = requests.request("GET", url, headers=headers, data=payload)
        htmlContent = response.text
        soup = BeautifulSoup(htmlContent, 'html.parser')
        cls = soup.find(id="__NEXT_DATA__")
        mod = cls.text
        data = json.loads(mod)
        datamod = data['props']['pageProps']['areaList']
        pageUrlwithAlphabate.append({"alphabet": value, "link": url})
        num += 1
    print("here",len(pageUrlwithAlphabate))
    pageUrlwithAlphabate.pop()
    print(pageUrlwithAlphabate)
    for pageLinks in pageUrlwithAlphabate:
        url = pageLinks['link']
        response = requests.request("GET", url, headers=headers, data=payload)
        pages(response.text)

print(len(finalProductData))
print(finalProductData)
df = pd.DataFrame(finalProductData)
print(df)
df.to_csv('dsfata.csv', index=False, columns=['name', 'price', 'Description', 'BYName', "measurementUnit", "Contains", "Uses", "Side effects", "Therapy"])