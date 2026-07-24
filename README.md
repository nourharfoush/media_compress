# 📱 طريقة بناء وتنزيل تطبيق أندرويد (APK) لبرنامج حرفوش

تم إعداد كود تطبيق الأندرويد بالكامل باستخدام **KivyMD** لتوفير واجهة تفاعلية عصرية ومناسبة للهواتف الذكية.

---

## 🛠️ الطرق المتوفرة لبناء ملف `.apk`:

### 🚀 **الطريقة الأولى (الأسهل والأسرع - عبر GitHub أونلاين مجاناً)**:
1. ارفع مجلد المشروع على حسابك في **GitHub**.
2. سيقوم ملف البناء الأوتوماتيكي المعُد جاهزاً (`.github/workflows/build_apk.yml`) بتشغيل عملية التجميع فوراً في السحاب على سيرفرات Ubuntu.
3. بعد 5 دقائق، افتح تبويب **Actions** في مجلد GitHub الخاص بك وقم بتحميل ملف **`HarfoushCompressor-Android-APK`** المكتمل مباشرة إلى هاتفك وتثبيته!

---

### 🐧 **الطريقة الثانية (عبر جهازك باستخدام Linux / WSL)**:
إذا كان لديك بيئة Linux أو نظام **WSL (Windows Subsystem for Linux)** مثبت على ويندوز:
1. افتح مبدّل الأوامر في بيئة Linux ونفّذ:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip build-essential git ffmpeg
   pip install buildozer cython==0.29.33
   ```
2. انسخ `main_android.py` إلى `main.py`:
   ```bash
   cp main_android.py main.py
   ```
3. شغّل أمر البناء:
   ```bash
   buildozer android debug
   ```
4. سيتكون ملف الـ APK النهائي داخل مجلد `bin/HarfoushMediaCompressor-1.0.0-arm64-v8a-debug.apk`.

---

### 📂 **الملفات التي تم إنشاؤها لنسخة أندرويد:**
- 📄 [`main_android.py`](file:///c:/Users/SkyTop/Desktop/New%20folder%20%285%29/main_android.py): كود تطبيق الأندرويد التفاعلي بـ KivyMD.
- ⚙️ [`buildozer.spec`](file:///c:/Users/SkyTop/Desktop/New%20folder%20%285%29/buildozer.spec): ملف إعدادات حزمة الأندرويد والصلاحيات.
- 🤖 [`.github/workflows/build_apk.yml`](file:///c:/Users/SkyTop/Desktop/New%20folder%20%285%29/.github/workflows/build_apk.yml): ملف البناء التلقائي في السحاب عبر GitHub Actions.
