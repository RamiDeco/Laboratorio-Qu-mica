document.addEventListener('DOMContentLoaded', function() {
    // Configuración inicial del gráfico
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    const temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperatura',
                data: [],
                borderColor: 'rgba(750, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: true,
                        text: 'Tiempo'
                    },
                    ticks: {
                        autoSkip: true, // Habilita el autoSkip para reducir la cantidad de etiquetas
                        maxTicksLimit: 10 // Limita el número máximo de etiquetas a mostrar
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Temperatura (°C)'
                    }
                }
            }
        }
    });

    // Función para actualizar el gráfico con los nuevos datos
    function updateChart() {
        fetch('http://192.168.100.247:3000/data')
            .then(response => response.json())
            .then(data => {
                const now = new Date();
                temperatureChart.data.labels.push(now);
                temperatureChart.data.datasets[0].data.push({ x: now, y: data.value });
                temperatureChart.update();
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
            });
    }

    // Actualizar el gráfico cada 5 segundos
    setInterval(updateChart, 15000);

    // Actualizar el gráfico inmediatamente al cargar la página
    updateChart();
});