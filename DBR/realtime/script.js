google.charts.load('current', { 'packages': ['corechart'] });
google.charts.load('current', {'packages':['table']});
google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['corechart', 'bar']});
google.charts.load('current', {'packages':['line']});
google.charts.load('current', {'packages':['gauge']});
google.charts.load('current', {'packages':['timeline']});

const app = Vue.createApp({})

app.component('bestellungen', {
    template: `
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Dashboard - Bestellungen</h1>
    <div v-show="realtime">
    <button class="btn btn-primary" type="button" disabled>Daten werden geladen
  <span class="spinner-border spinner-border-sm" role="status"></span>
  <span class="sr-only"></span>
</button>
</div>
    </div>

    
    <div class="row">
      <div class="col">

      
      <p class="fs-5 fw-light text-secondary my-3">Aktuelle Lieferzeit</p><br>
      <div class="container">
  <div class="row">
    <div class="col-sm text-center">
     <span class="border p-3 fs-5 rounded" id="lieferzeit_d"></span><br><br>Tage
    </div>
    <div class="col-sm text-center">
     <span class="border p-3 fs-5 rounded" id="lieferzeit_h"></span><br><br>Stunden
    </div>
    <div class="col-sm text-center">
     <span class="border p-3 fs-5 rounded" id="lieferzeit_m"></span><br><br>Minuten
    </div>
    <div class="col-sm text-center">
     <span class="border p-3 fs-5 rounded" id="lieferzeit_s"></span><br><br>Sekunden
    </div>
  </div>
</div>
<hr>
<p class="fs-5 fw-light text-secondary my-3">Statusübersicht</p>
<div id="barchartstatus" ref="barchartstatus" style="width: 700px; height: 200px;"></div>
<hr>
<p class="fs-5 fw-light text-secondary my-3">Lagerübersicht</p>

<div class="container">
  <div class="row">
    <div class="col-md-auto">
    <div class="card" style="width: 9rem;">
    <div class="card-header">
      Karroserie
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item fw-bolder"><img src="../assets/img/hashtag.svg" width="18"> <span id="lager_menge_karroserie"></span> Stk.</li>
      <li class="list-group-item fw-bolder"><img src="../assets/img/avg.jpg" width="18"> <span id="lager_preis_karroserie"></span> €</li>
    </ul>
  </div>
    </div>
    <div class="col-md-auto">
    <div class="card" style="width: 9rem;">
    <div class="card-header">
      Batterie
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item fw-bolder"><img src="../assets/img/hashtag.svg" width="18"> <span id="lager_menge_Batterie"></span> Stk.</li>
      <li class="list-group-item fw-bolder"><img src="../assets/img/avg.jpg" width="18"> <span id="lager_preis_Batterie"></span> €</li>
    </ul>
  </div>
    </div>
    <div class="col-md-auto">
    <div class="card" style="width: 9rem;">
    <div class="card-header">
      Lack
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item fw-bolder"><img src="../assets/img/hashtag.svg" width="18"> <span id="lager_menge_Lack"></span> Stk.</li>
      <li class="list-group-item fw-bolder"><img src="../assets/img/avg.jpg" width="18"> <span id="lager_preis_Lack"></span> €</li>
    </ul>
  </div>
    </div>
    <div class="col-md-auto">
    <div class="card" style="width: 9rem;">
    <div class="card-header">
      Leder
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item fw-bolder"><img src="../assets/img/hashtag.svg" width="18"> <span id="lager_menge_Leder"></span> Stk.</li>
      <li class="list-group-item fw-bolder"><img src="../assets/img/avg.jpg" width="18"> <span id="lager_preis_Leder"></span> €</li>
    </ul>
  </div>
  </div>
  </div>
  </div>
<hr>
<p class="fs-5 fw-light text-secondary my-3">Margenübersicht</p>
<div id="gaugechart" ref="gaugechart" style="width: 500px; height: 200px;"></div>
<hr>
      </div>
      <div class="col me-3">
      <p class="fs-5 fw-light text-secondary my-3">Letzten 10 Bestellungen</p>
      <table class="table table-hover table-sm" id="bestellungtable">
  <thead>
    <tr>
    <th scope="col">Eingang</th>
      <th scope="col">Typ</th>
      <th scope="col">Batterie</th>
      <th scope="col">Farbe</th>
      <th scope="col">Leder</th>
      <th scope="col" style="text-align: right;">Preis</th>
    </tr>
  </thead>
  <tbody>
  <tr v-for="item in bestellungen">
  <th scope="row">{{item.Eingang}}</th>  
  <td>{{item.Typ}}</td>
    <td>{{item.Batterie}}</td>
    <td>{{item.Farbe}}</td>
    <td>{{item.Leder}}</td>
    <td style="text-align: right;">{{item.Preis}} €</td>
  </tr>
  </tbody>
</table>
<hr>
<p class="fs-5 fw-light text-secondary my-3">Anzahl Bestellungen letzte Stunde</p>
      <div id="linechart" ref="linechart" style="width: 800px; height: 300px;"></div>
      <hr>
      <p class="fs-5 fw-light text-secondary my-3">Umsatz / Bestellungen letzten 5 Tage</p>
      <div id="barchart" ref="barchart" style="width: 800px; height: 300px;"></div>
      </div>
    </div>
  </div>
  <br>
  <br>
  <hr>
<p class="fw-light">&copy; by Levent Lukas & Jan Warwas</p>
    `,
    data: function () {
        return {
            data: [],
            realtime: false,
            intervall_BT: 0,
            intervall_BL: 0,
            intervall_UB: 0,
            intervall_MG: 0,
            intervall_LW: 0,
            intervall_BS: 0,
            intervall_LZ: 0,
            bestellungen: []


        }
    },
    mounted() {
        this.getData_BT()
        this.getData_BL()
        this.getData_UB()
        this.getData_MG()
        this.getData_LW()
        this.getData_BS()
        this.getData_LZ()
        google.charts.setOnLoadCallback(() => this.drawChart_BL())
        google.charts.setOnLoadCallback(() => this.drawChart_UB())
        google.charts.setOnLoadCallback(() => this.drawChart_MG())
        google.charts.setOnLoadCallback(() => this.drawChart_BS())
        this.getRealtimeData()

    },
    methods: {
        getData_BT() {
            axios.get(api_BT)
                .then(response => {
                    this.bestellungen = response.data
                })
        },
       
        getData_BL() {
            axios.get(api_BL)
                .then(response => {
                    this.data = response.data
                    this.drawChart_BL()
                })
        },
        drawChart_BL() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


          data.addColumn('timeofday', '');
            data.addColumn('number', 'Anzahl Bestellungen');

            for (var i = 0; i < jsonData.length; i++) {
                sales = parseInt(jsonData[i].count);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], sales]
                ]);
            }  

            var options = {
                legend: {position: 'none'},
                vAxis: {
                    viewWindow: {
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.linechart);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_UB() {
            axios.get(api_UB)
                .then(response => {
                    this.data = response.data
                    this.drawChart_UB()
                })
        },
        drawChart_UB() {

            jsonData = this.data

            var data = new google.visualization.DataTable();
              data.addColumn('string', '');
              data.addColumn('number', 'Bestellungen');
              data.addColumn('number', 'Umsatz');


              for (var i = 0; i < jsonData.length; i++) {
                anzahl = parseInt(jsonData[i].Anzahl)
                umsatz = parseInt(jsonData[i].Umsatz)
                data.addRows([
                    [jsonData[i].Datum, anzahl, umsatz]
                  ]);
            }  

            var options = {
                legend: {position: 'in'},
                series: {
                  0: { axis: 'Bestellungen'}, // Bind series 0 to an axis named 'distance'.
                  1: { axis: 'Umsatz' } // Bind series 1 to an axis named 'brightness'.
                },
                axes: {
                  y: {
                    Anzahl: {label: 'Bestellungen'}, // Left y-axis.
                    Umsatz: {side: 'right', label: 'Umsatz'} // Right y-axis.
                  }
                }
                
              };
            
            var chart = new google.charts.Bar(this.$refs.barchart);
 
            chart.draw(data, google.charts.Bar.convertOptions(options));
        },
        getData_MG() {
            axios.get(api_MG)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MG()
                })
        },
        drawChart_MG() {

            jsonData = this.data

            var data = new google.visualization.DataTable();
              data.addColumn('string', 'Typ');
              data.addColumn('number', 'Marge'); 


              for (var i = 0; i < jsonData.length; i++) {
                marge = parseInt(jsonData[i].Marge)
                data.addRows([
                    [jsonData[i].Typ ,marge]
                  ]);
            }   

            var options = {
                redFrom: 0, redTo: 35,
                yellowFrom: 35, yellowTo: 50,
                greenFrom: 50, greenTo: 100,
                minorTicks: 5
              };
            
            var chart = new google.visualization.Gauge(this.$refs.gaugechart);
 
            chart.draw(data, options);
        },
         getData_LW() {
            axios.get(api_LW)
                .then(response => {
                    this.data = response.data
                    this.drawChart_LW()
                })
        },
        drawChart_LW() {

            jsonData = this.data
            document.getElementById("lager_menge_karroserie").innerHTML = jsonData[0].Menge;
            document.getElementById("lager_preis_karroserie").innerHTML = jsonData[0].Preis;
            document.getElementById("lager_menge_Batterie").innerHTML = jsonData[1].Menge;
            document.getElementById("lager_preis_Batterie").innerHTML = jsonData[1].Preis;
            document.getElementById("lager_menge_Lack").innerHTML = jsonData[2].Menge;
            document.getElementById("lager_preis_Lack").innerHTML = jsonData[2].Preis;
            document.getElementById("lager_menge_Leder").innerHTML = jsonData[3].Menge;
            document.getElementById("lager_preis_Leder").innerHTML = jsonData[3].Preis;


        }, 

        getData_BS() {
            axios.get(api_BS)
                .then(response => {
                    this.data = response.data
                    this.drawChart_BS()
                })
        },
        drawChart_BS() {

            jsonData = this.data

            var data = new google.visualization.DataTable();
              data.addColumn('string', '');
              data.addColumn('number', 'Anzahl');


              for (var i = 0; i < jsonData.length; i++) {
                anzahl = parseInt(jsonData[i].Anzahl)
                data.addRows([
                    [jsonData[i].Status, anzahl]
                  ]);
            }  

            var options = {
                legend: {position: 'none'},
                series: {
                  0: { axis: 'Anzahl' }, // Bind series 0 to an axis named 'distance'.
                },
                axes: {
                  y: {
                    Anzahl: {label: ''}, // Left y-axis.
                  }
                }
              };
            
            var chart = new google.charts.Bar(this.$refs.barchartstatus);
 
            chart.draw(data, google.charts.Bar.convertOptions(options));
        },
        getData_LZ() {
            axios.get(api_LZ)
                .then(response => {
                    this.data = response.data
                    this.drawChart_LZ()
                })
        },
        drawChart_LZ() {

            jsonData = this.data
            document.getElementById("lieferzeit_d").innerHTML = jsonData[0].d;
            document.getElementById("lieferzeit_h").innerHTML = jsonData[0].h;;
            document.getElementById("lieferzeit_m").innerHTML = jsonData[0].m;;
            document.getElementById("lieferzeit_s").innerHTML = jsonData[0].s;;


        }, 

        getRealtimeData() {
            this.realtime = true
            this.intervall_BL = setInterval(() => this.getData_BL(), 2000);
            this.intervall_BT = setInterval(() => this.getData_BT(), 2000);
            this.intervall_UB = setInterval(() => this.getData_UB(), 2000);
            this.intervall_MG = setInterval(() => this.getData_MG(), 2000);
            this.intervall_LW = setInterval(() => this.getData_LW(), 2000);
            this.intervall_BS = setInterval(() => this.getData_BS(), 2000);
        },
        stopRealtimeData() {
            this.realtime = false
            clearInterval(this.interval);
        }



    },
    watch: {
    }
})

const bestellungen = app.component("bestellungen")

app.component('produktion', {
    template: `
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Dashboard - Produktion</h1>
    <div v-show="realtime">
    <button class="btn btn-primary" type="button" disabled>Daten werden geladen
  <span class="spinner-border spinner-border-sm" role="status"></span>
  <span class="sr-only"></span>
</button>
</div>
    </div>

    <div class="row">
      <div class="col">
      <p class="fs-5 fw-light text-secondary my-3">Aktuelle Durchlaufzeit</p><br>
      <div class="container">
      <div class="row">
        <div class="col-sm text-center">
         <span class="border p-3 fs-5 rounded" id="durchlaufzeit_d"></span><br><br>Tage
        </div>
        <div class="col-sm text-center">
         <span class="border p-3 fs-5 rounded" id="durchlaufzeit_h"></span><br><br>Stunden
        </div>
        <div class="col-sm text-center">
         <span class="border p-3 fs-5 rounded" id="durchlaufzeit_m"></span><br><br>Minuten
        </div>
        <div class="col-sm text-center">
         <span class="border p-3 fs-5 rounded" id="durchlaufzeit_s"></span><br><br>Sekunden
        </div>
      </div>
    </div>
    <hr>
    <p class="fs-5 fw-light text-secondary my-3">Lagerübersicht</p>

<div class="container">
  <div class="row">
    <div class="col-md-auto">
    <div class="card" style="width: 13rem;">
    <div class="card-header">
      Rohstoffe
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item fw-bolder"><img src="../assets/img/hashtag.svg" width="18"> <span id="menge1"></span> Stk.</li>
      <li class="list-group-item fw-bolder"><img src="../assets/img/euro.svg" width="18"> <span id="wert1"></span> €</li>
    </ul>
  </div>
    </div>
    <div class="col-md-auto">
    <div class="card" style="width: 13rem;">
    <div class="card-header">
      Unfertige Erzeugnisse
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item fw-bolder"><img src="../assets/img/hashtag.svg" width="18"> <span id="menge2"></span> Stk.</li>
      <li class="list-group-item fw-bolder"><img src="../assets/img/euro.svg" width="18"> <span id="wert2"></span> €</li>
    </ul>
  </div>
    </div>
    <div class="col-md-auto">
    <div class="card" style="width: 13rem;">
    <div class="card-header">
      Fertige Erzeugnisse
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item fw-bolder"><img src="../assets/img/hashtag.svg" width="18"> <span id="menge3"></span> Stk.</li>
      <li class="list-group-item fw-bolder"><img src="../assets/img/euro.svg" width="18"> <span id="wert3"></span> €</li>
    </ul>
  </div>
    </div>
  </div>
  </div>

      </div>



      <div class="col">
      <p class="fs-5 fw-light text-secondary my-3">Produktionsübersicht</p>
      <div id="produktion_status" ref="produktion_status" style="width: 700px; height: 300px;"></div>
      </div>
      
    </div>
<hr>
<p class="fs-5 fw-light text-secondary my-3">Auslastung</p>

<div class="row">
  <div class="col">
    <div id="MaschineNutzung1" ref="MaschineNutzung1" style="width: 400px; height: 200px;"></div>
    </div>
    <div class="col">
    <div id="MaschineNutzung2" ref="MaschineNutzung2" style="width: 400px; height: 200px;"></div>
    </div>
    <div class="col">
    <div id="MaschineNutzung3" ref="MaschineNutzung3" style="width: 400px; height: 200px;"></div>
    </div>
    <div class="col">
    <div id="MaschineNutzung4" ref="MaschineNutzung4" style="width: 400px; height: 200px;"></div>
    </div>
  </div>

  <hr>
  <p class="fs-5 fw-light text-secondary my-3">Produktivität</p>
  
  <div class="row">
    <div class="col">
      <div id="MaschineLeistung1" ref="MaschineLeistung1" style="width: 400px; height: 200px;"></div>
      </div>
      <div class="col">
      <div id="MaschineLeistung2" ref="MaschineLeistung2" style="width: 400px; height: 200px;"></div>
      </div>
      <div class="col">
      <div id="MaschineLeistung3" ref="MaschineLeistung3" style="width: 400px; height: 200px;"></div>
      </div>
      <div class="col">
      <div id="MaschineLeistung4" ref="MaschineLeistung4" style="width: 400px; height: 200px;"></div>
      </div>
    </div>
 <hr>
 <p class="fs-5 fw-light text-secondary my-3">Statusverlauf</p>
 <div class="row">
 <div class="col">
 <span class="fs-6 fw-light text-secondary">Maschine 1</span>
 <div id="MaschineStatus1" ref="MaschineStatus1" style="width: 400px; height: 200px;" class="mt-3"></div>
   </div>
   <div class="col">
   <span class="fs-6 fw-light text-secondary">Maschine 2</span>
   <div id="MaschineStatus2" ref="MaschineStatus2" style="width: 400px; height: 200px;" class="mt-3"></div>
   </div>
   <div class="col">
   <span class="fs-6 fw-light text-secondary">Maschine 3</span>
   <div id="MaschineStatus3" ref="MaschineStatus3" style="width: 400px; height: 200px;" class="mt-3"></div>
   </div>
   <div class="col">
   <span class="fs-6 fw-light text-secondary">Maschine 4</span>
   <div id="MaschineStatus4" ref="MaschineStatus4" style="width: 400px; height: 200px;" class="mt-3"></div>
   </div>
 </div>
 <hr>
 <p class="fw-light">&copy; by Levent Lukas & Jan Warwas</p>
    `,
    data: function () {
        return {
            data: [],
            realtime: false,
            intervall: 0,
            intervall_PS: 0,
            intervall_DLZ: 0,
            intervall_LB: 0,
            intervall_MN1: 0,
            intervall_MN2: 0,
            intervall_MN3: 0,
            intervall_MN4: 0,
            intervall_ML1: 0,
            intervall_ML2: 0,
            intervall_ML3: 0,
            intervall_ML4: 0,
            intervall_MS1: 0,
            intervall_MS2: 0,
            intervall_MS3: 0,
            intervall_MS4: 0
        }
    },
    mounted() {
        this.getData()
        this.getData_PS()
        this.getData_DLZ()
        this.getData_LB()
        this.getData_MN1()
        this.getData_MN2()
        this.getData_MN3()
        this.getData_MN4()
        this.getData_ML1()
        this.getData_ML2()
        this.getData_ML3()
        this.getData_ML4()
        this.getData_MS1()
        this.getData_MS2()
        this.getData_MS3()
        this.getData_MS4()
        google.charts.setOnLoadCallback(() => this.drawChart())
        google.charts.setOnLoadCallback(() => this.drawChart_PS())
        google.charts.setOnLoadCallback(() => this.drawChart_MN1())
        google.charts.setOnLoadCallback(() => this.drawChart_MN2())
        google.charts.setOnLoadCallback(() => this.drawChart_MN3())
        google.charts.setOnLoadCallback(() => this.drawChart_MN4())
        google.charts.setOnLoadCallback(() => this.drawChart_ML1())
        google.charts.setOnLoadCallback(() => this.drawChart_ML2())
        google.charts.setOnLoadCallback(() => this.drawChart_ML3())
        google.charts.setOnLoadCallback(() => this.drawChart_ML4())
        google.charts.setOnLoadCallback(() => this.drawChart_MS1())
        google.charts.setOnLoadCallback(() => this.drawChart_MS2())
        google.charts.setOnLoadCallback(() => this.drawChart_MS3())
        google.charts.setOnLoadCallback(() => this.drawChart_MS4())
        this.getRealtimeData()
    },
    methods: {
        getData() {
            axios.get(api_test)
                .then(response => {
                    this.data = response.data
                    this.drawChart()
                })
        },
        drawChart() {

            jsonData = this.data

            var data = new google.visualization.DataTable();

            data.addColumn('string', 'Typ');
            data.addColumn('number', 'Anzahl');

            for (var i = 0; i < jsonData.length; i++) {
                anzahl = parseInt(jsonData[i].Anzahl)
                data.addRows([jsonData[i].Typ, anzahl]);
            }

            var options = {
                title: 'Bestellte Modelle'
            };

            var chart = new google.visualization.PieChart(this.$refs.piechart);

            chart.draw(data, options);
        },

        getData_PS() {
            axios.get(api_PS)
                .then(response => {
                    this.data = response.data
                    this.drawChart_PS()
                })
        },
        drawChart_PS() {

            jsonData = this.data

            var data = new google.visualization.DataTable();
              data.addColumn('string', '');
              data.addColumn('number', 'Anzahl');


              for (var i = 0; i < jsonData.length; i++) {
                anzahl = parseInt(jsonData[i].Anzahl)
                data.addRows([
                    [jsonData[i].Status, anzahl]
                  ]);
            }  

            var options = {
                legend: {position: 'none'},
                series: {
                  0: { axis: 'Anzahl' }, // Bind series 0 to an axis named 'distance'.
                },

              };
            
            var chart = new google.charts.Bar(this.$refs.produktion_status);
 
            chart.draw(data, google.charts.Bar.convertOptions(options));
        },

        getData_DLZ() {
            axios.get(api_DLZ)
                .then(response => {
                    this.data = response.data
                    this.drawChart_DLZ()
                })
        },
        drawChart_DLZ() {

            jsonData = this.data
            document.getElementById("durchlaufzeit_d").innerHTML = jsonData[0].d;
            document.getElementById("durchlaufzeit_h").innerHTML = jsonData[0].h;
            document.getElementById("durchlaufzeit_m").innerHTML = jsonData[0].m;
            document.getElementById("durchlaufzeit_s").innerHTML = jsonData[0].s;


        }, 
        getData_LB() {
            axios.get(api_LB)
                .then(response => {
                    this.data = response.data
                    this.drawChart_LB()
                })
        },
        drawChart_LB() {

            jsonData = this.data
            document.getElementById("wert1").innerHTML = jsonData[0].Wert;
            document.getElementById("menge1").innerHTML = jsonData[0].Menge;
            document.getElementById("wert2").innerHTML = jsonData[1].Wert;
            document.getElementById("menge2").innerHTML = jsonData[1].Menge;
            document.getElementById("wert3").innerHTML = jsonData[2].Wert;
            document.getElementById("menge3").innerHTML = jsonData[2].Menge;


        }, 
        getData_MN1() {
            axios.get(api_MN1)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MN1()
                })
        },
        drawChart_MN1() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', '');

            for (var i = 0; i < jsonData.length; i++) {
                auslastung = parseInt(jsonData[i].Auslastung);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], auslastung]
                ]);
            }  

            var options = {
                chart: {
                    title: 'Maschine 1',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };
            var chart = new google.charts.Line(this.$refs.MaschineNutzung1);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_MN2() {
            axios.get(api_MN2)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MN2()
                })
        },
        drawChart_MN2() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', 'Auslastung');

            for (var i = 0; i < jsonData.length; i++) {
                auslastung = parseInt(jsonData[i].Auslastung);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], auslastung]
                ]);
            }  

            var options = {
                chart: {
                    title: 'Maschine 2',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.MaschineNutzung2);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_MN3() {
            axios.get(api_MN3)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MN3()
                })
        },
        drawChart_MN3() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', 'Auslastung');

            for (var i = 0; i < jsonData.length; i++) {
                auslastung = parseInt(jsonData[i].Auslastung);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], auslastung]
                ]);
            }  

            var options = {
                chart: {
                    title: 'Maschine 3',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.MaschineNutzung3);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_MN4() {
            axios.get(api_MN4)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MN4()
                })
        },
        drawChart_MN4() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', 'Auslastung');

            for (var i = 0; i < jsonData.length; i++) {
                auslastung = parseInt(jsonData[i].Auslastung);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], auslastung]
                ]);
            }  
            var options = {
                chart: {
                    title: 'Maschine 4',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.MaschineNutzung4);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_ML1() {
            axios.get(api_ML1)
                .then(response => {
                    this.data = response.data
                    this.drawChart_ML1()
                })
        },
        drawChart_ML1() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', 'Produktivität');

            for (var i = 0; i < jsonData.length; i++) {
                prod = parseInt(jsonData[i].Produktivitaet);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], prod]
                ]);
            }  

            var options = {
                chart: {
                    title: 'Maschine 1',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.MaschineLeistung1);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_ML2() {
            axios.get(api_ML2)
                .then(response => {
                    this.data = response.data
                    this.drawChart_ML2()
                })
        },
        drawChart_ML2() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', 'Produktivität');

            for (var i = 0; i < jsonData.length; i++) {
                prod = parseInt(jsonData[i].Produktivitaet);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], prod]
                ]);
            }  

            var options = {
                chart: {
                    title: 'Maschine 2',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.MaschineLeistung2);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_ML3() {
            axios.get(api_ML3)
                .then(response => {
                    this.data = response.data
                    this.drawChart_ML3()
                })
        },
        drawChart_ML3() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', 'Produktivität');

            for (var i = 0; i < jsonData.length; i++) {
                prod = parseInt(jsonData[i].Produktivitaet);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], prod]
                ]);
            }  

            var options = {
                chart: {
                    title: 'Maschine 3',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.MaschineLeistung3);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_ML4() {
            axios.get(api_ML4)
                .then(response => {
                    this.data = response.data
                    this.drawChart_ML4()
                })
        },
        drawChart_ML4() {

            jsonData = this.data
            var data = new google.visualization.DataTable();


            data.addColumn('timeofday', '');
            data.addColumn('number', 'Produktivität');

            for (var i = 0; i < jsonData.length; i++) {
                prod = parseInt(jsonData[i].Produktivitaet);
                std = parseInt(jsonData[i].stunde);
                min = parseInt(jsonData[i].minute);
                data.addRows([
                    [[std-1, min, 0], prod]
                ]);
            }  

            var options = {
                chart: {
                    title: 'Maschine 4',
                  },
                legend: { position: 'none' },
                vAxis: {
                    viewWindow: {
                      max:100,
                      min:0
                    }
                },
              };

            var chart = new google.charts.Line(this.$refs.MaschineLeistung4);

            chart.draw(data, google.charts.Line.convertOptions(options));
        },
        getData_MS1() {
            axios.get(api_MS1)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MS1()
                })
        },
        drawChart_MS1() {

            jsonData = this.data
            var data = new google.visualization.DataTable();

            data.addColumn({ type: 'string', id: 'Status' });
            data.addColumn({ type: 'string', id: 'X' });
            data.addColumn({ type: 'date', id: 'Start' });
            data.addColumn({ type: 'date', id: 'End' });

            for (var i = 0; i < jsonData.length; i++) {
                startH = parseInt(jsonData[i].stunde);
                endH = parseInt(jsonData[i].stunde);
                startM = parseInt(jsonData[i].minute);
                endM = parseInt(jsonData[i].minute);
                status_str = ''
                if(parseInt(jsonData[i].Produktivitaet) == 0){
                    status_str = 'Gestoppt';
                }else if(parseInt(jsonData[i].Produktivitaet) > 0 && parseInt(jsonData[i].Produktivitaet) < 100){
                    status_str = 'Warnung';
                }else if(parseInt(jsonData[i].Produktivitaet) == 100){
                    status_str = 'Normal';
                }
                data.addRows([
                    [ 'Status', status_str, new Date(0,0,0,startH,startM,0), new Date(0,0,0,endH,endM,0) ]
                ]);
            }   


            var options = {
                chart: {
                    title: 'Maschine 1',
                  },
                timeline: { showRowLabels: false },
                colors: ['#dc3545', '#198754', '#ffc107'],
              };

            var chart = new google.visualization.Timeline(this.$refs.MaschineStatus1);

            chart.draw(data, options);
        },
        getData_MS2() {
            axios.get(api_MS2)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MS2()
                })
        },
        drawChart_MS2() {

          jsonData = this.data
          var data = new google.visualization.DataTable();

          data.addColumn({ type: 'string', id: 'Status' });
          data.addColumn({ type: 'string', id: 'X' });
          data.addColumn({ type: 'date', id: 'Start' });
          data.addColumn({ type: 'date', id: 'End' });

          for (var i = 0; i < jsonData.length; i++) {
              startH = parseInt(jsonData[i].stunde);
              endH = parseInt(jsonData[i].stunde);
              startM = parseInt(jsonData[i].minute);
              endM = parseInt(jsonData[i].minute);
              status_str = ''
              if(parseInt(jsonData[i].Produktivitaet) == 0){
                  status_str = 'Gestoppt';
              }else if(parseInt(jsonData[i].Produktivitaet) > 0 && parseInt(jsonData[i].Produktivitaet) < 100){
                  status_str = 'Warnung';
              }else if(parseInt(jsonData[i].Produktivitaet) == 100){
                  status_str = 'Normal';
              }
              data.addRows([
                  [ 'Status', status_str, new Date(0,0,0,startH,startM,0), new Date(0,0,0,endH,endM,0) ]
              ]);
          }   


          var options = {
              chart: {
                  title: 'Maschine 2',
                },
              timeline: { showRowLabels: false },
              colors: ['#dc3545', '#198754', '#ffc107'],
            };

          var chart = new google.visualization.Timeline(this.$refs.MaschineStatus2);

          chart.draw(data, options);
      },
        getData_MS3() {
            axios.get(api_MS3)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MS3()
                })
        },
        drawChart_MS3() {

          jsonData = this.data
          var data = new google.visualization.DataTable();

          data.addColumn({ type: 'string', id: 'Status' });
          data.addColumn({ type: 'string', id: 'X' });
          data.addColumn({ type: 'date', id: 'Start' });
          data.addColumn({ type: 'date', id: 'End' });

          for (var i = 0; i < jsonData.length; i++) {
              startH = parseInt(jsonData[i].stunde);
              endH = parseInt(jsonData[i].stunde);
              startM = parseInt(jsonData[i].minute);
              endM = parseInt(jsonData[i].minute);
              status_str = ''
              if(parseInt(jsonData[i].Produktivitaet) == 0){
                  status_str = 'Gestoppt';
              }else if(parseInt(jsonData[i].Produktivitaet) > 0 && parseInt(jsonData[i].Produktivitaet) < 100){
                  status_str = 'Warnung';
              }else if(parseInt(jsonData[i].Produktivitaet) == 100){
                  status_str = 'Normal';
              }
              data.addRows([
                  [ 'Status', status_str, new Date(0,0,0,startH,startM,0), new Date(0,0,0,endH,endM,0) ]
              ]);
          }   


          var options = {
              chart: {
                  title: 'Maschine 3',
                },
              timeline: { showRowLabels: false },
              colors: ['#dc3545', '#198754', '#ffc107'],
            };

          var chart = new google.visualization.Timeline(this.$refs.MaschineStatus3);

          chart.draw(data, options);
      },
        getData_MS4() {
            axios.get(api_MS4)
                .then(response => {
                    this.data = response.data
                    this.drawChart_MS4()
                })
        },
        drawChart_MS4() {

          jsonData = this.data
          var data = new google.visualization.DataTable();

          data.addColumn({ type: 'string', id: 'Status' });
          data.addColumn({ type: 'string', id: 'X' });
          data.addColumn({ type: 'date', id: 'Start' });
          data.addColumn({ type: 'date', id: 'End' });

          for (var i = 0; i < jsonData.length; i++) {
              startH = parseInt(jsonData[i].stunde);
              endH = parseInt(jsonData[i].stunde);
              startM = parseInt(jsonData[i].minute);
              endM = parseInt(jsonData[i].minute);
              status_str = ''
              if(parseInt(jsonData[i].Produktivitaet) == 0){
                  status_str = 'Gestoppt';
              }else if(parseInt(jsonData[i].Produktivitaet) > 0 && parseInt(jsonData[i].Produktivitaet) < 100){
                  status_str = 'Warnung';
              }else if(parseInt(jsonData[i].Produktivitaet) == 100){
                  status_str = 'Normal';
              }
              data.addRows([
                  [ 'Status', status_str, new Date(0,0,0,startH,startM,0), new Date(0,0,0,endH,endM,0) ]
              ]);
          }   


          var options = {
              chart: {
                  title: 'Maschine 4',
                },
              timeline: { showRowLabels: false },
              colors: ['#dc3545', '#198754', '#ffc107'],
            };

          var chart = new google.visualization.Timeline(this.$refs.MaschineStatus4);

          chart.draw(data, options);
      },
        getRealtimeData() {
            this.realtime = true
            this.interval = setInterval(() => this.getData(), 2000);
            this.interval_PS = setInterval(() => this.getData_PS(), 2000);
            this.interval_DLZ = setInterval(() => this.getData_DLZ(), 2000);
            this.interval_LB = setInterval(() => this.getData_LB(), 2000);
            this.interval_MN1 = setInterval(() => this.getData_MN1(), 2000);
            this.interval_MN2 = setInterval(() => this.getData_MN2(), 2000);
            this.interval_MN3 = setInterval(() => this.getData_MN3(), 2000);
            this.interval_MN4 = setInterval(() => this.getData_MN4(), 2000);
            this.interval_MN1 = setInterval(() => this.getData_ML1(), 2000);
            this.interval_MN2 = setInterval(() => this.getData_ML2(), 2000);
            this.interval_MN3 = setInterval(() => this.getData_ML3(), 2000);
            this.interval_MN4 = setInterval(() => this.getData_ML4(), 2000);
            this.interval_MS1 = setInterval(() => this.getData_MS1(), 2000);
            this.interval_MS2 = setInterval(() => this.getData_MS2(), 2000);
            this.interval_MS3 = setInterval(() => this.getData_MS3(), 2000);
            this.interval_MS4 = setInterval(() => this.getData_MS4(), 2000);
        },
        stopRealtimeData() {
            this.realtime = false
            clearInterval(this.interval);
        }

    },
    watch: {
    }
})

const produktion = app.component("produktion")


var routes = [

    {
        path: "/bestellungen",
        components: {
            view: bestellungen
        }
    },
    {
        path: "/produktion",
        components: {
            view: produktion
        }
    },
    {
        path: "/",
        components: {
            view: bestellungen
        }
    }



]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: routes
})



app.use(router)
app.mount("#app")