#!/usr/bin/env python3
"""
Database initialization script
Clears all collections and creates a test user with sample transaction data
"""

import sys
import os
from datetime import datetime, date
from passlib.context import CryptContext

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.firebase_client import db
from data.user_dao import create_user
from data.transaction_dao import batch_create
from models.transaction import TransactionIn

# Password context for hashing
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test user credentials
TEST_USER_NAME = "Test User"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "password123"

# Sample transaction data from the user
SAMPLE_TRANSACTIONS = [
    {"date": "31/05/25", "narration": "UPI-R INDVENTURES PVT LT-PIDGE70.RZP@ICICI-ICIC0DC0099-551717127904-PAYMENTTOPIDGE", "withdrawn": 167, "deposit": 0, "closing_balance": 38738.48},
    {"date": "1/6/2025", "narration": "UPI-RAJESH TULSIDAS JESW-PAYTMQR5CGJOT@PTYS-YESB0PTMUPI-105736147910-CHAAT", "withdrawn": 50, "deposit": 0, "closing_balance": 38688.48},
    {"date": "1/6/2025", "narration": "UPI-SUSHIL KUMAR S-8088688428-2@YBL-YESB0001245-105761474661-UPI", "withdrawn": 105, "deposit": 0, "closing_balance": 38583.48},
    {"date": "1/6/2025", "narration": "UPI-YOGENDRA R-YOGENDRA4159@OKHDFCBANK-HDFC0000075-105771601797-UPI", "withdrawn": 93, "deposit": 0, "closing_balance": 38490.48},
    {"date": "2/6/2025", "narration": ".DC INTL POS TXN MARKUP+ST 140525 140525-MIR2615216835038", "withdrawn": 62.5, "deposit": 0, "closing_balance": 38427.98},
    {"date": "2/6/2025", "narration": ".DC INTL POS TXN MARKUP+ST 150525 150525-MIR2615217123282", "withdrawn": 83.37, "deposit": 0, "closing_balance": 38344.61},
    {"date": "2/6/2025", "narration": "UPI-GROFERS INDIA PRIVAT-GROFERSINDIA.RZP@HDFCBANK-HDFC0MERUPI-105819375392-PAYVIARAZORPAY", "withdrawn": 217, "deposit": 0, "closing_balance": 38127.61},
    {"date": "3/6/2025", "narration": "ME DC SI 435584XXXXXX8558 WINDSURF", "withdrawn": 1515.23, "deposit": 0, "closing_balance": 36612.38},
    {"date": "3/6/2025", "narration": "UPI-SHANTHI WINES-0798072A0176622.BQR@KOTAK-KKBK0008072-105885207859-UPI", "withdrawn": 806, "deposit": 0, "closing_balance": 35806.38},
    {"date": "4/6/2025", "narration": "UPI-JUICE JUNCTION WIPRO-PAYTMQR1N6DWYKKZ6@PAYTM-YESB0PTMUPI-105921834868-UPI", "withdrawn": 185, "deposit": 0, "closing_balance": 35621.38},
    {"date": "6/6/2025", "narration": "UPI-SOWBHAGYA AND CO-PAYTM-46071647VDQM@PTYS-YESB0PTMUPI-106052370181-UPI", "withdrawn": 400, "deposit": 0, "closing_balance": 35221.38},
    {"date": "7/6/2025", "narration": "UPI-THARESH KUMAR DC-PAYTMQR5IBKOQ@PTYS-YESB0PTMUPI-106056760428-UPI", "withdrawn": 45, "deposit": 0, "closing_balance": 35176.38},
    {"date": "7/6/2025", "narration": "NEFT CR-YESB0000001-ZERODHA BROKING LTD-DSCNB A/C-SANCHIT VIKAS GUPTA-YESBN12025060706128783", "withdrawn": 0, "deposit": 6000, "closing_balance": 41176.38},
    {"date": "7/6/2025", "narration": "UPI-SELFSPIN MOBILITY PR-SELFSPINMOBILITYPRXZS.RAZORP@ICICI-ICIC0DC0099-515858313233-UPAID AMOUNT OF BO", "withdrawn": 111, "deposit": 0, "closing_balance": 41065.38},
    {"date": "7/6/2025", "narration": "UPI-ABDUL JALEEL K P-JALEELKP1986@OKHDFCBANK-KVBL0001170-106067184524-UPI", "withdrawn": 64, "deposit": 0, "closing_balance": 41001.38},
    {"date": "7/6/2025", "narration": "UPI-SOUMYA RANJAN JENA-9649655655@PTYES-IDFB0040101-686158334740-SENT FROM PAYTM", "withdrawn": 0, "deposit": 1125, "closing_balance": 42126.38},
    {"date": "7/6/2025", "narration": "UPI-SAMPATH KUMAR L M-99002807@IBL-HDFC0004118-106103332867-UPI", "withdrawn": 54, "deposit": 0, "closing_balance": 42072.38},
    {"date": "7/6/2025", "narration": "UPI-99 VARIETY DOSA   PA-GPAY-11258272613@OKBIZAXIS-UTIB0000553-106103561962-PAV BHAJI", "withdrawn": 250, "deposit": 0, "closing_balance": 41822.38},
    {"date": "7/6/2025", "narration": "UPI-99 VARIETY DOSA   PA-GPAY-11258272613@OKBIZAXIS-UTIB0000553-106104168147-PULAV", "withdrawn": 120, "deposit": 0, "closing_balance": 41702.38},
    {"date": "8/6/2025", "narration": "UPI-SHREYAS JAGADISH CHO-SHREYASHCHOULGE@OKICICI-BKID0000025-106126222847-UPI", "withdrawn": 13000, "deposit": 0, "closing_balance": 28702.38},
    {"date": "8/6/2025", "narration": "UPI-ZEPTO MARKETPLACE PR-ZEPTO.PAYU@AXISBANK-UTIB0000100-106150632785-UPI", "withdrawn": 651, "deposit": 0, "closing_balance": 28051.38},
    {"date": "8/6/2025", "narration": "UPI-NOUSHAD K-PAYTMQR69SSD7@PTYS-YESB0PTMUPI-106150844939-UPI", "withdrawn": 15, "deposit": 0, "closing_balance": 28036.38},
    {"date": "8/6/2025", "narration": "UPI-ANANDI A-Q065262193@YBL-YESB0YBLUPI-663988451595-UPI", "withdrawn": 35, "deposit": 0, "closing_balance": 28001.38},
    {"date": "9/6/2025", "narration": "UPI-V  RAGUPATHY-Q602455552@YBL-YESB0YBLUPI-106166970607-UPI", "withdrawn": 30, "deposit": 0, "closing_balance": 27971.38},
    {"date": "9/6/2025", "narration": "UPI-TANISHQ  RINJAY-TANISHQBARANWAL@OKICICI-KKBK0004280-516002110537-UPI", "withdrawn": 0, "deposit": 50, "closing_balance": 28021.38},
    {"date": "9/6/2025", "narration": "UPI-OJAS  AKLECHA-OJASAKLECHAYT-1@OKSBI-SBIN0012275-516001238743-UPI", "withdrawn": 0, "deposit": 50, "closing_balance": 28071.38},
    {"date": "9/6/2025", "narration": "UPI-NITIN KUMAR JHA-JHANITIN906-1@OKICICI-KKBK0000430-516047713037-CAKE", "withdrawn": 0, "deposit": 50, "closing_balance": 28121.38},
    {"date": "9/6/2025", "narration": "UPI-OJAS SO INDRAJEET AK-OJASAKLECHAYT@OKSBI-BKID0009547-516001341447-UPI", "withdrawn": 0, "deposit": 350, "closing_balance": 28471.38},
    {"date": "9/6/2025", "narration": "UPI-MS MEHAK KHANNA-MEHAKHANNA1311@OKICICI-IDIB000S746-516012402854-UPI", "withdrawn": 0, "deposit": 50, "closing_balance": 28521.38},
    {"date": "9/6/2025", "narration": "UPI-ITISH  SRIVASTAVA-9984113768@PTSBI-SBIN0018244-516066158853-SENT USING PAYTM U", "withdrawn": 0, "deposit": 50, "closing_balance": 28571.38},
    {"date": "9/6/2025", "narration": "UPI-MUFTI MOHAMMAD USMAN-9682194502@PTAXIS-JAKA0EMPIRE-516077271642-SENT USING PAYTM U", "withdrawn": 0, "deposit": 50, "closing_balance": 28621.38},
    {"date": "10/6/2025", "narration": "UPI-ARYAN KAMBOJ-9149345908@PTYES-PUNB0482000-385019402062-SENT USING PAYTM U", "withdrawn": 0, "deposit": 50, "closing_balance": 28671.38},
    {"date": "10/6/2025", "narration": "UPI-SHASHVI MITESH SHAH-SHASHVISHAH.993@OKHDFCBANK-UBIN0531286-106218876339-UPI", "withdrawn": 0, "deposit": 50, "closing_balance": 28721.38},
    {"date": "10/6/2025", "narration": "UPI-SURYADEVARA MEGHANA -8904586724@IBL-ICIC0002330-326361190546-PAYMENT FROM PHONE", "withdrawn": 0, "deposit": 50, "closing_balance": 28771.38},
    {"date": "10/6/2025", "narration": "UPI-SUKRITI SINGH-SUKRITISINGH583@OKHDFCBANK-HDFC0001460-106226904010-CAKE", "withdrawn": 500, "deposit": 0, "closing_balance": 28271.38},
    {"date": "10/6/2025", "narration": "ME DC SI 435584XXXXXX8558 CLAUDE.AI SUBSCRIPTION", "withdrawn": 2023.11, "deposit": 0, "closing_balance": 26248.27},
    {"date": "10/6/2025", "narration": "ME DC SI 435584XXXXXX8558 WINDSURF", "withdrawn": 1517.33, "deposit": 0, "closing_balance": 24730.94},
    {"date": "11/6/2025", "narration": "UPI-V  RAGUPATHY-Q602455552@YBL-YESB0YBLUPI-106278290739-UPI", "withdrawn": 30, "deposit": 0, "closing_balance": 24700.94},
    {"date": "11/6/2025", "narration": "UPI-SUHAIL-PAYTM.S1ED0LB@PTY-YESB0MCHUPI-106315917980-VAPE", "withdrawn": 2400, "deposit": 0, "closing_balance": 22300.94},
    {"date": "11/6/2025", "narration": "UPI-MR OJAS  TYAGI-TYAGIOJAS@SLC-NESF0000333-516227722706-PAYMENT FROM SLICE", "withdrawn": 0, "deposit": 7400, "closing_balance": 29700.94},
    {"date": "12/6/2025", "narration": "UPI-OJAS SO INDRAJEET AK-OJASAKLECHAYT@OKSBI-BKID0009547-516375300293-MADHUGIRI", "withdrawn": 0, "deposit": 580, "closing_balance": 30280.94},
    {"date": "12/6/2025", "narration": "UPI-ITISH  SRIVASTAVA-9984113768@PTSBI-SBIN0018244-516311508568-SENT USING PAYTM U", "withdrawn": 0, "deposit": 580, "closing_balance": 30860.94},
    {"date": "12/6/2025", "narration": "UPI-SHASHVI MITESH SHAH-SHASHVISHAH.993@OKHDFCBANK-UBIN0531286-106375787589-UPI", "withdrawn": 0, "deposit": 580, "closing_balance": 31440.94},
    {"date": "12/6/2025", "narration": "UPI-SURYADEVARA MEGHANA -8904586724@IBL-ICIC0002330-290674674472-PAYMENT FROM PHONE", "withdrawn": 0, "deposit": 580, "closing_balance": 32020.94},
    {"date": "12/6/2025", "narration": "UPI-HCUBE WOWCARZ PVT LT-WOWCARZ730238.RZP@RXAXIS-UTIB0000RZP-516323476077-UPI PAYMENT", "withdrawn": 6049.2, "deposit": 0, "closing_balance": 25971.74},
    {"date": "12/6/2025", "narration": "UPI-SAAI NANDINI HOTELS-SAAINANDINIHOTELS@YBL-YESB0YBLUPI-106377587612-PAYMENT FOR 684B14", "withdrawn": 200, "deposit": 0, "closing_balance": 25771.74},
    {"date": "13/06/25", "narration": "UPI-ABHIJAY JAIN-ABHIJAY.3486@WAAXIS-STCB0000065-302915271645-UPI", "withdrawn": 0, "deposit": 1220, "closing_balance": 26991.74},
    {"date": "13/06/25", "narration": "UPI-SRI LAKSHMI ENTERPRI-Q922666564@YBL-YESB0YBLUPI-302958131645-UPI", "withdrawn": 1220, "deposit": 0, "closing_balance": 25771.74},
    {"date": "14/06/25", "narration": "UPI-BLINKIT-BLINKIT.PAYU@HDFCBANK-HDFC0MERUPI-106432005907-UPIINTENT", "withdrawn": 163, "deposit": 0, "closing_balance": 25608.74},
    {"date": "14/06/25", "narration": "ME DC SI 435584XXXXXX8558 WINDSURF", "withdrawn": 1526.23, "deposit": 0, "closing_balance": 24082.51},
    {"date": "14/06/25", "narration": "UPI-MAYUR CHANDRAKANTH V-MAYUR.CVAISHNAV-2@OKAXIS-UTIB0004163-106460052684-UPI", "withdrawn": 80, "deposit": 0, "closing_balance": 24002.51},
    {"date": "14/06/25", "narration": "UPI-SRI LAKSHMI ENTERPRI-Q065565832@YBL-YESB0YBLUPI-106484106642-OH", "withdrawn": 660, "deposit": 0, "closing_balance": 23342.51},
    {"date": "14/06/25", "narration": "UPI-MUNCHMART TECHNOLOGI-MUNCHMART.PAYU@ICICI-ICIC0DC0099-106484729564-UPIINTENT", "withdrawn": 212, "deposit": 0, "closing_balance": 23130.51},
    {"date": "15/06/25", "narration": "POS 435584XXXXXX8558 WINDSURF", "withdrawn": 1526.23, "deposit": 0, "closing_balance": 21604.28},
    {"date": "15/06/25", "narration": "ME DC SI 435584XXXXXX8558 WINDSURF", "withdrawn": 1526.23, "deposit": 0, "closing_balance": 20078.05},
    {"date": "15/06/25", "narration": "UPI-ICH HSR LAYOUT BANGA-VYAPAR.169022734267@HDFCBANK-HDFC0MERUPI-106508407374-CHOLE", "withdrawn": 315, "deposit": 0, "closing_balance": 19763.05},
    {"date": "15/06/25", "narration": "UPI-STAR BAZAAR-STARBAZAAR.42639244@HDFCBANK-HDFC0MERUPI-106510682973-UPI", "withdrawn": 2156.68, "deposit": 0, "closing_balance": 17606.37},
    {"date": "15/06/25", "narration": "UPI-STAR BAZAAR-STARBAZAAR.42639244@HDFCBANK-HDFC0MERUPI-106510735345-UPI", "withdrawn": 19, "deposit": 0, "closing_balance": 17587.37},
    {"date": "15/06/25", "narration": "UPI-SUPRATIK SENGUPTA-SUPRATIKSENGUPTA2002@OKAXIS-UTIB0000255-106519060423-COFFEE", "withdrawn": 200, "deposit": 0, "closing_balance": 17387.37},
    {"date": "15/06/25", "narration": "UPI-BLINKIT-BLINKIT.PAYU@HDFCBANK-HDFC0MERUPI-106522613285-UPIINTENT", "withdrawn": 269, "deposit": 0, "closing_balance": 17118.37},
    {"date": "15/06/25", "narration": "UPI-DOMINOS PIZZA-PAYTM-51955531@PTYS-YESB0PTMUPI-106533802508-UPI", "withdrawn": 1069.95, "deposit": 0, "closing_balance": 16048.42},
    {"date": "16/06/25", "narration": "UPI-INDIGO BY IATA-INDIGO.IATAPAY@SC-SCBL0036085-106591106684-PAYVIAIATAPAY", "withdrawn": 4515, "deposit": 0, "closing_balance": 11533.42},
    {"date": "17/06/25", "narration": "UPI-MASTER SUHAIL M G M -BHARATPE9L0P7Z2O8N913797@YESBANKLTD-YESB0YESUPI-106632019441-PAY TO BHARATPE ME", "withdrawn": 2400, "deposit": 0, "closing_balance": 9133.42},
    {"date": "17/06/25", "narration": "UPI-SHIVANSH KUMAR YADAV-Q296759232@YBL-YESB0YBLUPI-106632136240-UPI", "withdrawn": 20, "deposit": 0, "closing_balance": 9113.42},
    {"date": "20/06/25", "narration": "ME DC SI 435584XXXXXX8558 WINDSURF", "withdrawn": 1538.82, "deposit": 0, "closing_balance": 7574.6},
    {"date": "20/06/25", "narration": "UPI-SHIVANG SHARMA-9521062304@PTYES-ICIC0006758-686710921790-SENT FROM PAYTM", "withdrawn": 0, "deposit": 1533, "closing_balance": 9107.6},
    {"date": "20/06/25", "narration": "UPI-SRI LAKSHMI ENTERPRI-Q065565832@YBL-YESB0YBLUPI-106793562574-UPI", "withdrawn": 4150, "deposit": 0, "closing_balance": 4957.6},
    {"date": "20/06/25", "narration": "UPI-SRI LAKSHMI ENTERPRI-Q922666564@YBL-YESB0YBLUPI-183859021715-UPI", "withdrawn": 1110, "deposit": 0, "closing_balance": 3847.6},
    {"date": "20/06/25", "narration": "UPI-ABHIJAY  JAIN-9098083486@SUPERYES-STCB0000065-553773723112-UPI", "withdrawn": 100, "deposit": 0, "closing_balance": 3747.6},
    {"date": "21/06/25", "narration": "UPI-PADMA K-GPAY-11239211941@OKBIZAXIS-UTIB0000553-106804262120-UPI", "withdrawn": 898, "deposit": 0, "closing_balance": 2849.6},
    {"date": "21/06/25", "narration": "UPI-MANOJ LALMANI GUPTA-PAYTMQRT5PIGX0079@PAYTM-YESB0PTMUPI-106822585963-UPI", "withdrawn": 343, "deposit": 0, "closing_balance": 2506.6},
    {"date": "21/06/25", "narration": "UPI-VISHWANATH SUBBAYYA -Q602178386@YBL-YESB0YBLUPI-106846256806-UPI", "withdrawn": 30, "deposit": 0, "closing_balance": 2476.6},
    {"date": "22/06/25", "narration": "UPI-PATIL BHAVESH YASHAV-Q497473377@YBL-YESB0YBLUPI-106872246649-UPI", "withdrawn": 48, "deposit": 0, "closing_balance": 2428.6},
    {"date": "22/06/25", "narration": "UPI-FRESKO-VYAPAR.170724793924@HDFCBANK-HDFC0MERUPI-106880411309-CAKE", "withdrawn": 340, "deposit": 0, "closing_balance": 2088.6},
    {"date": "22/06/25", "narration": "UPI-VIKAS PRAHLAD GUPTA-VIKAS080874@OKICICI-ICIC0000203-517390250424-UPI", "withdrawn": 0, "deposit": 5000, "closing_balance": 7088.6},
    {"date": "23/06/25", "narration": "UPI-TRINETRA PETROLIUM-Q095448159@YBL-YESB0YBLUPI-106911183293-UPI", "withdrawn": 3384, "deposit": 0, "closing_balance": 3704.6},
    {"date": "23/06/25", "narration": "UPI-FOOD CARNIVAL 1-PAYTM.D19587027184@PTY-YESB0MCHUPI-106912401757-UPI", "withdrawn": 260, "deposit": 0, "closing_balance": 3444.6},
    {"date": "23/06/25", "narration": "UPI-PANDA FOOD AND BEVER-GETEPAY.RJSSBPQR635445@ICICI-ICIC0DC0099-517468197675-UPI", "withdrawn": 3200, "deposit": 0, "closing_balance": 244.6},
    {"date": "23/06/25", "narration": "UPI-SHREYAS JAGADISH CHO-SHREYASHCHOULGE@OKICICI-BKID0000025-517489672957-UPI", "withdrawn": 0, "deposit": 10000, "closing_balance": 10244.6},
    {"date": "23/06/25", "narration": "UPI-S S ENTERPRISES-Q114935135@YBL-YESB0YBLUPI-106940158559-UPI", "withdrawn": 30, "deposit": 0, "closing_balance": 10214.6},
    {"date": "23/06/25", "narration": "UPI-ATHARV SHAILESH KANB-7045314996@SUPERYES-UTIB0000574-517407754867-PAID VIA SUPERMONE", "withdrawn": 0, "deposit": 1, "closing_balance": 10215.6},
    {"date": "23/06/25", "narration": "UPI-ATHARV SHAILESH KANB-7045314996@SUPERYES-UTIB0000574-517407758854-PAID VIA SUPERMONE", "withdrawn": 0, "deposit": 10000, "closing_balance": 20215.6},
    {"date": "24/06/25", "narration": "UPI-SUNEEL KUMAR YADAV-SK16450325984@OKHDFCBANK-KKBK0001417-107005662301-UPI", "withdrawn": 80, "deposit": 0, "closing_balance": 20135.6},
    {"date": "25/06/25", "narration": "UPI-PREM AUTO SERVICE-PAYTM.D14987607561@PTY-YESB0MCHUPI-107033931811-UPI", "withdrawn": 2000, "deposit": 0, "closing_balance": 18135.6},
    {"date": "26/06/25", "narration": "UPI-GUPTA SHEETAL VIKAS-SVG0114-1@OKICICI-SRCB0000060-517740964791-UPI", "withdrawn": 0, "deposit": 2500, "closing_balance": 20635.6},
    {"date": "26/06/25", "narration": "UPI-MAHALE MADHAV DAULAT-Q780005766@YBL-YESB0YBLUPI-107087413865-UPI", "withdrawn": 120, "deposit": 0, "closing_balance": 20515.6},
    {"date": "26/06/25", "narration": "UPI-KESHAV PRASAD GUPTA-Q551726902@YBL-YESB0YBLUPI-107092029384-UPI", "withdrawn": 120, "deposit": 0, "closing_balance": 20395.6},
    {"date": "26/06/25", "narration": "UPI-ITISH  SRIVASTAVA-9984113768@PTSBI-SBIN0018244-107098425623-CAR", "withdrawn": 580, "deposit": 0, "closing_balance": 19815.6},
    {"date": "26/06/25", "narration": "UPI-G S TRADERS-Q396047299@YBL-YESB0YBLUPI-107106512365-UPI", "withdrawn": 50, "deposit": 0, "closing_balance": 19765.6},
    {"date": "26/06/25", "narration": "UPI-PATIL BHAVESH YASHAV-Q497473377@YBL-YESB0YBLUPI-107106973616-UPI", "withdrawn": 1, "deposit": 0, "closing_balance": 19764.6},
    {"date": "26/06/25", "narration": "UPI-AAIJI CHEMIST-Q182201128@YBL-YESB0YBLUPI-107107697765-MEDS", "withdrawn": 518, "deposit": 0, "closing_balance": 19246.6},
    {"date": "27/06/25", "narration": ".DC INTL POS TXN MARKUP+ST 030625 030625-MIR2617280646626", "withdrawn": 62.57, "deposit": 0, "closing_balance": 19184.03},
    {"date": "27/06/25", "narration": "UPI-CLEARTRIP-CLEARTRIP850.RZP@ICICI-ICIC0DC0099-554427281152-PAYMENTTOCLEARTRIP", "withdrawn": 3544, "deposit": 0, "closing_balance": 15640.03},
    {"date": "27/06/25", "narration": "UPI-RESTAURANT BRANDS AS-BURGERKINGINDIA231415.RZP@RXAXIS-UTIB0000RZP-517818733313-VIVIANAMALLTHANEMU", "withdrawn": 575.38, "deposit": 0, "closing_balance": 15064.65},
    {"date": "28/06/25", "narration": "UPI-JASPAL SINGH LAKHWIN-Q348300133@YBL-YESB0YBLUPI-107180721932-UPI", "withdrawn": 390, "deposit": 0, "closing_balance": 14674.65},
    {"date": "28/06/25", "narration": "UPI-JAGDISH BHIMA PAWAR-Q682357323@YBL-YESB0YBLUPI-107196340300-UPI", "withdrawn": 30, "deposit": 0, "closing_balance": 14644.65},
    {"date": "28/06/25", "narration": "UPI-NEW  A1  DAIRY-Q437666473@YBL-YESB0YBLUPI-107205683953-PRASAS", "withdrawn": 130, "deposit": 0, "closing_balance": 14514.65},
    {"date": "29/06/25", "narration": "UPI-SHEETAL RATANSINGH R-PAYTMQR6AXEKI@PTYS-YESB0PTMUPI-107225001671-UPI", "withdrawn": 20, "deposit": 0, "closing_balance": 14494.65},
    {"date": "29/06/25", "narration": "UPI-RAKESH DURJANLAL GUP-PAYTMQR5YYZM8@PTYS-YESB0PTMUPI-107231464740-PAV", "withdrawn": 120, "deposit": 0, "closing_balance": 14374.65},
    {"date": "29/06/25", "narration": "UPI-SHEETAL RATANSINGH R-PAYTMQR5ZOTVZ@PTYS-YESB0PTMUPI-107231746215-UPI", "withdrawn": 30, "deposit": 0, "closing_balance": 14344.65},
    {"date": "29/06/25", "narration": "UPI-SUKRITI SINGH-SUKRITISINGH583@OKHDFCBANK-HDFC0001460-107238849108-UPI", "withdrawn": 0, "deposit": 1537, "closing_balance": 15881.65},
    {"date": "29/06/25", "narration": "UPI-SUJAL KUMAR TIMILSIN-SUJAL.KUMAR311@OKSBI-SBIN0005989-518067638230-UPI", "withdrawn": 0, "deposit": 1514, "closing_balance": 17395.65},
    {"date": "29/06/25", "narration": "UPI-NIKHIL GANESH BHOIR-Q862085369@YBL-YESB0YBLUPI-107242582268-UPI", "withdrawn": 42, "deposit": 0, "closing_balance": 17353.65},
    {"date": "29/06/25", "narration": "UPI-SRI LAKSHMI ENTERPRI-Q922666564@YBL-YESB0YBLUPI-417752021805-UPI", "withdrawn": 1350, "deposit": 0, "closing_balance": 16003.65},
    {"date": "30/06/25", "narration": "UPI-INN SILICON VALLEY-PAYTMQR2810050501011MHIJQ8U5VAS@PAYTM-YESB0PTMUPI-107266289311-BEER", "withdrawn": 540, "deposit": 0, "closing_balance": 15463.65},
    {"date": "30/06/25", "narration": ".DC INTL POS TXN MARKUP+ST 150625 150625-MIR2617988959515", "withdrawn": 63.04, "deposit": 0, "closing_balance": 15400.61},
    {"date": "30/06/25", "narration": ".DC INTL POS TXN MARKUP+ST 150625 150625-MIR2617988959523", "withdrawn": 63.04, "deposit": 0, "closing_balance": 15337.57},
    {"date": "30/06/25", "narration": "UPI-KETAN  JAIN-KETANJAIN805@OKSBI-SBIN0003170-518118532950-UPI", "withdrawn": 0, "deposit": 1530, "closing_balance": 16867.57},
    {"date": "30/06/25", "narration": "FT- SANCHIT-50200094914440 - THINK 41 TECHNOLOGIES PVT LTD -", "withdrawn": 0, "deposit": 18414, "closing_balance": 35281.57},
    {"date": "30/06/25", "narration": "FT- SANCHIT-50200094914440 - THINK 41 TECHNOLOGIES PVT LTD -", "withdrawn": 0, "deposit": 22000, "closing_balance": 57281.57},
    {"date": "30/06/25", "narration": "UPI-OJAS  AKLECHA-OJASAKLECHAYT-1@OKSBI-SBIN0012275-518127300199-UPI", "withdrawn": 0, "deposit": 1443, "closing_balance": 58724.57},
    {"date": "30/06/25", "narration": "UPI-SRI LAKSHMI ENTERPRI-Q922666564@YBL-YESB0YBLUPI-107311019523-OH", "withdrawn": 3920, "deposit": 0, "closing_balance": 54804.57},
    {"date": "1/7/2025", "narration": "INTEREST PAID TILL 30-JUN-2025", "withdrawn": 0, "deposit": 136, "closing_balance": 54940.57},
]

def parse_date(date_str):
    """Parse date string in various formats"""
    try:
        # Try parsing dd/mm/yy format first
        if "/" in date_str and len(date_str.split("/")[-1]) == 2:
            return datetime.strptime(date_str, "%d/%m/%y").date()
        # Try parsing dd/mm/yyyy format
        elif "/" in date_str and len(date_str.split("/")[-1]) == 4:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        # Try parsing dd/mm/yy format with different separators
        else:
            return datetime.strptime(date_str, "%d/%m/%y").date()
    except:
        # Fallback to current date if parsing fails
        return date.today()

def clear_all_collections():
    """Clear all collections in the database"""
    print("🧹 Clearing all database collections...")
    
    collections = ["users", "transactions", "relations", "spendings"]
    
    for collection_name in collections:
        docs = db.collection(collection_name).stream()
        batch = db.batch()
        count = 0
        
        for doc in docs:
            batch.delete(doc.reference)
            count += 1
            
            # Commit batch every 100 docs to avoid limits
            if count % 100 == 0:
                batch.commit()
                batch = db.batch()
        
        # Commit remaining docs
        if count % 100 != 0:
            batch.commit()
            
        print(f"   ✅ Cleared {count} documents from {collection_name}")

def create_test_user():
    """Create a test user with predefined credentials"""
    print("👤 Creating test user...")
    
    hashed_password = pwd_ctx.hash(TEST_USER_PASSWORD)
    user = create_user(TEST_USER_NAME, TEST_USER_EMAIL, hashed_password)
    
    print(f"   ✅ Created user: {TEST_USER_NAME} ({TEST_USER_EMAIL})")
    return user

def populate_transactions(user_id):
    """Populate database with sample transaction data"""
    print("💰 Populating sample transactions...")
    
    transactions = []
    
    for txn_data in SAMPLE_TRANSACTIONS:
        transaction = TransactionIn(
            user_id=user_id,
            date=parse_date(txn_data["date"]),
            narration=txn_data["narration"],
            withdrawn=txn_data["withdrawn"],
            deposit=txn_data["deposit"],
            type="UPI" if "UPI-" in txn_data["narration"] else "BANK",
            tags=[],
            remarks="Imported from sample data",
            processed=True
        )
        transactions.append(transaction)
    
    # Create transactions in batches
    batch_size = 50
    total_created = 0
    
    for i in range(0, len(transactions), batch_size):
        batch = transactions[i:i + batch_size]
        created_ids = batch_create(batch)
        total_created += len(created_ids)
        print(f"   ✅ Created batch {i//batch_size + 1}: {len(created_ids)} transactions")
    
    print(f"   ✅ Total transactions created: {total_created}")

def main():
    """Main function to initialize the database"""
    print("🚀 Starting database initialization...")
    print("=" * 50)
    
    try:
        # Step 1: Clear all collections
        clear_all_collections()
        
        # Step 2: Create test user
        user = create_test_user()
        
        # Step 3: Populate transactions
        populate_transactions(user["id"])
        
        print("=" * 50)
        print("✅ Database initialization completed successfully!")
        print(f"Test user credentials:")
        print(f"   Email: {TEST_USER_EMAIL}")
        print(f"   Password: {TEST_USER_PASSWORD}")
        print(f"   User ID: {user['id']}")
        
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        raise

if __name__ == "__main__":
    main()