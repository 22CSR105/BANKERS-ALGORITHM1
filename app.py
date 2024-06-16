from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def is_safe(processes, avail, max_demand, allocation):
    work = avail[:]
    finish = [False] * processes
    safe_seq = []

    need = [[0] * len(avail) for _ in range(processes)]
    for i in range(processes):
        for j in range(len(avail)):
            need[i][j] = max_demand[i][j] - allocation[i][j]

    while len(safe_seq) < processes:
        found = False
        for i in range(processes):
            if not finish[i]:
                for j in range(len(avail)):
                    if need[i][j] > work[j]:
                        break
                else:
                    for k in range(len(avail)):
                        work[k] += allocation[i][k]
                    safe_seq.append(i)
                    finish[i] = True
                    found = True
        if not found:
            return False, []

    return True, safe_seq

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    processes = data['processes']
    avail = data['avail']
    max_demand = data['max_demand']
    allocation = data['allocation']
    
    safe, safe_seq = is_safe(processes, avail, max_demand, allocation)
    return jsonify({'safe': safe, 'safe_seq': safe_seq})

if __name__ == '__main__':
    app.run(port=5500, debug=True)
