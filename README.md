# Автор
PLushkin https://t.me/plushkin_blog        

**На чай с плюшками автору:**
Полигон, БСК, Арбитрум - любые токены - `0x79a266c66cf9e71Af1108728e455E0B1D311e95E`
Трон TRC-20 только USDT, остальное не доходит - `TEZG4iSmr31wWnvBixKgUN9Aax4bbgu1s3`

# Чё делает

Запускаете,  скрипт ждет когда откроется отпаврка в зкбридж через Л0 и начианет с заданным промежудком отпарвлять на всех кошльках сообщения из слуйных сетей в случайные  , или которые вы зададите в конфиге.



# Запуск

1. перед запуском добавьте приватные ключи в private_keys.txt
2. настройте config.py под себя
3. Установка и запуск: 

Linux/Mac
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```
Windows - https://www.youtube.com/watch?v=EqC42mnbByc
```
pip install virtualenv
virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py
```




