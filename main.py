from flask import Flask, jsonify
from flask import request, make_response
from datetime import datetime
import pandas as pd
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello, World!"


@app.route('/add_author', methods=['POST'])
def addAnAuthor():
    value = request.json
    if value["Author ID"] is None or value["Name"] is None or value["Birth Date"] is None:
        return "Please enter values for Not_null columns"
    try:
        if not bool(datetime.strptime(str(value["Birth Date"]), "%d-%m-%Y")):
            return "Please fill all mandatory fields"
        elif value["Death Date"] is not None and not bool(datetime.strptime(value["Death Date"], "%d-%m-%Y")):
            return "Please enter valid Date_of_death"
    except Exception as e:
        return str(e)
    result = make_response(jsonify(value))
    return "SUCCESS {}".format(result)


@app.route('/add_book_to_catalogue', methods=['POST'])
def addBookToCatalog():
    value = request.json
    if value["Book ID"] is None or value["Title"] is None or value["Author ID"] is None or value["Publisher"] is None or \
            value["Publish Date"] is None or value["Category ID"] is None or value["Price"] is None or \
            value["Sold Count"] is None:
        return "Please fill all mandatory fields"
    try:
        if not bool(datetime.strptime(value["Publish Date"], "%d-%m-%Y")):
            return "Please enter valid Date_of_birth"
    except Exception as e:
        return str(e)
    result = make_response(jsonify(value))
    return "SUCCESS {}".format(result)


@app.route('/add_category', methods=['POST'])
def addCategory():
    value = request.json
    if value["CategoryId"] is None or value["CategoryName"] is None:
        return "Please fill all mandatory fields"
    result = make_response(jsonify(value))
    return "SUCCESS {}".format(result)


@app.route('/get_list_of_categories', methods=['GET', 'POST'])
def getlistofcategories():
    value = str(request.json)
    if value:
        d = json.loads(value.replace("'", '"'))
        df = pd.DataFrame(d)
        result = []
        for i in df["CategoryName"]:
            if i not in result:
                result.append(i)
        return str(result)


@app.route('/get_list_of_authors', methods=['GET', 'POST'])
def getlistofauthors():
    value = str(request.json)
    if value:
        d = json.loads(value.replace("'", '"'))
        df = pd.DataFrame(d)
        result = []
        for i in df["Name"]:
            if i not in result:
                result.append(i)
        return str(result)


@app.route('/most_books_sold_by_author', methods=['GET', 'POST'])
def getMostBooksSoldByAuthor():
    value = str(request.json)
    if value:
        d = json.loads(value.replace("'", '"'))
        df = pd.DataFrame(d)
        input_authorid = list(df["input_authorid"])[0]
        content = list(df["values"])[0]
        max_value = 0
        result = {}
        for i in content:
            if i["Author ID"] == input_authorid:
                if i["Sold Count"] > max_value:
                    max_value = i["Sold Count"]
                    result = i
        return result


@app.route('/most_books_sold_by_category', methods=['GET', 'POST'])
def getMostBooksSoldByCategory():
    value = str(request.json)
    if value:
        d = json.loads(value.replace("'", '"'))
        df = pd.DataFrame(d)
        input_categoryid = list(df["input_categoryid"])[0]
        content = list(df["values"])[0]
        max_value = 0
        result = {}
        for i in content:
            if i["Category ID"] == input_categoryid:
                if i["Sold Count"] > max_value:
                    max_value = i["Sold Count"]
                    result = i
        return result


@app.route('/search_book', methods=['GET', 'POST'])
def searchbook():
    flag = len(request.json[0].items())
    value = str(request.json)
    if value:
        d = json.loads(value.replace("'", '"'))
        df = pd.DataFrame(d)
        content = list(df["values"])[0]
        result = []
        if flag == 2 and df.columns[0] == "input_partial_author":
            input_partial_author = list(df["input_partial_author"])[0]
            for i in content:
                if input_partial_author in i["Author name"]:
                    if i["Book ID"] not in result:
                        result.append(i["Book ID"])
        elif flag == 2 and df.columns[0] == "input_partial_title":
            input_partial_title = list(df["input_partial_title"])[0]
            for i in content:
                if input_partial_title in i["Title"]:
                    if i["Book ID"] not in result:
                        result.append(i["Book ID"])
        elif flag == 3:
            input_partial_title = list(df["input_partial_title"])[0]
            input_partial_author = list(df["input_partial_author"])[0]
            for i in content:
                if input_partial_author in i["Author name"] or input_partial_title in i["Title"]:
                    if i["Book ID"] not in result:
                        result.append(i["Book ID"])
        return str(result)


@app.route('/get_books_by_author', methods=['GET', 'POST'])
def getBooksByAuthor():
    value = str(request.json)
    if value:
        d = json.loads(value.replace("'", '"'))
        df = pd.DataFrame(d)
        input_authorid = list(df["input_authorid"])[0]
        content = list(df["values"])[0]
        result = []
        for i in content:
            if i["Author ID"] == input_authorid:
                if i["Book ID"] not in result:
                    result.append(i["Book ID"])
        return str(result)


if __name__ == '__main__':
    app.run(debug=True)
