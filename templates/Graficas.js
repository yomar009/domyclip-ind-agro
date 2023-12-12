// chart.js
// Datos de ejemplo
var temperaturesAmbData = [22, 23, 24, 25, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6];
var humidityAmbData = [50, 52, 55, 60, 62, 65, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 90, 88, 85, 82, 80, 78, 75, 72];
var hoursAmbData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];

var humiditySoilData = [50, 52, 55, 60, 62, 65, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 90, 88, 85, 82, 80, 78, 75, 72];
var hoursSoilData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];

//var temperaturesAmbData = {{ temperatures_amb|tojson }};
//var humidityAmbData = {{ humidity_amb|tojson }};
//var hoursAmbData = {{ hours_amb|tojson }};

//var humiditySoilData = {{ humidity_soil|tojson }};
//var hoursSoilData = {{ hours_soil|tojson }};

document.addEventListener('DOMContentLoaded', function () {
    inicializarGraficaAmbiental();
    inicializarGraficaSuelo();
});

// Variables para almacenar las instancias de las gráficas
var graficaAmbiental = inicializarGraficaAmbiental();
var graficaSuelo = inicializarGraficaSuelo();

// Funciones para inicializar las gráficas
function inicializarGraficaAmbiental() {
    var ctx = document.getElementById('grafica-amb').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hoursAmbData,  // Utiliza las horas desde Flask
            datasets: [{
                label: 'Temperatura (°C)',
                data: temperaturesAmbData,  // Utiliza las temperaturas desde Flask
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            },{
                label: 'Humedad (%)',
                data: humidityAmbData,
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 1,   // Mínimo en el eje x
                    max: 24,  // Máximo en el eje x
                    step: 1,   // Paso entre etiquetas
                    title:{
                        display: true,
                        text: 'Horas del dia'
                    }
                },
                y: {
                    beginAtZero: true,
                    title:{
                        display: true,
                        text:'Temperatura y Humedad'
                    }
                }
            },
            plugins:{
                legent:{
                    display: true,
                    position: 'top'
                }
            },
            maintainAspectRatio: false, // Esto permite que el gráfico ocupe todo el tamaño del canvas
            responsive: true // Esto hace que el gráfico sea responsive
        }
    });
}

function inicializarGraficaSuelo() {
    var ctx = document.getElementById('grafica-soil').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hoursSoilData,  // Utiliza las horas desde Flask
            datasets: [{
                label: 'Humedad suelo (%)',
                data: humiditySoilData,  // Utiliza las temperaturas desde Flask
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 1,   // Mínimo en el eje x
                    max: 24,  // Máximo en el eje x
                    step: 1,   // Paso entre etiquetas
                    title:{
                        display: true,
                        text: 'Horas del dia'
                    }
                },
                y: {
                    beginAtZero: true,
                    title:{
                        display: true,
                        text:'Humedad del suelo'
                    }
                }
            },
            plugins:{
                legend:{
                    display: true,
                    position: 'top'
                }
            },
            maintainAspectRatio: false, // Esto permite que el gráfico ocupe todo el tamaño del canvas
            responsive: true // Esto hace que el gráfico sea responsive
        }
    });
}

