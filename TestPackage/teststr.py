__author__ = 'PC-B1301'

strr = "get BoyChaiwat 110 [24/Sep/2015:13:22:54 +0700] 2 1 - 192.168.1.38 IT55-32 - Google Docs A4 one-sid"
jid = 111
check = "get-" + str(jid)+ " xxxxxxxxxxxxxx"
print(strr)
stdid = 55130500013

def cutcredit(stdid, jobfrom, jobid):
    print(strr.find("+0700]"))
    print(strr[strr.find("+0700]")+7:strr.find("+0700]")+8])
    print(strr[strr.find("+0700]")+9:strr.find("+0700]")+10])
    print(int(strr[strr.find("+0700]")+7:strr.find("+0700]")+8])*int(strr[strr.find("+0700]")+9:strr.find("+0700]")+10]))
    print(check.find("get-110"))
cutcredit(55130500013, "BoyChaiwat", 110)