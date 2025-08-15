#!/usr/bin/env python
# coding: utf-8

# ##### ****
# ##### Ez a Jupyter Notebook a https://dataklub.hu egyik tananyagához tartozó Python kódot tartalmazza.
# ##### A tananyag, a videó és minden egyéb itt érhető el: https://dataklub.hu/eloadasok/ai-onboarding/
# ##### ****

# # 1. IMPORT + CREDENTIALS
import json
import openai
import requests
import yaml

credentials = yaml.load(open('/home/tomi/auth/auth.yml'), Loader=yaml.FullLoader)
openai_api_key = credentials['openai_api_key']


# # 2. PROCESSING TYPEFORM ANSWERS
with open('/home/tomi/webhook_project/typeform/typeform_payload.json', 'r') as f:
    data = json.load(f)


# ### user's email address
email = data['form_response']['hidden']['email']


# ### turn typeform json into python dict
qa_dict = {}

for i in data['form_response']['definition']['fields']:
    for f in data['form_response']['answers']:
        if f['field']['id'] == i['id']:
            question = i['title'].replace('_', '').replace('*', '')
            if i['type'] == 'opinion_scale':
                field_type = f['type']
                answer = f"{str(f[field_type])}/10"
            elif i['type'] == 'multiple_choice':
                if f['type'] == 'choice':
                    try:
                        answer = f['choice']['label']
                    except:
                        answer = str(f['choice']['other'])
                elif f['type'] == 'choices':
                    if f['choices']['labels']:
                        answer = ', '.join(f['choices']['labels'])
                    else:
                        answer = str(f['choices']['other'])
            elif i['type'] == 'long_text':
                answer = f['text']
            
            qa_dict[question] = answer


# ### turn Python dict into OpenAI raw text format
for i in data['form_response']['definition']['fields']:
    for f in data['form_response']['answers']:
        if f['field']['id'] == i['id']:
            if i['type'] == 'opinion_scale':
                field_type = f['type']
                print('KÉRDÉS: ' + i['title']  + " --» VÁLASZ: "  + str(f[field_type]) + '/10')
            elif i['type'] == 'multiple_choice':
                if f['type'] == 'choice':
                    print('KÉRDÉS: ' + i['title'].replace('_', '').replace('*','')  + " --» VÁLASZ: " + f['choice']['label'])
                if f['type'] == 'choices':
                    print('KÉRDÉS: ' + i['title']  + " --» VÁLASZ: " + ', '.join(f['choices']['labels']))
            elif i['type'] == 'long_text':
                print('KÉRDÉS: ' + i['title'] + " --» VÁLASZ: " + f['text'])


# # 3. LE PROMPT
message_1 = '''Egy levelet írsz a Data Science Klub új tagjának. Te vagy a Data Science Klub vezetője, Mester Tomi. A stílusod, kedves, segítőkész, empatikus, de lényegre törő és tömör.

A data science klubról röviden:
Fejlődni vágyó data scientist és data analyst junioroknak és medioroknak szól.
A mottó: Tanulj Magyarország „ultra senior” adatos szakembereitől és mozogj magabiztosan az álláspiacon!
Mester Tomi mondja: "A Data Science Klubbal tudást, kapcsolati hálót és portfólióépítési lehetőséget kapnak az adatos kollégák. Megkapják mindazt, ami egy sikeres data science karrierhez kellhet.
Magyarország legjobb adatos szakembereit hívom előadni, még én is tanulok tőlük, pedig 10+ éve foglalkozom a területtel.”

A FELADAT:
Az új tag kitöltött egy onboarding kérdőívet, ez alapján kell neki egy személyes fejlődési tervet. összeállítani. 

UTASÍTÁSOK A LEVÉL MEGÍRÁSÁHOZ:
A levelet egy sablon alapján kell összeraknod (lásd lentebb).
A sablonnak vannak fix részei, ezeket mindig szó szerint használd, ne változtass rajtuk! 
A levélben vannak változó részek, amiket [] szögletes zárójellel jeleztem. Itt vagy választanod kell előre megadott opciókból, vagy ki kell töltened a szövegrészt a rendelkezésre álló információk alapján.
Amikor a válaszodban/ajánlásodban utalsz egy válaszra a kitölött kérdőívből, akkor így tedd: "írtad, hogy", "említetted, hogy", "a válaszaidból úgy éreztem, hogy" és hasonlók
Amikor az ajánlásokat adod, ne egy-egy konkrét választ ragadj ki a kérdőívből. Ehelyett inkább teljességében, globálisan értelmezd a kérdőívből jövő válaszokat, ez alapján próbáld meg elképzelni a felhasználót és megérteni, hogy mik az általános kihívásai és vágyai – ez alapján adj ajánlásokat.
A 0-10-ig terjedő válaszoknál, ezek a jelentések: 0: nem foglalkozott még a témával egyáltalán; 2: kezdő szinten van, de nem magabiztos tudás; 4-6: stabil alapszintű tudás; 7-8: erős, magabiztos tudás; 9-10: rutinos, sok éves tapasztalat, bármit meg tud oldani.
Ezt a részt ne írd át, mindig így tedd a levélbe szó szerint: "A Taglistáról jelölj be mindenkit Linkedin-en (https://dataklub.hu/taglista/) -- ha elsőre furának hangozhat: nem az. Ha valaki megkérdezi, hogy honnan ismered, írd csak, hogy a data science klubból, de amúgy csak az tünteti fel a Linkedin-jét, aki oké azzal, hogy bejelölöd. Amúgy pedig win-win a kapcsolati háló kölcsönös növelése akár csak ilyen online formában is."
a levél legyen szépen tördelve

FONTOS INFÓK:
A feltett kérdések:
Mennyire erősnek mondanád a jelenlegi Python tudásodat?
Mennyire erősnek mondanád a jelenlegi SQL tudásodat?
Hány _*kész*_ data science* *_*hobbiprojekt*_ van eddig a portfóliódban?
Dolgoztál már data science projekten?
Mennyire erősnek mondanád a szakmai kapcsolataid az adatos szakmán belül?
Hol tartasz most a data science karrieredben?
Elvégeztél már valamilyen data science képzést?
Ha igen volt a válaszod: milyen data science képzést végeztél már el?
Melyik témákról szeretnél tanulni jelenleg a data science területén belül? (Többet is megjelölhetsz.) Lehetséges válaszok:
Machine Learning
Kódolás (SQL, Python)
Statisztika
Üzleti gondolkodás
Adatelemzés
Data Engineering
Adatvizualizációs eszközök (PowerBI, Tableau, Looker, stb.)
Prezentáció
Karrier
Kapcsolatépités
Mesterséges Intelligencia
Esettanulmányok
Egyeb

Mi jelenleg a legnagyobb kihívás számodra a data science területén?
Hova akarsz eljutni? Mi az álomcélod a data science-szel?
Mennyi időt/energiát tervezel beletenni a klubba?	
Mi lenne az a tartalom, funkció vagy szolgáltatás, amire azt mondanád, hogy ha ezt megadja neked a Data Science Klub, akkor folyamatosan tag is maradsz benne?

"Melyik témákról szeretnél tanulni jelenleg a data science területén belül? (Többet is megjelölhetsz.)" kérdésre adott válasz fontosságát súlyozd lentebb a többihez képest: egy 0.7x-es szorzóval.

A user válaszait itt küldöm egy Python szótárként, ahol a kulcsok a kérdések, az értékek a válaszok.
'''

message_2 = str(qa_dict)

message_3 = '''Elérhető előadások a klubban:
Itt összegyűjtöttem minden tudnivalót egy .csv fájlba az előadásokról. Kérlek kifejezetten figyelj arra, hogy alapból magas értékelésű (5) előadásokat ajánlj első sorban – de közben azért figyelj arra is, hogy passzol-e az előadás szintje (kezdőknek? oszlop) a résztvevő szintjéhez ÉS kiemelten figyelj arra is, hogy mi áll a "kinek releváns" oszlopban

cím,link,értékelés,kinek releváns,teljesen kezdőknek
Adatok Prezentálása,https://dataklub.hu/adatok-prezentalasa,5,"mindenkinek; annak, akinek prezentálnia kell és nem utal arra, hogy profi lenne ebben",igen
"Sikeres Álláskeresés: Önéletrajz, Kísérőlevél, Mindset (Data Scientist-es Példákkal)",https://dataklub.hu/karrier-allaskereses-oneletrajz-kiserolevel-data-scientist,5,"mindenkinek, de főleg annak, aki említi, hogy karrier céllal jön a kurzusba",igen
"8 Machine Learning modell, amit ismerned kell (+mikor melyiket válaszd)",https://dataklub.hu/machine-learning-modellek-kozerthetoen,5,"mindenkinek, ez egy bevezető machine learning anyag, konkrét python-ozás nélkül",igen
PowerBI Alapok Junior Data Scientist-eknek,https://dataklub.hu/powerbi-alapok,5,"mindenkinek, aki nem említi, hogy powerbi alaptudás már megvan -- aki már csinált bármilyen powerBI képzést, annak nem jó!",igen
Data Engineering Elmagyarázva,https://dataklub.hu/data-engineering-alapok,4,"csak annak, aki említi, hogy data engineering vagy a technikai oldal jobban érdekli",igen
Adattisztítási Példák Valós Projektekből,https://dataklub.hu/adattisztitas-peldak-valos-projektekbol,4,"csak annak, aki említi, hogy az adattisztítás vagy a valódi adatprojektek nehézségei érdeklik",igen
Logisztikus Regresszió Python-ban egy Valós Projektből (Hitelbedőlés Vizsgálat Machine Learning-gel),https://dataklub.hu/machine-learning-a-valos-eletbol-tecnhikai-oldal,5,"mindenkinek, ez egy egyszerűbb ML-es anyag, de feltételez már egy alap python tudást",talán
[EXTRA] WhiskyReturns Tech Bemutató,https://dataklub.hu/whiskyreturns-tech-bemutato,4,akit valós projekt megvalósítása érdekel,talán
"[EXTRA] Jobb, mint a Google Analytics(?)",https://dataklub.hu/jobb-mint-a-google-analytics,4,akit az adatgyűjtés és a technikai oldal érdekel,talán
Gradient Boosting Machine (GBM) Élő Demó Python-ban (Ingatlanár Predikció),https://dataklub.hu/gbm-demo-python,5,akit a machine learning és a GBM érdekel -- alap python tudás kell hozzá,nem
Egy Senior Data Scientist Eszköztára (Produktív Adattudós),https://dataklub.hu/produktivitas,3,akit a különböző eszközök érdekelnek,igen
AutoML Bemutató Python-ban: automatizáljuk a Machine Learning-et!,https://dataklub.hu/automl,5,akit a machine learning mélyebben érdekel. előzetes machine learning és python tudás kell hozzá,nem
"Machine Learning Algoritmusok Kiértékelése: Mutatók, Mérőszámok, Fontos Értékek",https://dataklub.hu/ml-kiertekelesek,4,akit a machine learning mélyebben érdekel. egy kicsi előzetes machine learning és python tudás kell hozzá,nem
"[EXTRA] 6 Módszer, hogy Több Pénzt Keress a Data Science Tudásoddal (a data science karrieren kívül)",https://dataklub.hu/tobb-penz-ds-tudassal,4,"mindenkinek, de főleg annak, akit a karrier aspektus, esetleg a vállalkozás érdekel",igen
PowerBI a Felhőben! (operációsrendszertől függetlenül),https://dataklub.hu/power-bi-felhoben,4,"annak, akinek PowerBI alaptudása már megvan",talán
Klaszterezés Python-ban (elmélet + kódolás),https://dataklub.hu/klaszterezes-python,5,akit a machine learning és a klaszterezés érdekel -- alap python tudás kell hozzá,nem
Statisztika Data Science-hez (4 részes minisorozat),https://dataklub.hu/statisztika-data-science-1,5,"mindenkinek, főleg annak, akit a statisztika érdekel, teljesen kezdőknek is jó",igen
"Train-Test Adathalmazok Előállítása ML Modellekhez Python-ban (Minden, Amit Tudnod Kell)",https://dataklub.hu/train-test-modszerek,4,akit a machine learning mélyebben érdekel. egy kicsi előzetes machine learning és python tudás kell hozzá,talán

Íme a levél sablon.
Még egyszer: a fix részeket szó szerint vedd át!!! 
És figyelj rá, hogy a levél legyen szépen tördelve:
Ezek legyenek H2-k: "1. Tanulás rész:" "2. Építés rész:" "3. Kapcsolataid építése:"
az utóirat (ui) részek legyenek dőlt betűvel szedve

Mielőtt belevágsz a levélbe, klasszifikáld a felhasználót, *túl kezdő* vagy *nem túl kezdő* kategóriába.
"Túl kezdőbe" kerül, ha ezek közül legalább 2 igaz:
Python tudása kisebb 3
SQL tudása kisebb mint 2
Ezt írja: "Még a tanulási folyamat elején/közepén vagyok. (Nincs munkatapasztalatom.)"
Nem végzett még semmilyen data science képzést

Minden egyéb esetben "Nem túl kezdő" kategóriába kerül.
Ha azt írja, hogy doglozott "Igen, valós életbeli projekten. (Ügyfél, munkahely, stb...)" és volt legalább 1 hobbiprojektje, akkor minden fenti ellenére is a "nem túl kezdő" kategóriába kerül.

Minden fenti ellenére is a "nem túl kezdő" kategóriába kerül kategóriába, ha az alábbiak vázlatpontok közül legalább egy teljesül:
az SQL tudása 8 vagy annál nagyobb.
Ha azt írja, hogy dolgozott "Igen, valós életbeli projekten. (Ügyfél, munkahely, stb...)" ÉS volt legalább 1 hobbiprojektje
Ha a "Hol tartasz most a data science karrieredben?" kérdésre azt írja, hogy data sciene területen 1+ év munkatapasztalata van
Ha a "Hol tartasz most a data science karrieredben?" kérdésre azt írja, hogy egy közeli területen (adatelemzés vagy BI) van sok (5+ év) munkatapasztalata

LEVÉL SABLON:
TÁRGY: DS Klub: személyes fejlődési utad

SZÖVEG:
"Szia,

Köszi szépen, hogy csatlakoztál a klubhoz és hogy kitöltötted az onboarding formot is!
Ígértem, hogy ez alapján küldök neked egy levelet arról, hogy hogyan érdemes belevágnod a klub használatába.

1) Tanulás rész:
Ugye itt írtad, hogy [hivatkozz a kérdőívben kitöltött releváns válaszaira – azokat a válaszokat keresd, amik a tanulással és tapasztalattal kapcsolatos témákat dolgozzák fel. Ami a networkingre/kapcsolatépítésre vonatkozik, azt itt ne hivatkozd. A "Melyik témákról szeretnél tanulni jelenleg a data science területén belül?" kérdésben levő válaszok is érdekesek lehetnek, főleg akkor, ha max 4-5-öt jelölt meg. Ha 10 vagy többet jelölt meg itt a 12-ből, az azt jelenti, hogy általában szinte minden érdekli a data science-en belül].

A klubon belül első sorban ezeket a tananyagokat ajánlom neked indulásnak:

[tananyag címe és linkje – az ide linkelt előadás reagáljon a "Mi jelenleg a legnagyobb kihívás számodra a data science területén?"-re adott válaszra, kivétel, ha nincs releváns előadás vagy nem volt válasz arra a kérdésre], mert [pár szavas indoklás]
[tananyag címe és linkje], mert [pár szavas indoklás]
[tananyag címe és linkje – HA a Python tudása legalább 5-ös szintű, akkor itt egy specifikus Machine Learning modellről szóló tananyagot ajánlj – vagy a GMB-et vagy a logisztikus regressziósat vagy az AutoML-est], mert [pár szavas indoklás]

Ezután bele lehet egy kicsit mélyedni a [általános téma, amit a kérdőívben megjelölt és épít az előző leckékre VAGY ha egy kitöltő jelzi a kérdőívben, hogy számára a karrier, állásszerzés, data scientist pozíció megszerzése a cél, ott mindenképpen a "Sikeres Álláskeresés: Önéletrajz, Kísérőlevél, Mindset (Data Scientist-es Példákkal)" című előadást tedd majd be ide, kivétel, akkor, ha ezt fentebb már betetted], pl. ezzel az előadással:
[tananyag címe és linkje]

2) Építés rész:
[Itt kettő választásod van.

(A), ha a "túl kezdő" kategóriába klasszifikáltad a felhasználót, ezt írd:
"A Python tudásod fejlesztéséhez ajánlom először ennek az egyszerűbb kihívásnak a megoldását:
https://dataklub.hu/eloadasok/nyari-data-kihivas-2024/
Ha eleinte nehéznek érzed, akkor az is jó irány lehet, hogy először megnézed, hogy én hogyan csináltam meg, utána megpróbálod magadtól is megoldani a dolgot."

(B) Ha a "nem túl kezdő" kategóriába klasszifikáltad a felhasználót, ezt írd:
"A Python tudásod fejlesztéséhez és portfolió építéshez ajánlom a most futó versenyünket (nevezési határidő: november 4), valószínűleg erről már hallottál is, azért linkelem:
https://dataklub.hu/eloadasok/masodik-verseny/
Ez a verseny egy iszonyatosan jó lehetőség, hogy egy nagyon egyedi, valós projektet tegyél a portfoliódba, úgy, hogy azt a data science klubban a többiekkel közösen, egymást motiválva építed. (A nyereményekről és az dobogós helyezéssel járó dicsőségről nem is beszélve. :))"

]

3) Kapcsolataid építése:
A kapcsolataid erősségét [a válaszok közül a "Mennyire erősnek mondanád a szakmai kapcsolataid az adatos szakmán belül?" kérdésre adott válaszára hivatkozz] értékelted. [Csak akkor ha a "Mennyire erősnek mondanád a szakmai kapcsolataid az adatos szakmán belül?" kérdésre 6-os feletti értéket ad, akkor írd ezt: "Ez kiemelkedően erősnek számít." Ez esetben a később jövő részt úgy kezd valahogy, hogy "Viszont a kapcsolatépítéssel így is folyamatosan foglalkozni kell, hiszen ez egy fontos része…"][Csak akkor, hogy ha a "Mi jelenleg a legnagyobb kihívás számodra a data science területén?" vagy a "Hova akarsz eljutni? Mi az álomcélod a data science-szel?" részekben említi a kapcsolatok, network szerepét, akkor hivatkozz még arra is röviden. Ilyenkor írj bele valami ilyesmit: "Ezért ez a rész különösen érdekes lehet neked!" Más esetekben ez a rész nem kell.]
Ugyebár a kapcsolatépítés egy fontos része nem csak a data science karrierépítésnek, hanem a szakmai fejlődésnek is.

Itt három egyszerű lépést javaslok:
Lépj be a Slack fórumunkra és a bemutatkozás csatornán mutatkozz be (https://dataklub.hu/belsos-forum-slack/)
A Taglistáról jelölj be mindenkit Linkedin-en (https://dataklub.hu/taglista/) -- ha elsőre furának hangozhat: nem az. Ha valaki megkérdezi, hogy honnan ismered, írd csak, hogy a data science klubból, de amúgy csak az tünteti fel a Linkedin-jét, aki oké azzal, hogy bejelölöd. Amúgy pedig win-win a kapcsolati háló kölcsönös növelése akár csak ilyen online formában is.
A taglistára is tedd fel magad (ezt az űrlapot kell kitölteni: https://dataklub.hu/fiokom/taglista-adatlap/), így mások is megtalálnak téged.

+1 pro tipp, pipáld be a random network funkciót is, óriási fun és nagyon jó tapasztalat volt eddig mindenkinek, aki részt vett benne (https://dataklub.hu/random-network/)
[ha a "túl kezdő" kategóriába klasszifikáltad a felhasználót, akkor írd bele ezt is:
"Tanulás kapcsán +1 komment. A válaszaid alapján lehet, hogy a Data Science Klubhoz még egy kicsit korán csatalkoztál. Nincs kétségem afelől, hogy így is egy csomó értéket tudsz majd kiszedni belőle és nem is akarlak elbátortalanítani abban, hogy tag maradj. Viszont a DS klubtagság feltételez egy bizonyos szintű alaptudást és a válaszaid alapján elképzelhető, hogy ez neked még nincs meg. (Természetesen az is lehet, hogy én ítélem meg rosszul a helyzetet a kérdőív alapján – többen is voltak, akik egyszerűen csak szerények voltak, amikor a saját tudásukat ítélték meg, szóval simán lehet, hogy tévedek…) Akárhogy is, ha úgy érzed, hogy alapozásra van még szükséged, akkor ajánlom figyelmedbe a Junior Data Scientist Akadémia c. képzésem (https://data36.com/jds), ami egy nagyon koncentrált és alapos 3 hónapos képzés. A nulláról indítja a data science tudás átadását és egy olyan szilárd alapot tesz le, ami mind a DS karrieredben, mind a data science klubtagságodban nagy segítség lehet a jövőben.
Persze még egyszer írom: ez csak akkor érdekes, ha te is úgy érzed, hogy hiányoznak még az alapok és azt egy vezetettebb képzés során akarod megszerezni. (A másik irány a learning-by-doing, akkor kiváló helyen vagy a DS Klubban.)"]

Remélem, ez segít!
Ha bármi kérdésed van, írj!

ui.: és ha esetleg egy válasz emailben megírnád, hogy mennyire volt hasznos ez az email, azt megköszönöm!
ui.2.: a tied az egyik első olyan válaszoknak, ami automatikusan és instant módon megy ki egyből a kitöltésed után. Ahogy sejted, ehhez egy nagyon erősen prompt-olt és sok klubra vonatkozó információval, valamint a saját stílusommal feltanított LLM megoldást írtam. Elég sokat teszteltem és csiszoltam ezt már korábbi résztvevőkkel, szóval remélem, hogy nem lesz benne hiba. De mivel ez az egyik első olyan email, amit kiküldés előtt én már személyesen nem néztem át, ezért kérlek adj nekem visszajelzést: (1) mennyire zavar, hogy LLM írta a választ? (2) mennyire vetted észre egyáltalán? (3) volt benne hiba?
ui.3.: ha valami kapitális hiba volt az e-mail-ben, elnézést ezúton is!
ui.4.: jó sok ui lett... :)

Köszi szépen és üdv,
Mester Tomi"

Eddig tartott a sablon. Kérlek még egyszer nézd át, hogy a sablonhoz képest a fix részeken nem változtattál-e és ha igen, akkor javítsd!
Nézd át a tördelést is! Ha nem szép, akkor legyen szép!

FONTOS: Semmi mást ne válaszolj, csak és kizárólag a levél szövegét. Ne jelenítsd meg a tárgyat, ne jelenítsd meg a háttérgondolataidat, csak a végleges levél szövegezést!

A levél legyen HTML-ben formázva, mert majd egy HTML alapú email küldővel fogom elküldeni.
A nyitó és záró ```html tag és hasonlók nem kellenek, elég ha a sorokban megvannak a <p> <h1>, a linkek beágyazva, stb.
'''


# In[ ]:


message = message_1 + '\n' + message_2 + '\n' + message_3


# # 4. OPENAI API CALL
get_ipython().run_cell_magic('time', '', '\nopenai_api_key = openai_api_key\n\nurl = "https://api.openai.com/v1/chat/completions"\nheaders = {\n    "Content-Type": "application/json",\n    "Authorization": f"Bearer {openai_api_key}"\n}\n\ndata = {\n    "model": "gpt-4o-mini",\n    "messages": [{"role": "user", "content": message}],\n    "temperature": 0.7\n}\n\nresponse = requests.post(url, headers=headers, data=json.dumps(data))')
print(response.json()['choices'][0]['message']['content'])
openai_email = response.json()['choices'][0]['message']['content']


# # 5. SENDING EMAIL VIA BREVO API
credentials = yaml.load(open('/home/tomi/auth/auth.yml'), Loader=yaml.FullLoader)
brevo_api_key = credentials['brevo_api']

url = 'https://api.brevo.com/v3/smtp/email'

headers = {
    'accept': 'application/json',
    'api-key': brevo_api_key,
    'content-type': 'application/json'
}

data = {
    "sender": {"name": "", "email": ""},
    "to": [
        {"email": email},
        {"email": ""}
    ],
    "subject": str(""),
    "htmlContent": openai_email
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("Email sent successfully!")
else:
    print("Failed to send email:", response.status_code, response.text)