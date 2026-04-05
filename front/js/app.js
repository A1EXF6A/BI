function showSection(sectionId) {
    const sections = document.querySelectorAll(".section");

    sections.forEach(sec => sec.classList.add("hidden"));

    document.getElementById(sectionId).classList.remove("hidden");
}

async function loadMetrics() {
    const tableSelector = document.getElementById("factTable");
    const selectedTable = tableSelector.value;

    try {
        // pedir métricas ya calculadas al backend
        const response = await fetch(`http://localhost:8000/metrics/${selectedTable.toLowerCase()}`);
        if (!response.ok) {
            const text = await response.text();
            console.error(`Backend returned ${response.status}:`, text);
            alert(`Error al obtener métricas (${response.status}): ${text}`);
            return;
        }
        const data = await response.json();

        const metricsResult = document.getElementById("metricsResult");
        metricsResult.innerHTML = `<h3>Métricas de ${selectedTable}</h3>`;

        if (!data || Object.keys(data).length === 0) {
            metricsResult.innerHTML += `<p>No hay métricas disponibles para esta tabla.</p>`;
            return;
        }

        // Mostrar todas las métricas devueltas por el backend
            const formatKey = k => k.replace(/_/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2');
            const labels = [];
            const values = [];
            for (const [key, value] of Object.entries(data)) {
                labels.push(formatKey(key));
                values.push(typeof value === 'number' ? value : (value === null || value === undefined ? 0 : value));
                metricsResult.innerHTML += `<p>${formatKey(key)}: ${value !== null && value !== undefined ? value : 'N/A'}</p>`;
            }

            // Dibujar gráfico con Chart.js
            const canvas = document.getElementById('metricsChart');
            if (canvas) {
                const ctx = canvas.getContext('2d');
                try {
                    if (window.metricsChart) {
                        if (typeof window.metricsChart.destroy === 'function') {
                            window.metricsChart.destroy();
                        } else {
                            try { window.metricsChart = undefined; } catch(_) { window.metricsChart = null; }
                        }
                    }
                    window.metricsChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Métricas',
                                data: values,
                                backgroundColor: 'rgba(54, 162, 235, 0.6)'
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                y: { beginAtZero: true }
                            }
                        }
                    });
                } catch (e) {
                    console.error('Error creando/actualizando el gráfico:', e);
                }
            }
    } catch (error) {
        console.error("Error al cargar las métricas:", error);
        alert("No se pudieron cargar las métricas. Verifica la conexión con el servidor.");
    }
}