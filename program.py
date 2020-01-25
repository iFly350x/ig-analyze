from flask import Flask, redirect, url_for, render_template, request, jsonify, session, flash
import requests
import string

app = Flask(__name__)
app.debug = True
app.secret_key = "sup"

def search(ig_name): 
	url = "https://www.instagram.com/{}/?__a=1".format(ig_name)
	r = requests.get(url)
	stcode = r.status_code
	if stcode == 200:
		res = r.json()
		followers = ("Followers: {}".format(res['graphql']['user']['edge_followed_by']['count']))
		following = ("Following: {}".format(res['graphql']['user']['edge_follow']['count']))
		posts = ("Posts: {}".format(len(res["graphql"]['user']["edge_owner_to_timeline_media"]['edges'])))
		#photos and likes of every photo
		likes = sum([res["graphql"]['user']["edge_owner_to_timeline_media"]['edges'][i]["node"]["edge_liked_by"]['count'] for i in range(len(res["graphql"]['user']["edge_owner_to_timeline_media"]['edges']))])
    	# total_likes = "Total Likes: {}".format(likes)
		return followers, following, posts, likes
	else:
		print("Shit is Broken")

@app.route("/", methods=["POST", "GET"] )
def home():
	if request.method == "POST":
		name = request.form["nm"]
		return redirect(url_for("response", name=name))
	else:
		return render_template("index.html", title="Instgram Analyzer")

@app.route("/response/<name>", methods=["POST", "GET"])
def response(name):
	data = search(name)
	if data[3] == 0:
		flash("Enable to calculate number of likes due to the account being private.")
	return render_template("response.html", title="Response", name=name, posts=data[2], likes=data[3], following=data[1], followers=data[0])
		

if __name__ == "__main__":
	app.run()
