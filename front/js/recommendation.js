async function getRecommendations() {
    const producto = document.getElementById("productoInput").value;

    const res = await fetch(`${API_URL}/recommend/similarity/${producto}`);
    const data = await res.json();

    const list = document.getElementById("recommendList");
    list.innerHTML = "";

    for (let key in data) {
        const li = `<li>${key} → score: ${data[key]}</li>`;
        list.innerHTML += li;
    }
}