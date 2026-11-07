# 🎓 Qaraqalpaqsha Grantlar Portalı (Avtomatlasqan)

Bul sayt Qaraqalpaqstan jasları ushın xalıqaralıq hám mámleketlik grantlar, stipendiyalar hám oqıw baǵdarlamaların óz ishine aladı. Sayt **Google AI Studio (Gemini)** hám **GitHub Actions** arqalı tolıq avtomat túrde ózin-ózi yangilap baradı.

---

## 🚀 Qanday qilib ishga tushiriladi? (Bosqichma-bosqich)

### 1-qadam: GitHub'da yangi Repozitoriy ochish
1. [github.com](https://github.com) ga kiring va **"New repository"** tugmasini bosing.
2. Repozitoriyga nom bering (masalan: `qaraqalpaq-grantlar`).
3. Uni **Public** qilib belgilang va **Create repository** tugmasini bosing.

---

### 2-qadam: Fayllarni GitHub'ga yuklash
Ushbu jilddagi barcha fayllarni:
* `index.html`
* `.gitignore`
* `data/grants.json`
* `scripts/generate_grant.py`
* `.github/workflows/auto_update.yml`
* `README.md`

GitHub repozitoriyangizga yuklang (Drag & Drop orqali yoki Git orqali).

---

### 3-qadam: API Kalitni GitHub Secrets'ga qo'shish (Xavfsizlik)
1. GitHub repozitoriyangizda **Settings** bo'limiga kiring.
2. Chap menyudan **Secrets and variables** -> **Actions** bo'limini tanlang.
3. Yashil rangdagi **"New repository secret"** tugmasini bosing.
4. Maydonlarni to'ldiring:
   * **Name:** `GEMINI_API_KEY`
   * **Secret:** Siz bergan Google AI Studio API kaliti
5. **Add secret** tugmasini bosing.

---

### 4-qadam: GitHub Actions'ga yozish huquqini berish
1. Repozitoriyingizda **Settings** -> **Actions** -> **General** bo'limiga kiring.
2. Eng pastiga tushib **"Workflow permissions"** bo'limini toping.
3. **"Read and write permissions"** bandini tanlang va **Save** tugmasini bosing.
*(Bu skriptga yangi grantlarni avtomatik repoga saqlashga ruxsat beradi).*

---

### 5-qadam: Saytni bepul jonlantirish (GitHub Pages)
1. Repozitoriyingizda **Settings** -> **Pages** bo'limiga kiring.
2. **Branch** bo'limida:
   * `None` o'rniga `main` ni tanlang.
   * Papkaga `/ (root)` ni tanlang.
3. **Save** tugmasini bosing.
4. 1-2 daqiqadan so'ng sizga shaxsiy saytingiz manzili beriladi (masalan: `https://username.github.io/qaraqalpaq-grantlar/`).

---

### ⚡ Qo'lda test qilib ko'rish (Istagan payt yangilash):
1. Repozitoriyingizdagi **Actions** bo'limiga o'ting.
2. Chap tomondan **"Avtomat Grant Yangilaw"** workflow'ini bosing.
3. O'ng tarafdagi **"Run workflow"** tugmasini bosing.
4. Skript 1 daqiqada ishga tushadi, Gemini AI'dan yangi grant ma'lumotini qoraqalpoq tilida oladi va saytingizga avtomatik qo'shadi!
