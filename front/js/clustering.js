async function loadClusters() {
    const res = await fetch(`${API_URL}/clusters`);
    const data = await res.json();

    const tbody = document.querySelector("#clustersTable tbody");
    tbody.innerHTML = "";

    data.forEach(item => {
        const row = `
            <tr>
                <td>${item["Producto.NombreProducto"]}</td>
                <td>${item.cluster}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}