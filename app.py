from flask import Flask, render_template, request, redirect, session, send_file
from models import db, User, Transaction

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'finance_secret'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return redirect('/login')


# REGISTER
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered"

        new_user = User(name=name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')

        else:
            return "Invalid email or password"

    return render_template('login.html')


# AUTO CATEGORY FUNCTION
def auto_category(description):

    description = description.lower()

    if any(word in description for word in ["uber","ola","bus","metro","train","taxi"]):
        return "Travel"

    elif any(word in description for word in ["swiggy","zomato","restaurant","food","cafe","dinner","lunch"]):
        return "Food"

    elif any(word in description for word in ["amazon","flipkart","shopping","mall","store"]):
        return "Shopping"

    elif any(word in description for word in ["gym","fitness","workout","health"]):
        return "Health"

    elif any(word in description for word in ["insurance","lic","policy"]):
        return "Insurance"

    elif any(word in description for word in ["rent","electricity","water","bill"]):
        return "Bills"

    else:
        return "Other"


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    transactions = Transaction.query.filter_by(user_id=session['user_id']).all()

    categories = {}

    for t in transactions:
        categories[t.category] = categories.get(t.category, 0) + t.amount

    labels = list(categories.keys())
    values = list(categories.values())

    insight = "Add expenses to see financial insights."
    budget = {}

    # Financial Health Score
    score = 100

    if categories:

        total_spent = sum(values)

        # Budget recommendation (reduce 10%)
        for cat, amount in categories.items():
            budget[cat] = round(amount * 0.9, 2)

        # Highest spending category
        max_category = max(categories, key=categories.get)
        max_amount = categories[max_category]

        insight = f"You spent the most on {max_category}. Reducing it by 10% can save {round(max_amount*0.1,2)}."

        # Health Score Rule 1: One category dominates spending
        if max_amount > total_spent * 0.5:
            score -= 20

        # Health Score Rule 2: Too many categories
        if len(categories) > 5:
            score -= 10

    return render_template(
        'dashboard.html',
        transactions=transactions,
        labels=labels,
        values=values,
        insight=insight,
        budget=budget,
        score=score
    )


# ADD EXPENSE
@app.route('/add_transaction', methods=['POST'])
def add_transaction():

    if 'user_id' not in session:
        return redirect('/login')

    description = request.form['description']
    amount = float(request.form['amount'])
    date = request.form['date']

    # automatic category detection
    category = auto_category(description)

    new_transaction = Transaction(
        user_id=session['user_id'],
        category=category,
        amount=amount,
        date=date,
        description=description
    )

    db.session.add(new_transaction)
    db.session.commit()

    return redirect('/dashboard')


# DOWNLOAD REPORT
@app.route('/download_report')
def download_report():

    if 'user_id' not in session:
        return redirect('/login')

    from datetime import datetime

    transactions = Transaction.query.filter_by(user_id=session['user_id']).all()

    current_month = datetime.now().month

    monthly_transactions = []

    for t in transactions:
        try:
            t_month = datetime.strptime(t.date, "%Y-%m-%d").month
            if t_month == current_month:
                monthly_transactions.append(t)
        except:
            pass

    categories = {}

    for t in monthly_transactions:
        categories[t.category] = categories.get(t.category, 0) + t.amount

    total = sum(categories.values())

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Monthly Financial Report", styles['Title']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Total Expenses This Month: {total}", styles['Normal']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph("Category Breakdown", styles['Heading2']))

    for cat, amount in categories.items():
        elements.append(Paragraph(f"{cat}: {amount}", styles['Normal']))

    filename = "monthly_report.pdf"

    pdf = SimpleDocTemplate(filename, pagesize=letter)
    pdf.build(elements)

    return send_file(filename, as_attachment=True)

# EXCELREPORT
@app.route('/download_excel')
def download_excel():

    if 'user_id' not in session:
        return redirect('/login')

    transactions = Transaction.query.filter_by(user_id=session['user_id']).all()

    data = []

    for t in transactions:
        data.append({
            "Date": t.date,
            "Category": t.category,
            "Amount": t.amount,
            "Description": t.description
        })

    df = pd.DataFrame(data)

    file_name = "financial_report.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(file_name, as_attachment=True)

@app.route('/chatbot', methods=['POST'])
def chatbot():

    if 'user_id' not in session:
        return redirect('/login')

    question = request.form['question'].lower()

    transactions = Transaction.query.filter_by(user_id=session['user_id']).all()

    total = 0
    categories = {}

    for t in transactions:
        total += t.amount
        categories[t.category] = categories.get(t.category, 0) + t.amount

    answer = "Sorry, I couldn't understand your question."

    if "total" in question or "spend" in question:
        answer = f"You spent {total} in total."

    elif "highest" in question or "biggest" in question:
        if categories:
            max_cat = max(categories, key=categories.get)
            answer = f"Your highest spending category is {max_cat}."

    elif "categories" in question:
        answer = ", ".join(categories.keys())

    return render_template(
        "dashboard.html",
        transactions=transactions,
        labels=list(categories.keys()),
        values=list(categories.values()),
        insight="Ask the assistant for insights.",
        budget={},
        chatbot_answer=answer
    )

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)