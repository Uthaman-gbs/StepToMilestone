from pandas import DataFrame
import datetime
import flask
import pickle
from flask import Flask,render_template,request
#creating instance for class
app=Flask(__name__)
# to tell flask what url should trigger the function index()
@app.route('/')
@app.route('/Home/')
def index():
     return flask.render_template('Home.html')
def ValuePredictor(ibk,iwd,imd,ihr):
    bankCode=DataFrame({'bankcode':['ABDIEGAC','ABDIEGOBAC','ABPTPKTT','ALEXEGCASH','ALFHPKFLIBFT','BARCUKTT','BARTINFLASH','BCEYLKFLASH','BKNZNZTT','BNINIDFLASH','BNINIDFLIBFT','BNOFPHFLASH','BNORPHOBAC','BOPIPHAC','BOPIPHFLASH','BOPIPHFLOBAC','BOPIPHOBAC','BRIFIDFLASH','BSAFLKFLASH','BSATLKOBTT','BSATLKTTR','CAABJOAMMJOD','CBAUAEABUDHA','CBITINFLASH','CCEFLKFLASH','CENAIDAC','CENAIDFLASH','CENAIDOBAC','CNRTINFLASH','FLIFINFLASH','GLBBNPCASH','GLBBNPFLASH','GLBBNPFLCASH','GLBBNPOBAC','GLBBNPTT','HBLILKTTR','HDFCINFLASH','HDFCINFLIMPS','HDFCINNEFT','HDFCINRTGS','HDFCINTT','HIMANPOBAC','HIMANPTT','HIMFNPFLASH','IBBTBDFLASH','IBBTBDFLOBAC','ICIFINFLASH','IDIFINFLASH','IOBFINFLASH','MBTCPHTT','MBTFPHFLASH','MBTFPHFLCASH','MTBTBDBEFTN','MTBTBDFBEFTN','MTBTBDFLASH','MUCBPKFLASH','NATAAUTTAUD','NBEGEGFLASH','NSBTLKTTD','NSBTLKTTR','NTBTLKTTD','NTBTLKTTR','PNBPPHRRAC','PSBKLKFLASH','PUNTINFLASH','PUNTINTT','RATNINFLIMPS','RATNINNEFT','RCBCPHFLASH','RCBCPHFLIBFT','RCBCPHOBAC','SBIFINFLASH','SBININTT','SEYFLKFLASH','SOIFINFLASH','UBIFINFLASH','UNIFPKFLASH','UNIFPKIBFT','UNILPKTT','UTIFINFLASH','YESRINFLASH','YESRINFLIMPS','YESRINTT'],
                    'bankname':['NA','NA','ALLIED BANK LIMITED - TT','BANK OF ALEXANDRIA SAE - TT','BANK ALFALAH LIMITED - Flash','BARCLAYS BANK PLC - TT','BANK OF BARODA - Flash','BANK OF CEYLON - Flash','BANK OF NEW ZEALAND - TT','NA','BANK NEGARA INDONESIA - Flash','NA','BANCO DE ORO UNIVERSAL BANK - TT','BANK OF PHILIPPINES ISLANDS - TT','BANK OF PHILIPPINES ISLANDS - Flash','NA','NA','NA','NA','NA','SAMPATH BANK - TT','CAIRO AMMAN BANK - TT','CENTRAL BANK OF UAE - TT','CENTRAL BANK OF INDIA - Flash','NA','BANK CENTRAL ASIA - TT','BANK CENTRAL ASIA - Flash','NA','CANARA BANK - Flash','NA','NA','NA','GLOBAL IME BANK LTD - Flash','GLOBAL IME BANK LTD - TT','NA','HATTON NATIONAL BANK LTD - TT','NA','HDFC BANK - Flash','HDFC BANK - TT','NA','NA','NA','HIMALAYAN BANK - TT','NA','NA','NA','NA','NA','NA','METROPOLITAN BANK AND TRUST CO - TT','NA','NA','NA','NA','NA','MCB BANK LIMITED - Flash','NATIONAL AUSTRALIA BANK - TT','NATIONAL BANK OF EGYPT (AL AHLI BANK) - Flash','NA','NATIONAL SAVINGS BANK - TT','NA','NATIONS TRUST BANK - TT','PHILIPPINE NATIONAL BANK - TT','PEOPLES BANK - Flash','PUNJAB NATIONAL BANK - Flash','PUNJAB NATIONAL BANK - TT','RBL BANK LTD - Flash','RBL BANK LTD - TT','NA','RIZAL COMMERCIAL BANKING CORPORATION - Flash','RIZAL COMMERCIAL BANKING CORPORATION - TT','NA','STATE BANK OF INDIA - TT','NA','NA','NA','UNITED BANK LTD - Flash','UNITED BANK LTD - TT','UNITED BANK LTD - TT','NA','NA','YES BANK LTD - Flash','YES BANK LTD - TT']})
    #payOutCode=DataFrame({'PayoutCcyCode':['AED','AUD','BDT','EGP','EUR','GBP','IDR','INR','JOD','LKR','NPR','NZD','PHP','PKR','USD']})
    wkDayCode=DataFrame({'weekday':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']})
    mode=DataFrame({'mode':['TT','Flash']})
    
    iwd=iwd.split('-')
    dayofweek = datetime.date(int(iwd[0]),int(iwd[1]),int(iwd[2])).strftime("%A")
    
    pbk=bankCode[bankCode['bankname']==ibk].index[0]
    #ppc=payOutCode[payOutCode['PayoutCcyCode']==ipc].index[0]
    pwd=wkDayCode[wkDayCode['weekday']==dayofweek].index[0]
    pmd=mode[mode['mode']==imd].index[0]
    phr=ihr
    #result=[[pwd,pmd,phr,ppc,pbk]]
    to_predict=[[pwd,pmd,phr,pbk]]
    loaded_model=pickle.load(open('model.pkl','rb'))
    result=int(loaded_model.predict(to_predict))
    if result==1:
        result='Expected to credit within TAT'
    else:
        result='Expect a delay in credit'
    return result

@app.route('/result/',methods=['POST'])
def result():
    if request.method=='POST':
        ibk = request.values['bankName']
        #ipc = 'INR' #request.values['ccyName']
        iwd = request.values['wkday']
        imd = request.values['tType']
        ihr = 16
        result=ValuePredictor(ibk,iwd,imd,ihr)
        return render_template('Result.html',prediction=result)
    
if __name__=='__main__':
    app.run()    
