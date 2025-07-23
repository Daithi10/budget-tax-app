from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random string for the session
# Simulated in-memory user store
users = {}

# This will store budget data temporarily (in-memory)
saved_budgets = []

# Budget form route (handles GET and POST)
@app.route("/budget", methods=["GET", "POST"])
def budget():
    residual_income = None
    savings_amount = None
    savings_percent = None
    username = session.get("username", None)

    if request.method == "POST":
        if "residual_income" in request.form:  # Savings calculation
            residual_income = float(request.form["residual_income"])
            savings_percent = float(request.form["savings"])
            savings_amount = round((savings_percent / 100) * residual_income, 2)
        else:  # Budget calculation
            try:
                income = float(request.form.get("income", 0))
                rent = float(request.form.get("rent", 0))
                groceries = float(request.form.get("groceries", 0))
                transport = float(request.form.get("transport", 0))
                utilities = float(request.form.get("utilities", 0))
                other = float(request.form.get("other", 0))

                total_expenses = rent + groceries + transport + utilities + other
                residual_income = round(income - total_expenses, 2)

            except ValueError:
                flash("Please enter valid numeric values.")

    return render_template(
        "budget.html",
        residual_income=residual_income,
        savings_amount=savings_amount,
        savings_percent=savings_percent,
        username=username
    )
# View saved budgets
saved_budgets = []
@app.route('/saved-budgets')
def saved():
    if 'username' not in session:
        flash('Please log in to view saved budgets.')
        return redirect(url_for('login'))
    return render_template('saved_budgets.html', budgets=saved_budgets)


@app.route("/tax", methods=["GET", "POST"])
def tax():
    result = None
    breakdown = {}
    salary = None

    if request.method == "POST":
        salary = float(request.form["salary"])
        marital_status = request.form["marital_status"]
        children_count = int(request.form.get("children_count", 0))
        age_group = request.form["age_group"]
        employment_type = request.form["employment_type"]
        tax_credits = float(request.form.get("tax_credits", 0))

        # CHILD TAX EXEMPTION
        child_exemption = 0
        if children_count > 0:
            first_two = min(children_count, 2)
            additional = max(children_count - 2, 0)
            child_exemption = (first_two * 575) + (additional * 830)

        # AGE 65+ EXEMPTION
        if age_group == "65_plus":
            exemption_limit = 18000 if marital_status == "single" else 36000
            if salary <= exemption_limit:
                result = 0.0
                breakdown["65+ Exemption"] = f"Income under €{exemption_limit}, no tax due"
                return render_template("tax.html", result=result, salary=salary, breakdown=breakdown)

        # TAX CALCULATION
        standard_band = 40000
        if marital_status == "married":
            standard_band = 49000

        standard_rate = 0.20
        higher_rate = 0.40

        if salary <= standard_band:
            tax = salary * standard_rate
            breakdown["Standard Rate (20%)"] = round(tax, 2)
        else:
            standard_tax = standard_band * standard_rate
            higher_tax = (salary - standard_band) * higher_rate
            tax = standard_tax + higher_tax
            breakdown["Standard Rate (20%)"] = round(standard_tax, 2)
            breakdown["Higher Rate (40%)"] = round(higher_tax, 2)

        # Subtract tax credits and child exemption
        tax -= (tax_credits + child_exemption)
        tax = max(tax, 0)

        if child_exemption > 0:
            breakdown["Child Exemption"] = f"-€{round(child_exemption, 2)}"

        if tax_credits > 0:
            breakdown["Tax Credits"] = f"-€{round(tax_credits, 2)}"

        result = round(tax, 2)

    return render_template("tax.html", result=result, salary=salary, breakdown=breakdown)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Securely check if username exists AND password is correct
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect(url_for('budget'))  # Redirect to budget page
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/')
def index():
    # You could check if user is logged in, then redirect accordingly
    if 'username' in session:
        return redirect(url_for('dashboard'))  # or wherever logged-in users go
    return render_template('index.html')

users = {}  # In-memory user store: {'username': 'password'}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        security_question = request.form.get('security_question')
        security_answer = request.form.get('security_answer', '').strip()

        # Basic validations
        if not email or not username or not password or not confirm_password or not security_question or not security_answer:
            error = 'Please fill in all required fields.'
            return render_template('register.html', error=error)

        if username in users:
            error = 'Username already exists.'
            return render_template('register.html', error=error)

        if password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('register.html', error=error)

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save user info (example user dict)
        users[username] = {
            'fullname': fullname,
            'email': email,
            'password': hashed_password,
            'security_question': security_question,
            'security_answer': security_answer
        }

        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')
if __name__ == '__main__':
    print("Starting Flask app... Open http://127.0.0.1:5000/ in your browser")
    app.run(debug=True)
