# COVID-19 Dashboard

## Projekt célja

A projekt célja, hogy bemutassa a **COVID-19 világjárvány egészségügyi és társadalmi következményeit** valós, nyilvánosan elérhető adatok feldolgozásán keresztül.  
A rendszer a **WHO (World Health Organization)** és az **Európai Unió** által közzétett nyílt adatforrásokra épül, amelyek lehetővé teszik a járvány lefolyásának, fertőzési és halálozási trendjeinek, valamint az oltottsági arányok változásának elemzését.

A választás azért esett erre a témára, mert a COVID-19 **jelentős hatással volt a mindennapi életre**, a gazdaságra és az egészségügyi rendszerekre világszerte.  
A projekt célja, hogy ezeket a hatásokat **adatvezérelt megközelítéssel és vizuális formában** jelenítse meg, segítve ezzel a felhasználókat abban, hogy átlássák a járvány alakulását és annak hosszú távú következményeit.

Az alkalmazás inspirációját a [BrianRuizy/covid19-dashboard](https://github.com/BrianRuizy/covid19-dashboard) projekt adta,  
amely szintén a COVID-időszak adatainak vizualizációját valósította meg.  
A jelen projekt azonban a koncepciót **új szemszögből közelíti meg**, az eredeti ötletet továbbgondolva egy **tanulási és kutatási célt szolgáló kezdeményezésként**,  
amely az adatvizualizáció segítségével támogatja a járványügyi trendek és összefüggések könnyebb megértését.


## Architektúra

A projekt a modern szoftverfejlesztési elveknek megfelelően, rétegzett **mikroszerviz-szemléletű architektúrában** készült. A rendszer komponensei tisztán elkülönülnek egymástól:

### 1. Backend
* **Technológia:** FastAPI (Python)
* **Feladata:** REST API biztosítása, kommunikáció a külső adatforrásokkal.
* **Adatforrások:**
    * **WHO API:** Várható élettartam és öngyilkossági ráták.
    * **WorldBank API:** GDP adatok (idősoros).
    * **Wikipedia (Web Scraping):** Munkanélküliségi ráták (BeautifulSoup használatával).
* **Adatbázis:** SQLAlchemy ORM-et használ. Fejlesztői környezetben **SQLite**, éles környezetben (Render) **PostgreSQL** biztosítja az adattárolást.

### 2. Frontend 
* **Technológia:** Streamlit
* **Feladata:** A felhasználói felület biztosítása és az adatok vizualizációja.
* **Kommunikáció:** HTTP kéréseken keresztül kommunikál a saját Backendünkkel, így a kliens sosem hív közvetlenül külső API-t.

### 3. Programozási Paradigmák
A kódbázis vegyes paradigmát alkalmaz a hatékonyság érdekében:
* **OOP (Objektumorientált):** Szolgáltatás réteg (`WhoDataService` osztály) és adatbázis modellek.
* **Funkcionális:** Adattranszformációk (Pandas `apply`, `lambda` kifejezések) és listaelemzések.
* **Procedurális:** A vezérlési logika és a szkriptek (pl. `run.py`) felépítése.

---

## Felhasznált Technológiák

* **Nyelv:** Python 3.10+
* **Web Framework:** FastAPI, Uvicorn
* **Frontend:** Streamlit
* **Adatbázis:** SQLAlchemy, SQLite / PostgreSQL
* **Adatfeldolgozás:** Pandas, Altair (grafikonok)
* **Hálózat & Scraping:** Requests, BeautifulSoup4
* **Tesztelés:** Pytest
* **Környezetkezelés:** Python-dotenv

---

## Telepítés és Indítás

A rendszer futtatásához kövesd az alábbi lépéseket:

### 1. Előfeltételek
Legyen telepítve a gépadon a **Python 3** és a **Git**.

### 2. A projekt klónozása
```bash
git clone [https://github.com/isandormeszaros/covid19-dashboard.git](https://github.com/isandormeszaros/covid19-dashboard.git)
cd covid19-dashboard
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 main.py