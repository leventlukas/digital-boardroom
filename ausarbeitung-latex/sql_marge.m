SELECT Bestellung.Typ, m1.Status, m1.Typ, 
SUM(m1.Materialkosten) AS Materialkosten, 
SUM(Bestellung.Preis) AS Umsatz, 
((SUM(Bestellung.Preis) - SUM(m1.Materialkosten)) / SUM(Bestellung.Preis)) AS MargeSM
FROM Bestellung 
NATURAL JOIN (
    SELECT Auto.Auto_ID, Auto.Status, AS VerbauterWert,
    SUM(Komponente.Preis) AS Materialkosten 
	FROM Auto JOIN Komponente ON Auto.Auto_ID = Komponente.Auto_ID 
	GROUP BY Auto.Auto_ID
) AS m1
WHERE m1.Status <=4
GROUP BY Bestellung.Typ