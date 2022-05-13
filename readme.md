# Fire Sale!
## T-220-VLN2
Þetta forrit er skilaverkefnið úr Verklegu námskeiði II fyrir hóp 7.
## Hópmeðlimir:
Baldur Jónsson <baldurj21@ru.is>  
Baldur Þór Jónasson <baldurtj21@ru.is>  
Frímann Benedikt Guðjónsson <frimann21@ru.is>  
Þorbergur Erlendsson <thorbergur21@ru.is>  

## Til að keyra
Stillingarnar eru sjálfgefnar með SQlite en local_settings.py sem fylgir verkefnaskilum eru með stillingar fyrir Google Cloud Postgres.
### Uppsetning með local_settings.py
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

### DEV umhverfi
Til að keyra nýtt dev umhverfi er best að keyra eftirfarandi skipanir:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Viðbótarkröfur
- Hlaða upp myndum í Google Cloud Storage og klippa þær til
- Breyta upplýsingum um notendur ásamt lykilorði
- Geyma heimilisföng milli vörukaupa
- Skilaboðahólf fyrir samskipti milli notenda og tilkynningar frá kerfi
- Seljandi þarf að geta séð sínar sölur, sölur sem eru búnar að ganga í gegn og sölur sem eru enn uppi.
- Seljandi þarf að geta séð tilboð og samþykkt þau tilboð sem hann er sáttur við.
- Seljandi þarf að geta tekið niður sölu ef hann hættir við.

## Github
https://github.com/BaldurThor/T-220-VLN2-software/  
https://github.com/baldurjonsson/T-220-VLN2-design/  