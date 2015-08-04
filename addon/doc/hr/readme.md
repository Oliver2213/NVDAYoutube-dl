#NVDA Youtube-DL dodatak

* Autori: Hrvoje Katić <info@hrvojekatic.com>.
* Preuzmite [razvojnu inačicu][1]

Ovaj dodatak integrira vaš NVDA čitač zaslona sa [Youtube-DL][2] programom. Youtube-DL je mali program za preuzimanje video zapisa sa YouTube.com i još nekolicine stranica. Za korištenje ovog dodatka, samo odaberite URL adresu video zapisa koristeći se standardnim Windows naredbama za odabir teksta, a zatim pritisnite NVDA+F8. Odabrana URL adresa bit će detektirana, a vaš video će biti automatski preuzet i pretvoren.
Pođite u NVDA izbornik, podizbornik Youtube skidač za podešavanje formata preuzimanja i ostalih mogućnosti.

##Prije nego počnete

Molimo pažljivo pročitajte informacije u ovom poglavlju.

###Pravne obavijesti

Iako su ovaj dodatak i Youtube-DL besplatni, imajte na umu da je preuzimanje materijala zaštićenog autorskim pravima protuzakonito. Prije nego što počnete s preuzimanjem bilo kakvog materijala, prihvaćate da ćete preuzimati samo one materijale koji nisu zaštićeni autorskim pravima te da ćete preuzet materijal koristiti samo isključivo za vaše osobne potrebe. Prije preuzimanja video zapisa, molimo pročitajte uvjete korištenja usluge s koje preuzimate sadržaj. Ukoliko ne prihvaćate uvjete korištenja, molimo uklonite preuzete datoteke s vašeg računala u roku 24 sata!

###Vanjski pretvornici

Youtube-DL zahtijeva korištenje nekih od vanjskih pretvornika u svrhu pretvaranja vaših preuzetih video zapisa u MP3 format, kao i u neke druge formate. Ovaj dodatak je prema početnoj vrijednosti podešen za korištenje FFMPEG pretvornika, kojeg je potrebno zasebno nabaviti zbog ogranićenja u licenci. Čak i ako ne nabavite FFMPEG, i dalje ćete moći preuzeti video, ali će krajnji rezultat preuzimanja biti datoteka u nekom drugom formatu koji možda niste htjeli.
Budući da je FFMPEG zahtjevan za kompiliranje iz izvornog koda na Windows sustavu, unaprijed kompilirane binarne datoteke možete pronaći za 32-bitne i 64-bitne Windows inačice na sljedećem linku: [http://ffmpeg.zeranoe.com/builds/][3]. Ako koristite 32-bitnu inačicu Windows sustava, molimo preuzmite 32-bitne statičke binarne datoteke. Za 64-bitne Windows inačice, preuzmite 64-bitne statičke binarne datoteke. Potrebne binarne datoteke nalaze se u pod mapi 'bin' unutar preuzete .7z arhive. Kopirajte sve izvršne .exe datoteke unutar te mape u vašu \Windows\System32 sistemsku mapu, ili \Windows\SysWOW64 mapu u slućaju 64-bitne Windows inačice. Ako i dalje imate problema s pronalaženjem FFMPEG.exe datoteke na 64-bitnim Windows inačicama, pokušajte preuzeti i 32-bitne i 64-bitne statičke binarne datoteke, a potom ih kopirajte u vaše System32 i SysWOW64 mape. Nakon toga ponovo pokrenite NVDA ukoliko bude potrebno.

##Osnovne upute za uporabu

###Primjer 1: Preuzimanje Youtube video zapisa koji se trenutno izvodi na Youtube stranici

1. Otvorite vaš Web preglednik.
2. Potražite neki video na Youtube stranici koji biste htjeli preuzeti.
3. Otvorite link željenog video zapisa.
4. Pritisnite Control+L da biste fokusirali adresnu traku. URL adresa bit će automatski odabrana čim je adresna traka u fokusu.
5. Pritisnite NVDA+F8 da biste započeli preuzimanje. Youtube-DL će automatski preuzeti video i pretvoriti ga u MP3 format u 192 KBPS kvaliteti prema početnoj vrijednosti.

###Primjer 2: Preuzimanje Youtube video zapisa putem prilijepljenog linka unutar E-Mail poruke ili dokumenta

1. Otvorite E-Mail poruku ili dokument koji sadrži neke Youtube linkove.
2. Pomaknite se strelicom dolje do redka u tekstu u kojem piše URL adresa Youtube video zapisa.
3. Odaberite URL adresu koristeći standardne Windows naredbe za odabir teksta, pazeći pritom da je potpuna URL adresa odabrana, jer ćete u protivnom dobiti pogrešku i vaš video se neće preuzeti.
4. Pritisnite NVDA+F8 da biste započeli preuzimanje. Youtube-DL će automatski preuzeti video i pretvoriti ga u MP3 format u 192 KBPS kvaliteti prema početnoj vrijednosti.

##Izbornik opcija dodatka

Pođite na NVDA izbornik, podizbornik Youtube skidač za pristup raznim opcijama koje se tiću ovog dodatka i Youtube-DL programa.

###Mogućnosti audio pretvornika

U dijaloškom okviru mogućnosti audio pretvornika možete podesiti u koji format će vaš video biti pretvoren nakon preuzimanja, te koja kvaliteta će se primijeniti.
Napomena: Iako Youtube-DL može preuzimati i u video i u audio formatima, trenutna inačica ovog dodatka podržava skidanje samo u audio formatima. Podržani zvučni formati koje možete odabrati su: MP3, Wave, Ogg Vorbis, AAC, M4A i Opus.

###Pregled preuzetih video zapisa

Ova opcija izbornika otvorit će mapu u koju se spremaju preuzeti video zapisi, gdje ih onda možete otvoriti, premjestiti ih u neku drugu mapu ili ih obrisati ako želite.

###Odaberite mapu za preuzimanje

Ova opcija izbornika omogućuje vam da odaberete mapu u kojoj će biti spremljeni preuzeti i pretvoreni video zapisi, ukoliko ste nezadovoljni zadanim mjestom za spremanje.

[1]: https://bitbucket.org/HKatic/nvda-addon-youtubedl/downloads/nvdaYoutubeDL-1.0dev.nvda-addon
[2]: https://rg3.github.io/youtube-dl/
[3]: http://ffmpeg.zeranoe.com/builds/
