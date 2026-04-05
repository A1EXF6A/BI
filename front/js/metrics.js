async function loadMetrics() {
    const res = await fetch(`${API_URL}/metrics/ventas`);
    const data = await res.json();

    const div = document.getElementById("metricsResult");

    div.innerHTML = `
        <p><b>Total Ventas:</b> ${data.total_ventas}</p>
        <p><b>Promedio Venta:</b> ${data.promedio_venta}</p>
        <p><b>Total Margen:</b> ${data.total_margen}</p>
    `;
}