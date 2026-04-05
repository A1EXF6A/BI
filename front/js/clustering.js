async function loadClusters() {
    console.log('loadClusters() start');
    const tableSelector = document.getElementById('factTable');
    const table = tableSelector.value.toLowerCase();
    const k = 3; // use default k
    // sample: default 500, can be overridden by user input
    const sampleEl = document.getElementById('clusterSample');
    let sample = 500;
    if (sampleEl) {
        const v = parseInt(sampleEl.value);
        if (!isNaN(v) && v > 0) sample = v;
        else sample = 0;
    }

    // Ensure clusters section is visible
    try {
        const sec = document.getElementById('clusters');
        if (sec && sec.classList.contains('hidden')) sec.classList.remove('hidden');
    } catch (e) {
        console.warn('Could not reveal clusters section:', e);
    }

    const res = await fetch(`${API_URL}/clusters/${table}?k=${k}&sample=${sample}`);
    if (!res.ok) {
        const txt = await res.text();
        alert(`Error obteniendo clusters: ${res.status} ${txt}`);
        return;
    }
    const data = await res.json();
    console.log('clusters response:', data);

    const records = data.records || [];
    const summaries = data.summaries || {};
    const counts = data.counts || {};

    if ((!records || records.length === 0) && (!summaries || Object.keys(summaries).length === 0)) {
        const clustersResult = document.getElementById('clustersResult');
        if (clustersResult) clustersResult.innerHTML = '<p>No hay datos para mostrar</p>';
        console.warn('No records or summaries returned from clusters endpoint');
        return;
    }

    // determine feature keys (use summaries or derive from records)
    let featureKeys = Object.keys(summaries[Object.keys(summaries)[0]] || {});
    if (!featureKeys || featureKeys.length === 0) {
        const first = records[0] || {};
        featureKeys = Object.keys(first).filter(k => typeof first[k] === 'number');
    }
    console.log('featureKeys:', featureKeys);

    // show textual summary (counts + interpretation) similar to metrics
    // scroll into view so user sees the results
    try {
        const sec = document.getElementById('clusters');
        if (sec) sec.scrollIntoView({ behavior: 'smooth' });
    } catch (e) {}
    // build legend (colored swatches + interpretation + counts)
    const clustersLegend = document.getElementById('clustersLegend');
    const clustersResultDiv = document.getElementById('clustersResult');
    if (clustersLegend && clustersResultDiv) {
        const clusterKeys = Object.keys(summaries);
        clustersLegend.innerHTML = '';
        clustersResultDiv.innerHTML = `<h3>Clusters (${clusterKeys.length})</h3>`;
        clusterKeys.forEach((c, idx) => {
            const interp = (data.interpretations && data.interpretations[c]) || '';
            const cnt = counts[c] || 0;
            const color = `hsl(${(idx*60)%360} 70% 50% / 0.8)`;
            const itemHtml = `
                <div class="cluster-legend-item" style="display:flex;align-items:center;margin:6px 0;">
                    <div style="width:18px;height:18px;background:${color};border-radius:4px;margin-right:8px"></div>
                    <div><strong>Cluster ${c}</strong>: ${interp} — ${cnt} items</div>
                </div>
            `;
            clustersLegend.innerHTML += itemHtml;
        });
    }

    // store records globally (sample) but render analytics only from summaries/counts
    window.clusterRecords = records;
    // Build analytics-only charts from summaries and counts (do NOT use records)
    drawClusterAnalytics(summaries, counts, data.interpretations || {});
}

function drawClusterAnalytics(summaries, counts, interpretations) {
    // summaries: { cluster: {feature: mean, ...}, ... }
    const clusterKeys = Object.keys(summaries).sort((a,b)=>Number(a)-Number(b));
    if (clusterKeys.length === 0) {
        const clustersResult = document.getElementById('clustersResult');
        if (clustersResult) clustersResult.innerHTML = '<p>No hay datos de resumen para mostrar</p>';
        return;
    }

    // determine feature order from first summary
    const featureKeys = Object.keys(summaries[clusterKeys[0]] || []);
    const colors = clusterKeys.map((_, idx) => `hsl(${(idx*60)%360} 70% 50% / 0.8)`);
    const borderColors = clusterKeys.map((_, idx) => `hsl(${(idx*60)%360} 70% 40% / 1)`);

    // Radar chart (profile per cluster)
    const radarEl = document.getElementById('clustersRadar');
    if (radarEl) {
        const ctx = radarEl.getContext('2d');
        if (window.clusterRadar) try { window.clusterRadar.destroy(); } catch(_){}
        const datasets = clusterKeys.map((c, idx) => ({
            label: `Cluster ${c}`,
            data: featureKeys.map(f => summaries[c][f] != null ? summaries[c][f] : 0),
            fill: true,
            backgroundColor: colors[idx],
            borderColor: borderColors[idx],
            pointBackgroundColor: borderColors[idx]
        }));
        window.clusterRadar = new Chart(ctx, {
            type: 'radar',
            data: { labels: featureKeys, datasets },
            options: { responsive:true, maintainAspectRatio:false, plugins:{ legend:{ position:'top' } } }
        });
    }

    // Grouped bar comparison per metric
    const barEl = document.getElementById('clustersBarCompare');
    if (barEl) {
        const ctx = barEl.getContext('2d');
        if (window.clusterBarCompare) try { window.clusterBarCompare.destroy(); } catch(_){}
        const datasets = clusterKeys.map((c, idx) => ({
            label: `Cluster ${c}`,
            data: featureKeys.map(f => summaries[c][f] != null ? summaries[c][f] : 0),
            backgroundColor: colors[idx],
            borderColor: borderColors[idx],
            borderWidth: 1
        }));
        window.clusterBarCompare = new Chart(ctx, {
            type: 'bar',
            data: { labels: featureKeys, datasets },
            options: { responsive:true, maintainAspectRatio:false, plugins:{ legend:{ position:'top' } }, scales: { x: { stacked: false }, y: { beginAtZero:true } } }
        });
    }

    // Distribution (counts)
    const distEl = document.getElementById('clustersDistribution');
    if (distEl) {
        const ctx = distEl.getContext('2d');
        if (window.clusterDist) try { window.clusterDist.destroy(); } catch(_){}
        const labels = clusterKeys.map(c => `Cluster ${c}`);
        const dataVals = clusterKeys.map(c => counts[c] || 0);
        const distColors = clusterKeys.map((_, idx) => `hsl(${(idx*60)%360} 70% 50% / 0.9)`);
        window.clusterDist = new Chart(ctx, {
            type: 'pie',
            data: { labels, datasets: [{ data: dataVals, backgroundColor: distColors }] },
            options: { responsive:true, maintainAspectRatio:false, plugins:{ legend:{ position:'bottom' } } }
        });
    }

    // Interpretations summary
    const clustersResult = document.getElementById('clustersResult');
    if (clustersResult) {
        clustersResult.innerHTML = `<h3>Clusters (${clusterKeys.length})</h3>`;
        clusterKeys.forEach((c, idx) => {
            const interp = interpretations[c] || interpretations[Number(c)] || '';
            const cnt = counts[c] || 0;
            clustersResult.innerHTML += `<div style="margin:6px 0; display:flex; gap:8px; align-items:center;"><div style="width:12px;height:12px;background:${colors[idx]};border-radius:3px"></div><div><strong>Cluster ${c}</strong>: ${interp} — ${cnt} items</div></div>`;
        });
    }
}