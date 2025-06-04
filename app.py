from flask import Flask, render_template_string, jsonify
import threading
import time

app = Flask(__name__)

stakeholder_value = {'value': 0}

def number_go_up():
    while True:
        stakeholder_value['value'] += 1
        time.sleep(1)

# Start background thread to increment value
t = threading.Thread(target=number_go_up, daemon=True)
t.start()

@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head>
        <title>Number Go Up! Maximize Stakeholder Value!</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
        body { font-family:sans-serif; background:#101820; color:#FEE715; }
        .ticker {
            background: #222; color: #FEE715; padding: 10px 0; font-size: 1.3em;
            white-space: nowrap; overflow: hidden; width: 100vw; margin-bottom: 20px;
        }
        .ticker span { display: inline-block; padding: 0 2em; }
        .stock-up { color: #00ff00; }
        .stock-down { color: #ff3333; }
        .stock-neutral { color: #FEE715; }
        </style>
        <script>
        let chart;
        let values = [];
        let labels = [];
        let fakeStocks = [
            {symbol: 'NGU', name: 'NumberGoUp Inc.', price: 1000, change: 0},
            {symbol: 'STKH', name: 'StakeholderMax', price: 420, change: 0},
            {symbol: 'VAL', name: 'Value4U', price: 69, change: 0},
            {symbol: 'GME', name: 'GameStonk', price: 420.69, change: 0},
            {symbol: 'BTC', name: 'BitCoin', price: 69000, change: 0}
        ];
        function randomizeStocks() {
            fakeStocks.forEach(s => {
                let delta = (Math.random()-0.5)*2 * (s.price*0.01);
                s.change = Math.round(delta*100)/100;
                s.price = Math.round((s.price + delta)*100)/100;
            });
        }
        function renderTicker() {
            let html = '';
            fakeStocks.forEach(s => {
                let cls = s.change > 0 ? 'stock-up' : (s.change < 0 ? 'stock-down' : 'stock-neutral');
                let sign = s.change > 0 ? '+' : '';
                html += `<span><b>${s.symbol}</b> ${s.price} <span class="${cls}">${sign}${s.change}</span></span>`;
            });
            document.getElementById('ticker').innerHTML = html;
        }
        function updateValue() {
            fetch('/value').then(r => r.json()).then(data => {
                document.getElementById('value').innerText = data.value;
                const now = new Date();
                labels.push(now.toLocaleTimeString());
                values.push(data.value);
                if (labels.length > 20) { labels.shift(); values.shift(); }
                if (chart) {
                    chart.data.labels = labels;
                    chart.data.datasets[0].data = values;
                    chart.update();
                }
            });
        }
        window.onload = function() {
            const ctx = document.getElementById('myChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Stakeholder Value',
                        data: values,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75,192,192,0.1)',
                        tension: 0.2
                    }]
                },
                options: {
                    animation: false,
                    plugins: { legend: { labels: { color: '#FEE715' } } },
                    scales: { 
                        y: { beginAtZero: true, ticks: { color: '#FEE715' } },
                        x: { ticks: { color: '#FEE715' } }
                    }
                }
            });
            updateValue();
            setInterval(updateValue, 1000);
            renderTicker();
            setInterval(() => { randomizeStocks(); renderTicker(); }, 2000);
        }
        </script>
    </head>
    <body style="text-align:center;margin-top:2%">
        <div class="ticker" id="ticker"></div>
        <h1>💸 Number Go Up! 💸</h1>
        <h2>Stakeholder Value: <span id="value">0</span></h2>
        <canvas id="myChart" width="600" height="250" style="background:#222;border-radius:8px;"></canvas>
        <p style="font-style:italic; color:#FEE715;">Maximize stakeholder value! Infinite growth! 🚀</p>
    </body>
    </html>
    ''')

@app.route('/value')
def value():
    return jsonify(value=stakeholder_value['value'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)