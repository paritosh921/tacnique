import sqlite3
from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def parse_query(query):
    """
    Converts a natural language query into an SQL statement and parameters.
    Supported queries:
      - "Show me all employees in the [department] department."
      - "Who is the manager of the [department] department?"
      - "List all employees hired after [date]." (date in YYYY-MM-DD)
      - "What is the total salary expense for the [department] department?"
    """
    query = query.lower().strip()


    m = re.match(r'show me all employees in the ([\w\s]+) department', query)
    if m:
        department = m.group(1).strip().title()
        sql = "SELECT * FROM Employees WHERE Department = ?"
        params = (department,)
        return sql, params


    m = re.match(r'who is the manager of the ([\w\s]+) department', query)
    if m:
        department = m.group(1).strip().title()
        sql = "SELECT Manager FROM Departments WHERE Name = ?"
        params = (department,)
        return sql, params


    m = re.match(r'list all employees hired after ([\d]{4}-[\d]{2}-[\d]{2})', query)
    if m:
        date = m.group(1)
        sql = "SELECT * FROM Employees WHERE Hire_Date > ?"
        params = (date,)
        return sql, params


    m = re.match(r'what is the total salary expense for the ([\w\s]+) department', query)
    if m:
        department = m.group(1).strip().title()
        sql = "SELECT SUM(Salary) as total_salary FROM Employees WHERE Department = ?"
        params = (department,)
        return sql, params

    return None, None

index_html = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Employee Database Chat Interface</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    <style>
        .chat-container {
            height: calc(100vh - 200px);
            background: #f8fafc;
        }
        .message {
            max-width: 80%;
            margin: 8px;
            padding: 12px;
            border-radius: 12px;
            position: relative;
        }
        .user-message {
            background: #3b82f6;
            color: white;
            margin-left: auto;
        }
        .bot-message {
            background: white;
            border: 1px solid #e5e7eb;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background: white;
        }
        .data-table th {
            background: #f3f4f6;
            padding: 8px;
            text-align: left;
            font-weight: 600;
        }
        .data-table td {
            padding: 8px;
            border-top: 1px solid #e5e7eb;
        }
        .sample-query {
            transition: all 0.2s;
        }
        .sample-query:hover {
            background: #dbeafe;
            transform: translateX(5px);
        }
        .queries-container {
            max-height: calc(100vh - 200px);
            overflow-y: auto;
        }
        .query-category {
            margin-bottom: 1rem;
        }
        .query-category-title {
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 0.5rem;
            padding: 0.5rem;
            background: #f3f4f6;
            border-radius: 0.375rem;
        }
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-3 gap-6">
            
            <div class="col-span-2">
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h1 class="text-2xl font-bold mb-4">Employee Database Assistant</h1>
                    <div id="chat" class="chat-container overflow-y-auto mb-4 p-4 rounded-lg"></div>
                    <div class="flex gap-2">
                        <input type="text" id="message" 
                               class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                               placeholder="Type your query here...">
                        <button id="send" 
                                class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                            Send
                        </button>
                    </div>
                </div>
            </div>
            
        
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h2 class="text-xl font-semibold mb-4">Sample Queries</h2>
                <div class="queries-container space-y-4">
               
                    <div class="query-category">
                        <div class="query-category-title">View Department Employees</div>
                        <div class="space-y-2">
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                Show me all employees in the Sales department.
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                Show me all employees in the Engineering department.
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                Show me all employees in the Marketing department.
                            </div>
                        </div>
                    </div>

                    <div class="query-category">
                        <div class="query-category-title">Find Department Managers</div>
                        <div class="space-y-2">
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                Who is the manager of the Sales department?
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                Who is the manager of the Engineering department?
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                Who is the manager of the Marketing department?
                            </div>
                        </div>
                    </div>

                    <div class="query-category">
                        <div class="query-category-title">Search by Hire Date</div>
                        <div class="space-y-2">
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                List all employees hired after 2021-01-10.
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                List all employees hired after 2020-06-10.
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                List all employees hired after 2022-03-20.
                            </div>
                        </div>
                    </div>

                    <div class="query-category">
                        <div class="query-category-title">Department Salary Expenses</div>
                        <div class="space-y-2">
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                What is the total salary expense for the Sales department?
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                What is the total salary expense for the Engineering department?
                            </div>
                            <div class="sample-query p-3 rounded cursor-pointer hover:bg-blue-50" onclick="copyQuery(this)">
                                What is the total salary expense for the Marketing department?
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const chatDiv = document.getElementById("chat");
        const messageInput = document.getElementById("message");

        function formatResponse(data) {
            if (data.error) {
                return `<div class="text-red-500">${data.error}</div>`;
            }

            if (data.manager) {
                return `<div class="p-3 bg-blue-50 rounded">
                    <span class="font-semibold">Department Manager:</span> ${data.manager}
                </div>`;
            }

            if (data.total_salary_expense) {
                return `<div class="p-3 bg-blue-50 rounded">
                    <span class="font-semibold">Total Salary Expense:</span> 
                    $${data.total_salary_expense.toLocaleString()}
                </div>`;
            }

            if (data.employees) {
                if (data.employees.length === 0) {
                    return '<div class="text-gray-500">No employees found matching your criteria.</div>';
                }

                const headers = Object.keys(data.employees[0]);
                let tableHtml = '<table class="data-table"><thead><tr>';
                
                // Create headers
                headers.forEach(header => {
                    tableHtml += `<th>${header.replace('_', ' ').toUpperCase()}</th>`;
                });
                tableHtml += '</tr></thead><tbody>';

                // Create rows
                data.employees.forEach(employee => {
                    tableHtml += '<tr>';
                    headers.forEach(header => {
                        let value = employee[header];
                        if (header.toLowerCase().includes('salary')) {
                            value = '$' + value.toLocaleString();
                        }
                        tableHtml += `<td>${value}</td>`;
                    });
                    tableHtml += '</tr>';
                });

                tableHtml += '</tbody></table>';
                return tableHtml;
            }

            return '<div class="text-gray-500">No data available.</div>';
        }

        function appendMessage(text, sender) {
            const messageEl = document.createElement("div");
            messageEl.className = `message ${sender === 'user' ? 'user-message' : 'bot-message'}`;
            
            if (sender === 'user') {
                messageEl.textContent = text;
            } else {
                try {
                    const data = JSON.parse(text);
                    messageEl.innerHTML = formatResponse(data);
                } catch (e) {
                    messageEl.textContent = text;
                }
            }
            
            chatDiv.appendChild(messageEl);
            chatDiv.scrollTop = chatDiv.scrollHeight;
        }

        function copyQuery(element) {
            messageInput.value = element.textContent.trim();
            messageInput.focus();
        }

        document.getElementById("send").addEventListener("click", function() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            appendMessage(message, "user");
            messageInput.value = "";

            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message })
            })
            .then(response => response.json())
            .then(data => {
                appendMessage(JSON.stringify(data), "bot");
            })
            .catch(error => {
                console.error("Error:", error);
                appendMessage("Error processing your request.", "bot");
            });
        });

        messageInput.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                document.getElementById("send").click();
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(index_html)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' parameter in JSON payload."}), 400

    query_text = data['query']
    sql, params = parse_query(query_text)
    if sql is None:
        return jsonify({"error": "Query not recognized or unsupported. Please try a different query."}), 400

    conn = get_db_connection()
    try:
        cur = conn.execute(sql, params)
        rows = cur.fetchall()
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    conn.close()

    if 'SUM(Salary)' in sql:
        total_salary = rows[0]['total_salary'] if rows and rows[0]['total_salary'] is not None else 0
        result = {"total_salary_expense": total_salary}
    elif 'Manager' in sql:
        if rows:
            manager = rows[0]['Manager']
            if manager:
                result = {"manager": manager}
            else:
                result = {"message": "Department found, but no manager is assigned."}
        else:
            result = {"error": "Department not found. Please check the department name."}
    else:
        if rows:
            employees = [dict(row) for row in rows]
            result = {"employees": employees}
        else:
            result = {"message": "No records found matching your query."}

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)