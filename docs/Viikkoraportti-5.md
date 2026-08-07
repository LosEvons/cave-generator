Käytetyt tunnit: 3

Toteutin testit ja algoritmin MST:n laskemiselle triangulaatiosta. Huomasin myös, että nykyisessä määrittelydokumentissa mainittu A* haku reitin löytämiseksi on itseasiassa teoriassa turha, koska kaikkien solujen arvo on teoriassa määritelty samaksi, joten pitää selvittää riittääkö triangulaatio ja MST näytöksi kurssille, vai pitääkö A* haku toteuttaa hieman turhaankin, vai vaaditaanko että visualisaatio kykenee osoittamaan sen toiminnan. I'm happy in any case.
Toteutin A* haun kuitenkin, ja asetin FREE ja SOLID celleille eri arvot. Pientä refaktorointia generate_rooms.py tiedoston sisällä, yksi bugikorjaus reducen käytössä, ja huomasin että algoritmilla kestää aika kauan laskea, joten pitää selvittää missä vika.
Opin että kannattaa testata funktion käyttämät ajat ajoissa.
Tein sympy:n tilalle omat tietorakenteet ja vaihdoin ne käyttöön.