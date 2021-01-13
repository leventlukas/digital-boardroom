# digital-boardroom

| Status | Bedeutung           |
|--------|---------------------|
| 0      | geplant             |
| 1      | Karosserie          |
| 2      | Farbe               |
| 3      | Batterie            |
| 4      | Innenraum und Pilot |
| 5      | Lagernd             |
| 6      | geliefert           |


# Funktion Maschinenablauf

Die Produktion erfolgt nach dem Pull Prinzip. Das bedeutet, dass für jede Maschine in jeder iteration zwei Szenarien geprüft werden müssen.
1. Ist Maschine fertig mit der Produktion (Timestmps prüfen und AutoID != null): Dann wird der Timestamp in Auto.ProdTimestmp und Komponente.Einbau gespeichert. Im Falle der letzten Maschine wird der Status auf 5 (lagernd) gesetzt.
2. Ist die Maschine bereits in der lezten iteration fertig geworden: Dann wird das nächste Auto der Produktionsstrasse der Maschine, das dem status Maschine -1 entspricht, wenn Maschine -1 bereits fertig ist. Das bedeutet für Maschine 4 wenn Auto_ID = null, dann schreibe Auto_ID in Maschine 4 wo Produktionsstrasse, der Maschinenproduktionsstraße entspricht und wo Status 3 ist. Setze außerdem in Auto den Status auf 4

# REST API Setup

```
docker-compose up --build
docker ps -a 
docker exec -it digital-boardroom bash
python server.py
```
```
test.py
```