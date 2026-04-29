from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore
from google.cloud import secretmanager

app = Flask(__name__)
db = firestore.Client()



# Flask to fetch the flask-secret-key from Secret Manager at startup.
# This is how the app uses secrets securely without hardcoding them. 
def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/gcp-recipes/secrets/{secret_id}/versions/latest"   
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


app.secret_key = get_secret("flask-secret-key")





# Get all documents from the recipes collection
# Build a list of recipe dicts (include the document ID too)
# Return str(recipes)

@app.route('/')
def hello():
    docs = db.collection('recipes').stream()
    recipes = []
    for doc in docs:
        recipe = doc.to_dict()
        recipe['id'] = doc.id # identify each recipe uniquely
        recipes.append(recipe)
    return str(recipes)


# Gets form data: title, ingredients, instructions, category
# Saves it to Firestore collection recipes
# Redirects to /

@app.route('/recipe/add', methods=['POST'])
def add_recipe():
    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    instructions = request.form.get('instructions')
    category = request.form.get('category')

    db.collection('recipes').add({
     'title': title,
     'ingredients': ingredients,
     'instructions': instructions,
     'category': category
    })
    return redirect(url_for('hello'))



# GET /recipe/<id> - fetch a single recipe by its Firestore document ID@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    doc = db.collection('recipes').document(id).get()
    return str(doc.to_dict())


   
     
  
    # POST /recipe/delete/<id> - delete a recipe by ID, redirect to /
@app.route('/recipe/delete/<id>', methods=['POST'])
def delete_recipe(id):
    db.collection('recipes').document(id).delete()
    return redirect(url_for('hello'))


    # GET /search
    # Get a query parameter q from the URL (e.g. /search?q=pasta)
    # Fetch all recipes from Firestore
    # Filter them where category or ingredients contains the search term
    # Return str(results)

@app.route('/search', methods=['GET'])
def search_recipe():
    q = request.args.get('q', '')
    docs = db.collection('recipes').stream()
    results = []
    for doc in docs:
        recipe = doc.to_dict()
        recipe['id'] = doc.id
        if q.lower() in recipe.get('category', '').lower() or q.lower() in recipe.get('ingredients', '').lower():
            results.append(recipe)
    return str(results)


    



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)


