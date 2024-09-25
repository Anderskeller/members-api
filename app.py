from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Læs alle members (GET)
@app.route('/members', methods=['GET'])
def get_members():
    with sqlite3.connect('members.sqlite') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members")
        members = cur.fetchall()
        return jsonify([dict(zip([column[0] for column in cur.description], row)) for row in members])
    
    

# Læs én member baseret på ID (GET)
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    with sqlite3.connect('members.sqlite') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members WHERE id=?", (member_id,))
        member = cur.fetchone()
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        return jsonify(dict(zip([column[0] for column in cur.description], member)))

# Tilføj en ny member (POST)
@app.route('/members', methods=['POST'])
def create_member():
    data = request.json
    with sqlite3.connect('members.sqlite') as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO members (first_name, last_name, birth_date, gender, email, phonenumber, address, nationality, active, github_username)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['first_name'], data['last_name'], data['birth_date'], data['gender'], data['email'], data['phonenumber'], data['address'], data['nationality'], data['active'], data['github_username']))
        conn.commit()
        return jsonify(data), 201

# Opdater kun github_username (PATCH)
@app.route('/members/<int:member_id>/github_username', methods=['PATCH'])
def update_github_username(member_id):
    data = request.json
    with sqlite3.connect('members.sqlite') as conn:
        cur = conn.cursor()
        cur.execute('''
            UPDATE members
            SET github_username=?
            WHERE id=?
        ''', (data['github_username'], member_id))
        conn.commit()
        return jsonify({"message": "GitHub username updated"}), 200

# Slet en member (DELETE)
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    with sqlite3.connect('members.sqlite') as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM members WHERE id=?", (member_id,))
        conn.commit()
        return jsonify({"message": "Member deleted"})

if __name__ == '__main__':
    app.run(debug=True) 