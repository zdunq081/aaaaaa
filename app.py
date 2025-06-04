from flask import Flask, render_template_string, jsonify
import threading
import time

app = Flask(__name__)

stakeholder_value = {
    'value': 0,
    'pm_count': 0, 'pm_cost': 15, 'pm_gain': 0.5,
    'consultant_count': 0, 'consultant_cost': 100, 'consultant_gain': 5,
    'ai_count': 0, 'ai_cost': 1000, 'ai_gain': 50
}

def number_go_up():
    while True:
        stakeholder_value['value'] += (
            1
            + stakeholder_value['pm_count'] * stakeholder_value['pm_gain']
            + stakeholder_value['consultant_count'] * stakeholder_value['consultant_gain']
            + stakeholder_value['ai_count'] * stakeholder_value['ai_gain']
        )
        time.sleep(1)

# Start background thread to increment value
t = threading.Thread(target=number_go_up, daemon=True)
t.start()

@app.route('/buy_pm', methods=['POST'])
def buy_pm():
    cost = stakeholder_value['pm_cost']
    if stakeholder_value['value'] >= cost:
        stakeholder_value['value'] -= cost
        stakeholder_value['pm_count'] += 1
        stakeholder_value['pm_cost'] = int(15 * (1.15 ** stakeholder_value['pm_count']))
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/buy_consultant', methods=['POST'])
def buy_consultant():
    cost = stakeholder_value['consultant_cost']
    if stakeholder_value['value'] >= cost:
        stakeholder_value['value'] -= cost
        stakeholder_value['consultant_count'] += 1
        stakeholder_value['consultant_cost'] = int(100 * (1.18 ** stakeholder_value['consultant_count']))
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/buy_ai', methods=['POST'])
def buy_ai():
    cost = stakeholder_value['ai_cost']
    if stakeholder_value['value'] >= cost:
        stakeholder_value['value'] -= cost
        stakeholder_value['ai_count'] += 1
        stakeholder_value['ai_cost'] = int(1000 * (1.22 ** stakeholder_value['ai_count']))
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/value')
def value():
    return jsonify(
        value=round(stakeholder_value['value'],2),
        pm_count=stakeholder_value['pm_count'],
        pm_cost=stakeholder_value['pm_cost'],
        consultant_count=stakeholder_value['consultant_count'],
        consultant_cost=stakeholder_value['consultant_cost'],
        ai_count=stakeholder_value['ai_count'],
        ai_cost=stakeholder_value['ai_cost']
    )

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
        .upgrade-btn {
            background: #FEE715; color: #101820; border: none; border-radius: 6px; padding: 10px 20px; font-size: 1.1em; margin: 10px; cursor:pointer; font-weight:bold;
        }
        .upgrade-btn:disabled { background: #888; color: #222; cursor: not-allowed; }
        </style>
        <script>
        let chart;
        let values = [];
        let labels = [];
        function updateValue() {
            fetch('/value').then(r => r.json()).then(data => {
                document.getElementById('value').innerText = data.value;
                document.getElementById('pm_count').innerText = data.pm_count;
                document.getElementById('pm_cost').innerText = data.pm_cost;
                document.getElementById('consultant_count').innerText = data.consultant_count;
                document.getElementById('consultant_cost').innerText = data.consultant_cost;
                document.getElementById('ai_count').innerText = data.ai_count;
                document.getElementById('ai_cost').innerText = data.ai_cost;
                document.getElementById('buy_pm').disabled = (data.value < data.pm_cost);
                document.getElementById('buy_consultant').disabled = (data.value < data.consultant_cost);
                document.getElementById('buy_ai').disabled = (data.value < data.ai_cost);
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
        function buyPM() {
            fetch('/buy_pm', {method:'POST'}).then(()=>updateValue());
        }
        function buyConsultant() {
            fetch('/buy_consultant', {method:'POST'}).then(()=>updateValue());
        }
        function buyAI() {
            fetch('/buy_ai', {method:'POST'}).then(()=>updateValue());
        }
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
                html += `<span><b>${s.symbol}</b> ${s.price} <span class=\"${cls}\">${sign}${s.change}</span></span>`;
            });
            document.getElementById('ticker').innerHTML = html;
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
        <div style="margin:20px auto;max-width:500px;">
            <button class="upgrade-btn" id="buy_pm" onclick="buyPM()">Hire Project Manager<br>(Cost: <span id="pm_cost">15</span>)<br>+0.5 value/tick<br>Owned: <span id="pm_count">0</span></button>
            <button class="upgrade-btn" id="buy_consultant" onclick="buyConsultant()">Hire Consultant<br>(Cost: <span id="consultant_cost">100</span>)<br>+5 value/tick<br>Owned: <span id="consultant_count">0</span></button>
            <button class="upgrade-btn" id="buy_ai" onclick="buyAI()">Deploy AI Solution<br>(Cost: <span id="ai_cost">1000</span>)<br>+50 value/tick<br>Owned: <span id="ai_count">0</span></button>
        </div>
        <canvas id="myChart" width="600" height="250" style="background:#222;border-radius:8px;"></canvas>
        <p style="font-style:italic; color:#FEE715;">Maximize stakeholder value! Infinite growth! 🚀</p>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)