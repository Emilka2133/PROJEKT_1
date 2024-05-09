1.Program służy do zamiany dowolnej ilości współrzędnych na współrzędne w innym układzie.
Oferuje on następujące funkcje:
’’transformacja XYZ -> BLH’’ służy do zamiany współrzędnych ortokartezjańskich na współrzędne geodezyjne. (xyz2flh)
 ’’transformacja BLH -> XYZ’’ służy do zamiany współrzędnych geodezyjnych na współrzędne ortokartezjańskie. 
 ’’transformacja XYZ -> neu’’ służy do zamiany współrzędnych prostokątnych płaskich na współrzędne topocentryczne.
’’transformacja BLH -> XY2000’’ służy do zamiany współrzędnych geodezyjnych na współrzędne prostokątne płaskie w układzie 2000.
 ’’transformacja BLH -> XY1992’’ służy do zamiany współrzędnych geodezyjnych na współrzędne prostokątne płaskie w układzie 1992.
Obsługiwanymi elipsami jest elipsoida GRS’80, WGS’84, Krasowskiego
 2. Aby program działał na danym komputerze użytkownik powinien mieć zainstalowanego Pythona 3.12 w wersji 64-bit oraz zainstalowaną bibliotekę numpy, math
3. Program został napisany dla systemu operacyjnego Windows Microsoft 11.
4. Utworzyłyśmy klasę o nazwie "Transformacje", której funcje obsługują dwie elipsoidy.
5. Sposób użycia poszczególnych funkcji
  - xyz2flh
    Funkcja przyjmuje plik tekstowy z rozszezreniem '.txt' na którego podstawie pobiera dane X,Y,Z punktów. Następnie transformuje za pomocą metody Hirvonena na współrzędne phi (szerokość geodezyjna),
    lambda (długość geodezyjna), h (wysokość geodezyjna).
    Parametry przekształcane są z typu string na float, aby poprawnie wykonać kod.
    parametry wejściowe:  X,Y,Z podane jest w metrach z dokładnością do 3 miejsc po przecinku
    dane wyjściowe:   f,l - podane są w stopniach dziesiętnych     h - podane jest w metrach z dokładnością do 3 miejsc po przecinku
    W rezultacie powstaje plik wynikowy posiadający trzy kolumny (kolejno f,l,h)
  - flh2xyz
    Funkcja przyjmuje plik tekstowy z rozszezreniem '.txt' na którego podstawie pobiera dane  phi (szerokość geodezyjna), lambda (długość geodezyjna), h (wysokość geodezyjna) punktów.
    Następnie transformuje za pomocą metody odwrotnej do Hirvonena na współrzędne ortokartezjańskie X,Y,Z.
    Parametry przekształcane są z typu string na float, aby poprawnie wykonać kod.
    parametry wejściowe: f,l - podane są w stopniach dziesiętnych       h - podane jest w metrach z dokładnością do 3 miejsc po przecinku
    dane wyjściowe: X,Y,Z podane jest w metrach z dokładnością do 3 miejsc po przecinku
    W rezultacie powstaje plik wynikowy posiadający trzy kolumny (kolejno X,Y,Z)
  - flh22000
    Funkcja przyjmuje plik tekstowy z rozszezreniem '.txt' na którego podstawie pobiera dane  phi (szerokość geodezyjna), lambda (długość geodezyjna), h (wysokość geodezyjna) punktów.
    Następnie transformuje na współrzędne w układzie PL-2000. Program sam rozpoznaje w jakiej strefie jest dany punkt i przyporządkowuje także odpowiednie parametry do właściwych obliczeń.
    Ważne jest aby użytkownik nie podał pliku ze współrzędnymi, które nie są na terenie Polski.
    Parametry przekształcane są z typu string na float, aby poprawnie wykonać kod.
    parametry wejściowe: f,l - podane są w stopniach dziesiętnych       h - podane jest w metrach z dokładnością do 3 miejsc po przecinku
    dane wyjściowe: X2000, Y2000 podane jest w metrach z dokładnością do 3 miejsc po przecinku
    W rezultacie powstaje plik wynikowy posiadający dwie kolumny (kolejno X2000, Y2000)
  - flh21992
    Funkcja przyjmuje plik tekstowy z rozszezreniem '.txt' na którego podstawie pobiera dane  phi (szerokość geodezyjna), lambda (długość geodezyjna), h (wysokość geodezyjna) punktów.
    Następnie transformuje na współrzędne w układzie PL-1992. Program wie, że południkiem zerowym jest 19 stopni.
    Ważne jest aby użytkownik nie podał pliku ze współrzędnymi, które nie są na terenie Polski.
    Parametry przekształcane są z typu string na float, aby poprawnie wykonać kod.
    parametry wejściowe: f,l - podane są w stopniach dziesiętnych       h - podane jest w metrach z dokładnością do 3 miejsc po przecinku
    dane wyjściowe: X1992, Y1992 podane jest w metrach z dokładnością do 3 miejsc po przecinku
    W rezultacie powstaje plik wynikowy posiadający dwie kolumny (kolejno X1992, Y1992)
   - xyz2neu
    Funkcja przyjmuje plik tekstowy z rozszezreniem '.txt' na którego podstawie pobiera dane X,Y,Z punktów oraz użytkownik musi wpisać trzy współrzędne referencyjne (ref_X, ref_Y, ref_Z)
    Następnie transformuje na współrzędne neu (do układu topocentrycznego)
    Parametry przekształcane są z typu string na float, aby poprawnie wykonać kod.
    parametry wejściowe:  X,Y,Z podane jest w metrach z dokładnością do 3 miejsc po przecinku
    dane wyjściowe:   n,e,u (str) - w metrach
    W rezultacie powstaje plik wynikowy posiadający trzy kolumny (kolejno n,e,u)

Przykłady wywołań i ich rezyltaty:
Pierwsza pozycja w wierszu poleceń: python
Druga pozycja w wierszu poleceń: nazwa pliku z kodem z rozszerzeniem .py (kod1.py)
Trzecia pozycja w wierszu poleceń: flaga wywołująca daną funkcję zamieniającą współrzędne 
Czwarta pozycja w wierszu poleceń: flaga --header_lines i po spacji podajemy ilość wierszy nagłówka, które chcemy pominąć w naszym pliku .txt z danymi,licząc od góry pliku. Numerem ragłówka może być tylko typ integer.  
Piąta pozycja w wierszu poleceń: elipsoida odniesienia (wgs84 lub grs80 lub Krasowskiego)
Szósta pozycja w wierszu poleceń: nazwa pliku, z którego pobieramy dane z pliku .txt
python kod1.py --xyz2flh --header_lines 4 wgs84 wsp_inp.txt
python kod1.py --flh2xyz --header_lines 1 wgs84 wyniki_xyz2flh.txt
python kod1.py --xyz2neu --header_lines 4 wgs84 wsp_inp.txt (Program pyta się użytkownika kolejno o wartości współrzędnych referencyjnych (XYZ), program jest dostosowany do wartości float. Gdy użytkownik napisze wartość współrzędnej, aby przejść do wpisania kolejnej współrzędnej musi kliknąć enter. Znakiem oddzielającym od części dziesiętnych jest kropka). Numerem nagłówka może być tylko typ integer. Jest to liczba wierszy nagłówka, które chcemy pominąć, licząc od góry pliku .txt.)

    
    - jak go używać wraz z kilkoma przykładami wywołań obrazującymi jak z niego korzystać (w tym opis struktury danych wejściowych i wyjściowych) 
      oraz rezultatami tych wywołań (przykładowe wywołania powinny za input brać plik z przykładowymi danymi)
    - znane błędy i nietypowe zachowania programu, które nie zostały jeszcze naprawione
