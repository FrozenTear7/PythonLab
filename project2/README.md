# Wirtualny pilot
## Wyjaśnienie
- W pliku test.yaml znajdują się informacje, które są podstawą do zbudowania interfejsu graficznego 
i przesyłania informacji przez UDP do pliku main.py zawierającego program testowy.
- Wczytane z yaml'a pokoje służą jako zakładki między którymi możemy się przełączać
i posyłać do programu testowego informacje za pomocą przycisków ON i OFF, które odpowiednio
posyłają informacje o włączeniu i wyłączeniu opisywanego przedmiotu w pokoju na adres
255.255.255.255, port 2018, który nasłuchuje program testowy.
(W Pythonie 3 wiadomość posyłana przez UDP musi być zakodowana w utf-8)
- Okno interfejsu jest otwierane, a następne wypełniane zakładkami na podstawie pokoi z yaml'a.
Każdy pokój ma własną zakładkę w której znajdują się przedmioty, którymi możemy sterować.
##
Autor: Paweł Mendroch