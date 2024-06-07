# ChatTrafficViolation

Hello ladies and gentelman guides to run the app in your local machine : 
1. clone repo
```bash
git clone https://github.com/amine759/ChatTrafficViolation.git
```

- navigate inside the project directory 
```bash
cd ChatTrafficViolation
```
2. install and create virtual environnement in your local machine 
**note: these are linux commands(I use linux btw) look for their equivalent in windows**
```bash
python3 -m venv venv # install virtual environnement
. venv/bin/activate # activate the project's virtual environnement
```

3. once venv is created, install all necessary dependencies 
```bash
pip install -r requirements.txt
```

4. apply django migrations
```bash
python3 manage.py migrate # 
```

5. finally run django server
```bash
python3 manage.py runserver # 
```