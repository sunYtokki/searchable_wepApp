import json, copy, re
from db import venues
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

app = Flask(__name__)

current_id = 30
result = []
search_key = None

# =======================================================================


@app.route('/')
def home():
    global venues
    showcase = []
    lastIdx = len(venues)
    startIdx = lastIdx - 12

    for i in range(startIdx, lastIdx):
        showcase.insert(0,venues[i])

    return render_template('home.html', data=showcase)


@app.route('/autoComplete')
def autoComplete():
    names = []

    for i in range(0, len(venues)):
        names.append(venues[i]['name'])

    return jsonify(names)


@app.route('/view/<venue_id>')
def view_result(venue_id):
    global venues
    view_id = int(venue_id)
    # data = []
    name = None
    img = None
    description = None
    rating = None
    reviews = [None,None,None]

    for i in range(0, len(venues)):
        if venues[i]['id'] == view_id:
            name = venues[i]['name']
            img = venues[i]['image']
            description = venues[i]['description']
            rating = venues[i]['rating']
            reviews = venues[i]['reviews']
            # data = venues[i]

    return render_template('view.html', name=name, img=img, venue_id=view_id, 
         description=description, rating=rating, reviews=reviews)


@app.route('/search_process', methods=['POST'])
def search_process():
    global venues
    global search_key
    global result
    result.clear()

    target = request.form['target'].lower()
    search_key = target

    for i in range(0, len(venues)):
        name = venues[i]['name'].lower()
        description = venues[i]['description'].lower()
        if target in name or target in description:
            result.append(venues[i])

    return jsonify(result)


@app.route('/search')
def search():
    global search_key
    global result
    highlighted = copy.deepcopy(result)
    search_str = str(search_key)
    
    for i in range(0, len(highlighted)):
        
        desc = highlighted[i]['description']
        desc = re.sub(search_str, r"<span class='hl'>\g<0></span>", desc, flags=re.IGNORECASE)
        highlighted[i]['description'] = desc 
        
        name = highlighted[i]['name']
        name = re.sub(search_str, r"<span class='hl'>\g<0></span>", name, flags=re.IGNORECASE)
        highlighted[i]['name'] = name

    return render_template('search.html', result=highlighted, key=search_key)


@app.route('/edits', methods=['POST'])
def addReview():
    global venues
    id = int(request.form['id'])

    new_user = request.form['new_user']
    new_review = request.form['new_review']
    reviews = venues[id]['reviews']

    if new_user and new_review:
        new_data = {
            "id": len(reviews),
            "is_deleted": False,
            "user": new_user,
            "review": new_review
        }

    reviews.insert(0, new_data)
    
    return jsonify(reviews)


@app.route('/edits2', methods=['POST'])
def eidtDescription():
    global venues
    id = int(request.form['id'])

    new_description = request.form['new_description']
    new_rating= request.form['new_rating']

    if new_description:
        venues[id]['description'] = new_description

    if new_rating:
        venues[id]['rating'] = new_rating

    return jsonify({"new_desc":new_description, "new_rating":new_rating})


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    global venues
    venue_id = int(request.form['venue_id'])
    deleted_id = int(request.form['delete_id'])
    is_undo = int(request.form['is_undo'])
    flagged = None
    idx = None

    for i in range (0, len(venues)):
        if venues[i]['id'] == venue_id:
            idx=i
            break

    reviews = venues[idx]['reviews']

    for j in range (0, len(reviews)):
        if reviews[j]['id'] == deleted_id:
            # jdx = j
            flagged = reviews[j]
            
            if is_undo == 0:
                reviews[j]['is_deleted'] = True
            if is_undo == 1:
                reviews[j]['is_deleted'] = False

    return jsonify({"deleted":flagged, "is_undo":is_undo}) 


@app.route('/create')
def create():

    return render_template('create.html')
    

@app.route('/create_process', methods=['POST'])
def create_process():
    global venues
    global current_id

    new_entry = current_id
    new_data = request.get_json()
    venues.append(new_data)
    venues[new_entry]['id'] = current_id

    current_id += 1

    return jsonify(venues[new_entry])


if __name__ == '__main__':
    app.run(debug=True)
