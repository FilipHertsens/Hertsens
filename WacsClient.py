import requests
import json
import time
import arrow
from pathlib import Path
from pprint import pprint
IdEigenvloot = [15, 8, 67, 68, 2, 3, 4, 5, 6, 104]
apikey = 'Bg8mf4V59bcSGlb+WftHuQ=='
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
pathvoertuigen = os.path.join(THIS_FOLDER, 'data/voertuigen.json')
opvolgdata = {5: 'KOH', 6: 'GOH', 90: 'TACHO', 91: 'TC', 240: 'GOH', 241: 'KOH', 252: '500-OH', 253: '1000-OH',
              254: '2000-OH'}

def GetAllAssetsDetails():
    Details = []
    bases = GetAllAssetsBase()
    for base in bases:
        if base['Active'] and base['OwnerID'] in IdEigenvloot:
            asset = GetAssetDetails(base['AssetID'])
            Details.append(asset)
    return Details

def SaveAssetDetails(voertuigen):
    try:
        with open(pathvoertuigen, 'w') as outfile:
            json.dump(voertuigen, outfile, indent=4)
        return True
    except:
        return False





def GetAllAssetsBase():
    response = requests.get(
        'https://api.wacs.online/api/v1/Assets/GetAll',
        params={'key': apikey},
    )
    if response.status_code == 200:
        json_response = response.json()
        return json_response


def GetAllTodo():
    response = requests.get(
        'https://api.wacs.online/api/v1/Todo/GetAllTodos',
        params={'key': apikey},
    )
    if response.status_code == 200:
        json_response = response.json()
        with open('/home/pi/DB/opentodo.json', 'w') as outfile:
            json.dump(json_response, outfile)
        return {"response" :"all todo's ontvangen", "code": response.status_code}
    else:
        return {"response" :"Request for all todo's mislukt", "code": response.status_code}



def GetPlanorders():
    response = requests.get(
        'https://api.wacs.online/api/v1/Planning/GetOrders',
        params={'key': apikey},
    )
    if response.status_code == 200:
        json_response = response.json()
        with open('/home/pi/DB/planorders.json', 'w') as outfile:
            json.dump(json_response, outfile)
        return {"response" :"alle planorders ontvangen", "code": response.status_code}
    else:
        return {"response" :"Request for alle planorders mislukt", "code": response.status_code}


def GetKeuringdata():
    response = requests.get(
        'https://api.wacs.online/api/v1/Todo/GetUpcomingVehicleDates',
        params={'key': apikey},
    )
    if response.status_code == 200:
        json_response = response.json()
        with open('/home/pi/DB/keuringdata.json', 'w') as outfile:
            json.dump(json_response, outfile)
        return {"response" :"keuringsdata ontvangen ontvangen", "code": response.status_code}
    else:
        return {"response" :"Request for keuringsdata mislukt", "code": response.status_code}

def GetAllTechniekers():
    response = requests.get(
        'https://api.wacs.online/api/v1/Employees/All',
        params={'key': apikey},
    )
    if response.status_code == 200:
        json_response = response.json()
        with open('/home/pi/DB/techniekers.json', 'w') as outfile:
            json.dump(json_response, outfile)
        return {"response" :"techniekers ontvangen ontvangen", "code": response.status_code}
    else:
        return {"response" :"Request for all techniekers mislukt", "code": response.status_code}


def GetAllorders():
    response = requests.get(
        'https://api.wacs.online/api/v1/OrdersWASP/GetAllOrders',
        params={'key': apikey},
    )
    if response.status_code == 200:
        json_response = response.json()
        with open('/home/pi/DB/orders.json', 'w') as outfile:
            json.dump(json_response, outfile)
        return {"response" : "orders ontvangen ontvangen", "code": response.status_code}
    else:
        return {"response" :"Request for all orders mislukt", "code": response.status_code}

def GetAssetmodified(x):
    response = requests.get(
        'https://api.wacs.online/api/v1/Assets/GetAllLastModified',
        params={'key': apikey, 'seconds': x},
    )
    if response.status_code == 200:
        json_response = response.json()

        return json_response
    else:
        return {"response" :"Request for all modified assets mislukt", "code": response.status_code}

def GetAssetDetails(x):
    response = requests.get(
        'https://api.wacs.online/api/v1/Assets/GetByID',
        params={'key': apikey, 'id': x},
    )

    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
        return False



def ChangeAssetBase(AssetId,data):
    '''
                vb van data parameter

                + 3x ' voor en na data

                 <Code>sample string 2</Code>
                  <ExternalId>sample string 6</ExternalId>
                  <Header1>sample string 3</Header1>
                  <Header2>sample string 4</Header2>
                  <Header3>sample string 5</Header3>
                  <Name>sample string 1</Name>
                  <OwnerId>1</OwnerId>
    '''

    xml = '''<AssetUpdateByIdDTO xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.datacontract.org/2004/07/WACS_API.Models.DTO.API.IN">
        %s
        </AssetUpdateByIdDTO>
        ''' %data
    response = requests.put(
        'https://api.wacs.online/api/v1/Assets/UpdateByID',
        params={'key': apikey, 'id': AssetId},
        data=xml,
        headers={'Content-Type': 'application/xml'}
        ).text
    print(response)

    try:
        true = True
        p = eval(response)
    except:
        return {"response" : response, "code": 'error'}

    try:
        if p['AssetID'] == AssetId:
            return {"response" :"Request update by id is gelukt", "code": 200}
        else:
            return {"response": response, "code": 'error'}
    except:
        return {"response": response, "code": 'error'}


def AddTodo(data):
    ''' voorbeeld van data

    + 3x ' voor en na data

          <AssetRegistrationNumber>H019</AssetRegistrationNumber>
          <DateNotified>2020-08-19T09:26:59.7157781+02:00</DateNotified>
          <DateOfExecution>2020-08-19T09:26:59.7157781+02:00</DateOfExecution>
          <ExternalID>4557524</ExternalID>
          <ExtraInformation>sample string 55</ExtraInformation>
          <Mileage>6545</Mileage>
          <PlanningsCode>AC</PlanningsCode>
    '''

    xml = """<TodoInDTO xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.datacontract.org/2004/07/WACS_API.Models.DTO.API.IN">
      %s
    </TodoInDTO>""" %data
    response = requests.post(
        'https://api.wacs.online/api/v1/Todo/InsertTodo',
        params={'key': apikey},
        data=xml,
        headers={'Content-Type': 'application/xml'}
        ).text

    if response == '':
        return {"response" :"Request add todo is gelukt", "code": 200}

    else:
        return {"response": response, "code": 'error'}
data = '''<AssetRegistrationNumber>D003</AssetRegistrationNumber>
          <DateNotified>2020-08-27T18:40:44.180857+02:00</DateNotified>
          <DateOfExecution>2020-08-27T18:40:44.180857+02:00</DateOfExecution>
          <ExternalID>1598546449</ExternalID>
          <ExtraInformation>Tele: test</ExtraInformation>
          <Mileage>50415</Mileage>
          <PlanningsCode>DEFAULT</PlanningsCode>'''




def FinishTodo(todoid):
    response = requests.post(
        'https://api.wacs.online/api/v1/Todo/FinishExternalTodo',
        params={'key': apikey, 'externalID': todoid})

    if response.status_code > 199 < 300:
        return {"response": "Request add todo is gelukt", "code": response.status_code}

    else:
        return {"response": response, "code": 'error'}


def UpdateKmById(AssetId,Km):
    response = requests.post(
        'https://api.wacs.online/api/v1/Assets/UpdateMileageById',
        params={'key': apikey, 'id': AssetId, 'mileage': Km})
    print(response)

    if response.status_code > 199 < 300:
        return {"response": "Request update km is gelukt", "code": response.status_code}

    else:
        return {"response": response, "code": 'error'}
    
    
def CheckCode(code,nummerplaat):
    y = True
    with open ('/home/pi/DB/assetsbase.json') as outfile:
        data = json.load(outfile)
    for x in data:
        if x['Active']:
            asset = x['Name'].lower()
            if code.lower() == asset:
                return [True,x['Name'],asset.upper(),x]
            else:
                if ' ' in asset:
                    asset = asset.split(" ")[0]
                if '_' in asset:
                    asset = asset.split("_")[-1]
                if asset == code.lower():
                    y = False
                    return [True,x['Name'],asset.upper(),x]
            if nummerplaat.upper() == x['Header1']:
                y = False
                return [True,x['Name'],asset.upper(),x]
    if y:
        return [False,False,False]


def GetAllTodoById(y):
    GetAllTodo()
    time.sleep(0.5)
    lijst = []
    with open ('/home/pi/DB/opentodo.json') as outfile:
        data = json.load(outfile)
        
        for x in data:
            asset = x['NumberPlate'].lower()

            if ' ' in asset:
                asset = asset.split(" ")[0]
            if '_' in asset:
                asset = asset.split("_")[-1]
                
            if asset == y.lower():
                if x['Automated'] == False:
                    lijst.append(x)
                
        return lijst
            

def ChangeID():
    with open ('/home/pi/DB/assetsbase.json') as outfile:
        data = json.load(outfile)
    for x in data:
        if x['Active']:

            None
            
        else:
            if x['Name'][0:2].lower() != 'ex':
                print(x)
                p = 'ex'+x['Name']
                AssetId = x['AssetID']
                
                data = '''<Name>%s</Name>
                        '''%(p)
                ChangeAssetBase(AssetId,data)
            
def getidbyname(name):
    GetAllAssetsBase()
    with open('/home/pi/DB/assetsbase.json') as json_file:
        voertuigen = json.load(json_file)
        
    for voertuig in voertuigen:
        nr = voertuig['Name'].lower()
        if voertuig['Name'].lower()[0] == '_':
            nr = voertuig['Name'].lower()[1:]
        if ' ' in voertuig['Name'].lower():
            nr = voertuig['Name'].lower().split(' ')[0]
        if voertuig['Active'] == True:
            if nr == name.lower():
                return voertuig['AssetID']
    return False
        
def getinfobyname(name):
    x = GetAssetDetails(getidbyname(name))
    fields = {}
    key = ''
    value = ''
    q = x['response']
    for t,l in q.items():
        if t == 'Fields':
            x = x['response']['Fields']
        else:
            key = str(t)
            value = str(l)
            fields[key] = value

    for f in x:
        for n, m in f.items():
            if n == 'Name':
                key = str(m)
            elif 'Value' in n and m != None:
                if n == 'DateValue':
                    t = arrow.get(m)
                    value = t.format('DD/MM/YYYY')
                else:
                    if str(m) == '':
                        m = '*'
                    value = str(m)
        fields[key] = value
    return fields

def GetAssettodos(x):
    global opvolgdata
    respon = []
    x = getidbyname(x)
    response = requests.get(
        'https://api.wacs.online/api/v1/Todo/GetUpcomingVehicleDates',
        params={'key': apikey})
    if response.status_code == 200 and x != False:
        json_response = response.json()
        for y in json_response:
            if y['AssetID'] == x:
                if y['PlanningscodeID'] in opvolgdata:
                    if y['PlanningscodeID'] in [252,253,254]:
                        respon.append(opvolgdata[y['PlanningscodeID']]+' last: '+str(y['LastMileage'])+' next: '+str(y['NextMileage']))
                    else:                      
                        respon.append(opvolgdata[y['PlanningscodeID']]+' last: '+cleandate(y['LastDate'])+' next: '+cleandate(y['NextDate']))
        return respon
    else:
        return False
  
  
def cleandate(x):
    time = arrow.get(x)
    cleantime = time.format('DD/MM/YYYY')
    return cleantime

def GetListtoelatingen():
    toelatingen = {}
    toelating = {}
    toelatingID = ''
    response = requests.get(
        'https://api.wacs.online/api/v1/Contacts/GetAllWithDetails',
        params={'key': apikey})
    json_response = response.json()
    for t in json_response:
        fs = t['Fields']
        for f in fs:
            if 'Telegram toelating' in f['Name']:
                toelating[f['Name'].split('|')[0]] = f['BooleanValue']
            if 'Telegram ID' in f['Name']:
                toelatingID = int(f['DecimalValue'])

        if toelatingID != '':
            toelatingen[toelatingID] = toelating
        toelating = {}
        toelatingID = ''
    if response.status_code > 199 < 300:
        return toelatingen
    else:
        return {"response": response, "code": 'error'}

def GetListVoertuigen():
    with open(pathvoertuigen, 'r') as json_file:
        data = json.load(json_file)
    return data


def update_list_voertuigen(sec):
    voertuigen = GetListVoertuigen()
    changes = GetAssetmodified(sec)
    ltchange = []
    for change in changes:
        ltchange.append(change['AssetID'])
    if not len(ltchange) == 0:
        res = [i for i in voertuigen if not (i['AssetID'] in ltchange)]

        for idd in ltchange:
            voertuig = GetAssetDetails(idd)
            if voertuig['Active'] and voertuig['OwnerID'] in IdEigenvloot:
                res.append(voertuig)
        SaveAssetDetails(res)
    print('[UPDATE VOERTUIGEN LIJST]')