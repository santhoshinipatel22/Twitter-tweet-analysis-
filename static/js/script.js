document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);

    fetch('/analyze', {
        method: 'POST',
        body: data
    })
    .then(res => res.json())
    .then(json => {
        document.getElementById('total').innerText = 'Total tweets analyzed: ' + json.total;
        const stats = json.stats;
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(stats),
                datasets: [{
                    data: Object.values(stats),
                    backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
                }]
            }
        });

        // render trend graph if available
        if (json.trend) {
            const trendCtx = document.getElementById('trendChart').getContext('2d');
            const labels = Object.keys(json.trend).sort();
            const sentiments = Object.keys(stats);
            const datasets = sentiments.map((s, idx) => ({
                label: s,
                data: labels.map(d => json.trend[d] ? json.trend[d][s] || 0 : 0),
                borderColor: ['#36A2EB', '#FF6384', '#FFCE56'][idx],
                fill: false
            }));
            new Chart(trendCtx, {
                type: 'line',
                data: { labels, datasets }
            });
        }
        // show word cloud image
        if (json.wordcloud) {
            const wcDiv = document.getElementById('wordcloud');
            wcDiv.innerHTML = '<h4>Word Cloud</h4><img src="data:image/png;base64,' + json.wordcloud + '" alt="Word Cloud" />';
        }

        if (json.records && json.records.length > 0) {
            // add download button
            let downloadBtn = document.getElementById('download-btn');
            if (!downloadBtn) {
                downloadBtn = document.createElement('button');
                downloadBtn.id = 'download-btn';
                downloadBtn.textContent = 'Download CSV';
                downloadBtn.addEventListener('click', () => {
                    const headers = ['tweet', 'sentiment', 'date'];
                    const rows = json.records.map(r => headers.map(h => '"' + (r[h] || '').replace(/"/g, '""') + '"').join(','));
                    const csv = headers.join(',') + '\n' + rows.join('\n');
                    const blob = new Blob([csv], { type: 'text/csv' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'tweets.csv';
                    a.click();
                });
                document.getElementById('results').appendChild(downloadBtn);
            }
        }
    })
    .catch(err => console.error(err));
});
