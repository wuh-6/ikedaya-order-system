# app.py
from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# 读取商品列表
products_df = pd.read_excel("酒类商品_全94项_含分类与酒精标记_v2.xlsx")
products_by_category = {}
for _, row in products_df.iterrows():
    category = row["分类"]
    if category not in products_by_category:
        products_by_category[category] = []
    products_by_category[category].append(row["商品名"])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        delivery_date = request.form.get("delivery_date")

        orders = []
        for category, products in products_by_category.items():
            for product in products:
                quantity = request.form.get(product)
                if quantity and quantity.isdigit() and int(quantity) > 0:
                    orders.append([name, phone, delivery_date, product, quantity])

        # 写入 CSV
        file_exists = os.path.isfile("orders.csv")
        with open("orders.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["姓名", "电话", "配送日期", "商品名", "数量"])
            writer.writerows(orders)

        return redirect("/success")

    return render_template("index.html", products=products_by_category)

@app.route("/success")
def success():
    return "<h2>订单提交成功！感谢您的订购。</h2><a href='/'>返回首页</a>"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

