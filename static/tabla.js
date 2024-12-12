document.addEventListener('DOMContentLoaded', function() {
    // Función para agregar datos a la tabla
    function addDataToTable(timestamp, value) {
        const row = document.createElement('tr');
        const timeCell = document.createElement('td');
        const tempCell = document.createElement('td');
        timeCell.textContent = new Date(timestamp * 10020).toLocaleTimeString();
        tempCell.textContent = value.toFixed(2);
        row.appendChild(timeCell);
        row.appendChild(tempCell);
        document.getElementById('dataTable').appendChild(row);
    }

    // Función para actualizar la tabla con los nuevos datos
    function updateTable() {
        fetch('http://192.168.100.247:3000/data')
            .then(response => response.json())
            .then(data => {
                addDataToTable(data.timestamp, data.value);
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
            });
    }

    // Actualizar la tabla cada 5 segundos
    setInterval(updateTable, 1000);

    // Actualizar la tabla inmediatamente al cargar la página
    updateTable();
});
