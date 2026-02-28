from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
import qrcode
import uuid
import os
# --- ADD THESE TWO LINES ---
from dotenv import load_dotenv
load_dotenv()
# ---------------------------

app = Flask(__name__)

# --- SECURE CONFIGURATION ---
# We use os.getenv to pull the URI from your .env file
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
# ---------------------------

# Categorized Capacity (3000+ total)
CAPACITY = {'2W': 2000, '4W': 1000}

@app.route('/')
def index():
    # Calculate live occupancy
    count_2w = mongo.db.vehicles.count_documents({"v_type": "2W", "status": "IN"})
    count_4w = mongo.db.vehicles.count_documents({"v_type": "4W", "status": "IN"})
    return render_template('index.html', c2w=count_2w, c4w=count_4w, cap=CAPACITY)

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    v_id = str(uuid.uuid4())[:8].upper()
    
    # Save to MongoDB
    vehicle_doc = {
        "_id": v_id,
        "plate": data['plate'],
        "owner": data['owner'],
        "contact": data['contact'],
        "v_type": data['v_type'],
        "status": "OUT",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    }
    mongo.db.vehicles.insert_one(vehicle_doc)
    
    # Generate QR Code
    qr_path = f"static/qrcodes/{v_id}.png"
    if not os.path.exists('static/qrcodes'): os.makedirs('static/qrcodes')
    qrcode.make(f"CHECK:{v_id}").save(qr_path)
    
    return f"Registration Success! ID: {v_id}. QR saved to {qr_path}"

@app.route('/lookup', methods=['GET'])
def lookup():
    plate = request.args.get('plate')
    vehicle = mongo.db.vehicles.find_one({"plate": plate})
    if vehicle:
        return jsonify({
            "owner": vehicle['owner'],
            "contact": vehicle['contact'],
            "status": vehicle['status']
        })
    return jsonify({"error": "Not Found"}), 404

@app.route('/scan/<v_id>', methods=['POST'])
def scan_handle(v_id):
    vehicle = mongo.db.vehicles.find_one({"_id": v_id})
    
    if not vehicle:
        return jsonify({"error": "Invalid QR Code"}), 404
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if vehicle['status'] == 'OUT':
        current_in = mongo.db.vehicles.count_documents({"v_type": vehicle['v_type'], "status": "IN"})
        if current_in >= CAPACITY[vehicle['v_type']]:
            return jsonify({"error": f"{vehicle['v_type']} Zone is Full!"}), 400
        
        new_status = 'IN'
        update_fields = {"status": new_status, "last_entry": now}
    else:
        new_status = 'OUT'
        update_fields = {"status": new_status, "last_exit": now}
        
    mongo.db.vehicles.update_one({"_id": v_id}, {"$set": update_fields})
    
    return jsonify({
        "status": new_status, 
        "owner": vehicle['owner'], 
        "plate": vehicle['plate'],
        "time": now
    })

if __name__ == '__main__':
    app.run(debug=True)