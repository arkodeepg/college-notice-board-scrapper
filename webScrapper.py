import requests
from bs4 import BeautifulSoup
import csv
import smtplib
import credentials as cred


def newDates():                                     #this function is to get the current dates and the the notice correponding to the dates and attach it to the a dictionary
    r = requests.get("http://rcciit.org/updates/notice.aspx")
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    dateHtml = soup.find_all("span",{"class":"gridtagdate"})
    date = [dateHtml[i].text for i in range(len(dateHtml))]
    ipText = soup.find_all("div",{"class":"ipcontainer3"})
    tex = (ipText[0].find_all("td"))    #although we are using the indexing of 0 but there are is only one element this is because find all returns list
    tex = [tex[i].text.strip() for i in range(len(tex))]
    date = date[:3:]
    tex = tex[:3:]                       #as there will be only 3 notice in the notice board which is recent

    dic = {}
    for i in range(len(date)):
        dic[date[i]] = tex[i]

    return dic


def sendEmail(sub,body):
    EMAIL_ADDRESS = cred.EMAIL_ADDRESS()
    EMAIL_PASSWORD = cred.EMAIL_PASSWORD()
    SENDERS_EMAIL = cred.SENDERS_EMAIL()
    body = body[len(sub):]
    with smtplib.SMTP(cred.EMAIL_SMTP(),cred.SMTP_PORT()) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

        msg = f"Subject: {'RCCIIT NOTICE FOR '+sub}\n\n{body}"
        smtp.sendmail(EMAIL_ADDRESS,SENDERS_EMAIL,msg)
    with open("date.csv","a",newline = "") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([sub])



if __name__ == '__main__':
    dicto = (newDates())
    with open("date.csv") as readFile:  #importing data from the data.csv files
        reader = csv.reader(readFile,delimiter=',')
        checkDate = list(reader)
    readFile.close()
    checkDate = [i[0] for i in checkDate]   #removing elements from the nested list and moving them into the main list
    currentDate = list(dicto.keys())
    for i in currentDate:
        if i not in checkDate:
            sendEmail(i, dicto[i])
