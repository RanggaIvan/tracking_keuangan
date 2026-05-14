from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pymysql
import pymysql.cursors
from functools import wraps
from datetime import datetime, date
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'keuangan_secret_key_2026'

# ─────────────────────────────────────────
#  DATABASE CONNECTION
# ─────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'keuangan',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ─────────────────────────────────────────
#  AUTH DECORATOR
# ─────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────
#  AUTH ROUTES
# ─────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        db = get_db()
        try:
            with db.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                            (email, hash_password(password)))
                user = cur.fetchone()
            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                session['user_role'] = user['role']
                return redirect(url_for('dashboard'))
            else:
                error = 'Email atau password salah.'
        finally:
            db.close()
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        if not name or not email or not password:
            error = 'Semua field harus diisi.'
        elif password != confirm:
            error = 'Password dan konfirmasi tidak cocok.'
        elif len(password) < 6:
            error = 'Password minimal 6 karakter.'
        else:
            db = get_db()
            try:
                with db.cursor() as cur:
                    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
                    if cur.fetchone():
                        error = 'Email sudah terdaftar.'
                    else:
                        cur.execute(
                            "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,'user')",
                            (name, email, hash_password(password))
                        )
                        db.commit()
                        return redirect(url_for('login'))
            finally:
                db.close()
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    uid = session['user_id']
    try:
        with db.cursor() as cur:
            cur.execute("SELECT COALESCE(SUM(amount),0) AS total FROM transactions WHERE user_id=%s AND type='income'", (uid,))
            total_income = cur.fetchone()['total'] or 0

            cur.execute("SELECT COALESCE(SUM(amount),0) AS total FROM transactions WHERE user_id=%s AND type='expense'", (uid,))
            total_expense = cur.fetchone()['total'] or 0

            balance = float(total_income) - float(total_expense)

            cur.execute("""
                SELECT t.*, c.name AS category_name
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.user_id=%s
                ORDER BY t.transaction_date DESC, t.created_at DESC
                LIMIT 8
            """, (uid,))
            recent = cur.fetchall()

            cur.execute("""
                SELECT MONTH(transaction_date) AS m, YEAR(transaction_date) AS y,
                       type, SUM(amount) AS total
                FROM transactions
                WHERE user_id=%s AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY y, m, type
                ORDER BY y, m
            """, (uid,))
            chart_raw = cur.fetchall()

    finally:
        db.close()

    return render_template('dashboard.html',
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance,
                           recent=recent,
                           chart_raw=chart_raw)

# ─────────────────────────────────────────
#  TRANSACTIONS
# ─────────────────────────────────────────
@app.route('/transactions')
@login_required
def transactions():
    uid = session['user_id']
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    filter_type = request.args.get('type', '')
    filter_cat  = request.args.get('category', '')
    filter_start = request.args.get('start', '')
    filter_end   = request.args.get('end', '')

    db = get_db()
    try:
        with db.cursor() as cur:
            # ── Build WHERE clause ──
            where = "WHERE t.user_id=%s"
            params = [uid]
            if filter_type:
                where += " AND t.type=%s"; params.append(filter_type)
            if filter_cat:
                where += " AND t.category_id=%s"; params.append(filter_cat)
            if filter_start:
                where += " AND t.transaction_date>=%s"; params.append(filter_start)
            if filter_end:
                where += " AND t.transaction_date<=%s"; params.append(filter_end)

            cur.execute(f"SELECT COUNT(*) AS cnt FROM transactions t {where}", params)
            total = cur.fetchone()['cnt']

            cur.execute(f"""
                SELECT t.*, c.name AS category_name
                FROM transactions t
                LEFT JOIN categories c ON t.category_id=c.id
                {where}
                ORDER BY t.transaction_date DESC, t.created_at DESC
                LIMIT %s OFFSET %s
            """, params + [per_page, offset])
            rows = cur.fetchall()

            # ── FIX: query categories tanpa user_id ──
            cur.execute("SELECT * FROM categories ORDER BY type, name")
            categories = cur.fetchall()

    finally:
        db.close()

    total_pages = (total + per_page - 1) // per_page
    return render_template('transactions.html',
                           rows=rows, categories=categories,
                           page=page, total_pages=total_pages,
                           total=total,
                           filter_type=filter_type,
                           filter_cat=filter_cat,
                           filter_start=filter_start,
                           filter_end=filter_end)

@app.route('/transactions/add', methods=['POST'])
@login_required
def add_transaction():
    uid = session['user_id']
    data = request.form
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("""
                INSERT INTO transactions (user_id, category_id, type, amount, description, transaction_date)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (uid, data['category_id'], data['type'], data['amount'],
                  data.get('description',''), data['transaction_date']))
            db.commit()
    finally:
        db.close()
    return redirect(url_for('transactions'))

@app.route('/transactions/edit/<int:tid>', methods=['POST'])
@login_required
def edit_transaction(tid):
    uid = session['user_id']
    data = request.form
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("""
                UPDATE transactions SET category_id=%s, type=%s, amount=%s,
                description=%s, transaction_date=%s
                WHERE id=%s AND user_id=%s
            """, (data['category_id'], data['type'], data['amount'],
                  data.get('description',''), data['transaction_date'], tid, uid))
            db.commit()
    finally:
        db.close()
    return redirect(url_for('transactions'))

@app.route('/transactions/delete/<int:tid>', methods=['POST'])
@login_required
def delete_transaction(tid):
    uid = session['user_id']
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM transactions WHERE id=%s AND user_id=%s", (tid, uid))
            db.commit()
    finally:
        db.close()
    return redirect(url_for('transactions'))

@app.route('/transactions/get/<int:tid>')
@login_required
def get_transaction(tid):
    uid = session['user_id']
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM transactions WHERE id=%s AND user_id=%s", (tid, uid))
            row = cur.fetchone()
    finally:
        db.close()
    if row:
        row['transaction_date'] = str(row['transaction_date'])
        row['amount'] = float(row['amount'])
        row['created_at'] = str(row['created_at'])
        return jsonify(row)
    return jsonify({}), 404

# ─────────────────────────────────────────
#  CATEGORIES
# ─────────────────────────────────────────
@app.route('/categories')
@login_required
def categories():
    uid = session['user_id']
    db = get_db()
    try:
        with db.cursor() as cur:
            # ── FIX: tidak pakai user_id, hitung transaksi milik user ini ──
            cur.execute("""
                SELECT c.*, COUNT(t.id) AS tx_count
                FROM categories c
                LEFT JOIN transactions t ON t.category_id=c.id AND t.user_id=%s
                GROUP BY c.id
                ORDER BY c.type, c.name
            """, (uid,))
            rows = cur.fetchall()
    finally:
        db.close()
    return render_template('categories.html', rows=rows)

@app.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO categories (name, type) VALUES (%s,%s)",
                        (request.form['name'], request.form['type']))
            db.commit()
    finally:
        db.close()
    return redirect(url_for('categories'))

@app.route('/categories/edit/<int:cid>', methods=['POST'])
@login_required
def edit_category(cid):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE categories SET name=%s, type=%s WHERE id=%s",
                        (request.form['name'], request.form['type'], cid))
            db.commit()
    finally:
        db.close()
    return redirect(url_for('categories'))

@app.route('/categories/delete/<int:cid>', methods=['POST'])
@login_required
def delete_category(cid):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM categories WHERE id=%s", (cid,))
            db.commit()
    finally:
        db.close()
    return redirect(url_for('categories'))

@app.route('/categories/get/<int:cid>')
@login_required
def get_category(cid):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE id=%s", (cid,))
            row = cur.fetchone()
    finally:
        db.close()
    return jsonify(row or {})

# ─────────────────────────────────────────
#  REPORTS
# ─────────────────────────────────────────
@app.route('/reports')
@login_required
def reports():
    uid = session['user_id']
    now = datetime.now()
    month = int(request.args.get('month', now.month))
    year  = int(request.args.get('year',  now.year))
    report_type = request.args.get('report_type', 'monthly')

    db = get_db()
    try:
        with db.cursor() as cur:
            if report_type == 'monthly':
                cur.execute("""
                    SELECT t.*, c.name AS category_name
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id=c.id
                    WHERE t.user_id=%s
                      AND MONTH(t.transaction_date)=%s
                      AND YEAR(t.transaction_date)=%s
                    ORDER BY t.transaction_date DESC
                """, (uid, month, year))
            else:
                cur.execute("""
                    SELECT t.*, c.name AS category_name
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id=c.id
                    WHERE t.user_id=%s AND YEAR(t.transaction_date)=%s
                    ORDER BY t.transaction_date DESC
                """, (uid, year))
            rows = cur.fetchall()

            if report_type == 'monthly':
                cur.execute("""
                    SELECT c.name, c.type, SUM(t.amount) AS total
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id=c.id
                    WHERE t.user_id=%s
                      AND MONTH(t.transaction_date)=%s
                      AND YEAR(t.transaction_date)=%s
                    GROUP BY c.id ORDER BY total DESC
                """, (uid, month, year))
            else:
                cur.execute("""
                    SELECT c.name, c.type, SUM(t.amount) AS total
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id=c.id
                    WHERE t.user_id=%s AND YEAR(t.transaction_date)=%s
                    GROUP BY c.id ORDER BY total DESC
                """, (uid, year))
            by_cat = cur.fetchall()

            monthly_breakdown = []
            if report_type == 'yearly':
                cur.execute("""
                    SELECT MONTH(transaction_date) AS m, type, SUM(amount) AS total
                    FROM transactions
                    WHERE user_id=%s AND YEAR(transaction_date)=%s
                    GROUP BY m, type ORDER BY m
                """, (uid, year))
                monthly_breakdown = cur.fetchall()

    finally:
        db.close()

    total_income  = sum(float(r['amount']) for r in rows if r['type'] == 'income')
    total_expense = sum(float(r['amount']) for r in rows if r['type'] == 'expense')
    balance = total_income - total_expense

    years = list(range(now.year - 4, now.year + 2))
    months_list = [
        (1,'Januari'),(2,'Februari'),(3,'Maret'),(4,'April'),(5,'Mei'),(6,'Juni'),
        (7,'Juli'),(8,'Agustus'),(9,'September'),(10,'Oktober'),(11,'November'),(12,'Desember')
    ]

    return render_template('reports.html',
                           rows=rows, by_cat=by_cat,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance,
                           month=month, year=year,
                           report_type=report_type,
                           years=years,
                           months_list=months_list,
                           monthly_breakdown=monthly_breakdown)

# ─────────────────────────────────────────
#  PROFILE
# ─────────────────────────────────────────
@app.route('/profile')
@login_required
def profile():
    uid = session['user_id']
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id=%s", (uid,))
            user = cur.fetchone()
    finally:
        db.close()
    return render_template('profile.html', user=user)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    uid = session['user_id']
    name  = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    if not name or not email:
        flash('Nama dan email tidak boleh kosong.', 'error')
        return redirect(url_for('profile'))
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email=%s AND id!=%s", (email, uid))
            if cur.fetchone():
                flash('Email sudah digunakan.', 'error')
                return redirect(url_for('profile'))
            cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, uid))
            db.commit()
        session['user_name']  = name
        session['user_email'] = email
        flash('Profil berhasil diperbarui.', 'success')
    finally:
        db.close()
    return redirect(url_for('profile'))

@app.route('/profile/change_password', methods=['POST'])
@login_required
def change_password():
    uid    = session['user_id']
    old_pw = request.form.get('old_password', '')
    new_pw = request.form.get('new_password', '')
    confirm = request.form.get('confirm_password', '')
    if new_pw != confirm:
        flash('Password baru dan konfirmasi tidak cocok.', 'error')
        return redirect(url_for('profile'))
    if len(new_pw) < 6:
        flash('Password minimal 6 karakter.', 'error')
        return redirect(url_for('profile'))
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id=%s AND password=%s",
                        (uid, hash_password(old_pw)))
            if not cur.fetchone():
                flash('Password lama tidak benar.', 'error')
                return redirect(url_for('profile'))
            cur.execute("UPDATE users SET password=%s WHERE id=%s",
                        (hash_password(new_pw), uid))
            db.commit()
        flash('Password berhasil diubah.', 'success')
    finally:
        db.close()
    return redirect(url_for('profile'))

# ─────────────────────────────────────────
#  TEMPLATE FILTERS
# ─────────────────────────────────────────
@app.template_filter('rupiah')
def rupiah_filter(value):
    try:
        return "Rp {:,.0f}".format(float(value)).replace(',', '.')
    except:
        return "Rp 0"

@app.template_filter('format_date')
def format_date_filter(value):
    if not value:
        return '-'
    try:
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d')
        return value.strftime('%d %b %Y')
    except:
        return str(value)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
