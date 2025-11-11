#include <bits/stdc++.h>
using namespace std;

// --------------------------------------------------
// Dummy dataset (simulating ecommerce data)
// --------------------------------------------------
struct Row {
    string category;
    double price;
    string state;
    string date;
};

vector<Row> DATA = {
    {"electronics", 1200, "SP", "2023-09-01"},
    {"electronics",  900, "RJ", "2023-09-05"},
    {"beauty",       400, "BA", "2023-08-11"},
    {"beauty",       350, "SP", "2023-09-17"},
    {"sports",       700, "MG", "2023-07-20"},
};

// --------------------------------------------------
// Utility helpers
// --------------------------------------------------
string monthsAgo(int m) {
    // Dummy static date for video — no real time math needed
    return "2023-06-01";
}

// --------------------------------------------------
// NL → SQL generator (rule-based)
// --------------------------------------------------
string generateSQL(const string &q0) {
    string q = q0;
    transform(q.begin(), q.end(), q.begin(), ::tolower);

    if (q.find("highest") != string::npos && q.find("category") != string::npos) {
        return 
R"(SELECT category, SUM(price) AS revenue
FROM data
WHERE date >= '2023-06-01'
GROUP BY category
ORDER BY revenue DESC
LIMIT 1;)";
    }

    if (q.find("average order value") != string::npos || q.find("aov") != string::npos) {
        return 
R"(SELECT AVG(price) AS avg_order_value
FROM data;)";
    }

    if (q.find("orders by state") != string::npos) {
        return 
R"(SELECT state, COUNT(*) AS orders
FROM data
GROUP BY state
ORDER BY orders DESC;)";
    }

    // Default fallback
    return 
R"(SELECT category, COUNT(*) AS total_items
FROM data
GROUP BY category;)";
}

// --------------------------------------------------
// Fake SQL executor (simulated computation)
// --------------------------------------------------
void executeSQL(const string &sql) {
    cout << "\nResult:\n";

    string low = sql;
    transform(low.begin(), low.end(), low.begin(), ::tolower);

    // Case 1: Revenue by category (top 1)
    if (low.find("sum(price)") != string::npos && low.find("group by category") != string::npos) {
        unordered_map<string, double> revenue;
        for (auto &r : DATA) revenue[r.category] += r.price;

        vector<pair<string,double>> v;
        for (auto &p : revenue) v.push_back(p);
        sort(v.begin(), v.end(), [&](auto &a, auto &b){
            return a.second > b.second;
        });

        cout << "category | revenue\n";
        cout << v[0].first << " | " << v[0].second << "\n";
        return;
    }

    // Case 2: AOV
    if (low.find("avg(price)") != string::npos) {
        double sum = 0;
        for (auto &r : DATA) sum += r.price;
        double aov = sum / DATA.size();

        cout << "avg_order_value\n" << aov << "\n";
        return;
    }

    // Case 3: Orders by state
    if (low.find("group by state") != string::npos) {
        unordered_map<string, int> cnt;
        for (auto &r : DATA) cnt[r.state]++;

        cout << "state | orders\n";
        for (auto &p : cnt) cout << p.first << " | " << p.second << "\n";
        return;
    }

    // Default: count items per category
    unordered_map<string, int> cnt;
    for (auto &r : DATA) cnt[r.category]++;

    cout << "category | total_items\n";
    for (auto &p : cnt) cout << p.first << " | " << p.second << "\n";
}

// --------------------------------------------------
// Main chat loop
// --------------------------------------------------
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "🛒 GenAI E-commerce Insights Demo (C++ Dummy Version)\n";
    cout << "Ask a question (type 'exit' to quit)\n\n";

    while (true) {
        cout << "You: ";
        string q;
        getline(cin, q);

        if (q == "exit" || q == "quit") {
            cout << "Bye!\n";
            break;
        }

        string sql = generateSQL(q);

        cout << "\nGenerated SQL:\n" << sql << "\n";

        executeSQL(sql);

        cout << "\n---------------------------------------\n";
    }

    return 0;
}
