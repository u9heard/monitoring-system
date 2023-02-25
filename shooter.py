import requests
import random
import schedule, time

names = [15, 16,17,18]

def round_custom(num, step):
    return round(num / step) * step

def send(name):
    head = {'Content-type': 'application/json'}
    param = {"id":str(name),"temp":str(round(random.normalvariate(100.2, 0.05), 1)), 
             "hum":str(round_custom(random.normalvariate(70, 1), 1))}
    
    resp = requests.post('http://192.168.0.110/api/add', headers=head,
                          json=param)
    print(resp.text)
    print(param)

def sendNames(names):
    
    for n in names:
        send(n)

schedule.every(1).minutes.do(sendNames, names)

if __name__ == "__main__":
    while 1:
        schedule.run_pending()
        time.sleep(1)

