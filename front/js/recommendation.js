async function getRecommendations() {
    const method = document.getElementById('recommendMethod').value;
    const topN = parseInt(document.getElementById('topN').value) || 5;
    const producto = document.getElementById('productoInput').value;
    const cliente = document.getElementById('clienteInput').value;

    const list = document.getElementById('recommendList');
    list.innerHTML = '';

    try {
        let res, data;
        if (method === 'collaborative') {
            if (!cliente) { alert('Introduce un ClienteKey para colaborativo'); return; }
            res = await fetch(`${API_URL}/recommend/collaborative/${cliente}?n=${topN}`);
            data = await res.json();
            if (data.error) { list.innerHTML = `<li>${data.error}</li>`; return; }
            for (const [p, score] of Object.entries(data)) {
                list.innerHTML += `<li>${p} — score: ${score.toFixed(3)}</li>`;
            }
        } else if (method === 'inventory_similarity') {
            if (!producto) { alert('Introduce el nombre o key del producto'); return; }
            res = await fetch(`${API_URL}/recommend/inventory/similarity/${encodeURIComponent(producto)}?n=${topN}`);
            data = await res.json();
            if (data.error) { list.innerHTML = `<li>${data.error}</li>`; return; }
            const recs = data.recommendations || [];
            if (recs.length === 0) list.innerHTML = '<li>No hay recomendaciones</li>';
            recs.forEach(r => {
                list.innerHTML += `<li>${r.producto} — score: ${r.score.toFixed(3)} — ${r.interpretation}</li>`;
            });
        } else if (method === 'content') {
            if (!producto) { alert('Introduce el nombre del producto'); return; }
            res = await fetch(`${API_URL}/recommend/content/${encodeURIComponent(producto)}?n=${topN}`);
            data = await res.json();
            if (data.error) { list.innerHTML = `<li>${data.error}</li>`; return; }
            const recs = data.recommendations || [];
            recs.forEach(r => {
                list.innerHTML += `<li>${r.producto} — score: ${r.score.toFixed(3)}</li>`;
            });
        } else {
            // similarity (existing)
            if (!producto) { alert('Introduce el nombre del producto'); return; }
            res = await fetch(`${API_URL}/recommend/similarity/${encodeURIComponent(producto)}`);
            data = await res.json();
            for (let key in data) {
                list.innerHTML += `<li>${key} → score: ${data[key]}</li>`;
            }
        }
    } catch (e) {
        console.error(e);
        list.innerHTML = `<li>Error llamando API: ${e.message}</li>`;
    }
}