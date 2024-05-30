# BEGIN CODE HERE
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# END CODE HERE 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get("name")
    products = mongo.db.products.find({"$text": {"$search": name}}).sort("price", -1)
    results = [{"id": str(product["_id"]), "name": product["name"], "production_year": product["production_year"], "price": product["price"], "color": product["color"], "size": product["size"]} for product in products]
    return jsonify(results)
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    data = request.get_json()
    product = {"id": data["id"], "name": data["name"], "production_year": data["production_year"], "price": data["price"], "color": int(data["color"]), "size": int(data["size"])}
    existing_product = mongo.db.products.find_one({"name": product["name"]})
    if existing_product:
        updated_product = mongo.db.products.find_one_and_update({"name": product["name"]}, {"$set": product}, return_document=True)
        product["id"] = str(updated_product["_id"])
    else:
        mongo.db.products.insert_one(product)
    return jsonify(product)
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    data = request.get_json()
    product = {"id": data["id"], "name": data["name"], "production_year": data["production_year"], "price": data["price"], "color": int(data["color"]), "size": int(data["size"])}
    products = mongo.db.products.find()
    product_vectors = []
    for p in products:
        vector = np.array([p["price"], p["production_year"], p["color"], p["size"]])
        product_vectors.append(vector)
    query_vector = np.array([product["price"], product["production_year"], product["color"], product["size"]])
    similarities = []
    for vector in product_vectors:
        similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
        similarities.append(similarity)
    recommended_products = [p["name"] for p in products if similarities[products.index(p)] > 0.7]
    return jsonify(recommended_products)
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    semester = int(request.args.get("semester"))
    driver = webdriver.Chrome()
    driver.get("https://qa.auth.gr/el/x/studyguide/600000438/current")
    courses = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='course']")))
    course_names = [course.text for course in courses]
    driver.quit()
    return jsonify(course_names)
    # END CODE HERE
