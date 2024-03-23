from app import app
import users, posts, comments, topics
from flask import render_template, request, redirect, session
import re
import sys


@app.route("/")
def index():
    all_posts= posts.get_posts()
    quotes=users.get_quotes()
    all_topics=topics.get_topics()
    all_comments=comments.get_all_comments()
    random_post_id=posts.get_random_post()
    usernames = users.get_usernames()
    if all_posts!=False:
        return render_template("index.html", all_posts=all_posts, quotes=quotes, topics=all_topics, all_comments=all_comments, random_post_id=random_post_id, usernames=usernames)
    else:
        return render_template("index.html")

 
@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Käyttäjätunnusta ei löytynyt näillä arvoilla. Kokeile uudelleen tai rekisteröidy. ")
        else:
            users.login(username, password)
            return redirect('/')

@app.route("/register",methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        role = request.form["role"]

    # Identification and Authentication failures
    # Users should be required to use a strong password, fix below
    #if len(password) < 8:
    #    return render_template("error.html", message="Password should be at least 8 characters long.")
    #if re.search(r'\s', password):
    #    return render_template("error.html", message="The password should not contain spaces.")
    #if re.search(r'\s', username):
    #    return render_template("error.html", message="The username should not contain spaces.")
    #if not (re.search(r'[a-zA-Z]', password) and re.search(r'\d', password)):
    #    return render_template("error.html", message="The password should include both letters and numbers.")
    
    if not re.match(r'^[a-zA-Z0-9_]{4,14}$', username):
        return render_template("error.html", message="Username should be 4-14 characters long and only contain letters, numbers, or underscores.")
    
    if password != password2:
        return render_template("error.html", message="Salasanat eivät täsmää.")
       
    else:
        if users.register(username, password, role):
            users.login(username, password)
        else:
            return render_template("error.html", message="Rekisteröityminen epäonnistui")

        return redirect("/")



@app.route("/new_post",methods=["get", "post"])
def new_post():
    if request.method == "GET":
        quote=users.get_quote()
        all_topics=topics.get_topics()
        if quote:
            return render_template("new_post.html", quote=quote, topics=all_topics)
        else:
            return render_template("new_post.html", topics=all_topics)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        user_id=request.form["user_id"]
        topic_id=request.form["topic"]
        #users.check_csrf()

        if len(title)==0 or len(content)==0 or title.isspace() or content.isspace():
            return render_template("error.html", message="Julkaisun ja sen otsikon täytyy sisältää tekstiä.")
        post_id = posts.create_post(title, content, True, user_id, topic_id)
        return redirect("/post/"+post_id)
  
@app.route("/post/<post_id>")
def post_page(post_id):
    title=posts.get_title(post_id)
    content=posts.get_content(post_id)
    all_comments=comments.get_comments(post_id)
    all_topics=topics.get_topics()
    post=posts.get_post(post_id)
    quotes=users.get_quotes()
    random_post_id=posts.get_random_post()
    usernames = users.get_usernames()
    return render_template("/post.html", title = title, content = content, quotes=quotes, topics=all_topics, comments= all_comments, post=post, post_id = post_id, random_post_id=random_post_id, usernames=usernames)

 
@app.route("/topic/<topic_id>")
def topic(topic_id):
    all_posts= posts.get_posts()
    quotes=users.get_quotes()
    all_topics=topics.get_topics()
    topic_id_int=int(topic_id)
    topic_name=topics.get_topic(topic_id)
    random_post_id=posts.get_random_post()
    usernames = users.get_usernames()
    if all_posts!=False:
        return render_template("topic.html", all_posts=all_posts, quotes=quotes, topics=all_topics, topic_name=topic_name, topic_id=topic_id_int, random_post_id=random_post_id, usernames=usernames)
    else:
        return render_template("topic.html")

 
@app.route("/edit_topics")
def edit_topics():
    all_topics=topics.get_topics()
    return render_template("edit_topics.html", topics=all_topics)


@app.route("/delete_topic", methods= {"get", "post"})
def delete_topic():
    topic_id = request.form["topic_id"]
    #users.check_csrf()
    try:
        topics.delete_topic(topic_id)
        return redirect("/edit_topics")
    except:
        return render_template("error.html")
        

@app.route("/create_topic", methods= {"get", "post"})
def create_topic():
    topic_name= request.form["topic"]
    #users.check_csrf()
    try:
        topics.create_topic(topic_name)
        return redirect("/edit_topics")
    except:
        return render_template("error.html")

@app.route("/quote",methods=["get", "post"])
def new_quote():
    if request.method == "GET":
        return render_template("quote.html")
        
    if request.method == "POST":
        content = request.form["content"]
        user_id=request.form["user_id"]
        #users.check_csrf()
        if content.isspace():
            return render_template("error.html", message="Allekirjoitus ei saa olla tyhjä.")
        if not users.set_quote(user_id, content):
            return render_template("error.html", message="Allekirjoituksen lisäys epäonnistui. Yritä myöhemmin uudelleen. ")

        return redirect("/")


    # Broken access control
@app.route("/delete_post/<int:post_id>",methods=["get", "post"])
def delete_post(post_id):
    print(post_id, file=sys.stderr)
    try:
        posts.delete_post(post_id)
    except:
     return render_template("error.html", message="Viestin poisto epäonnistui. Yritä uudelleen.")
        

        # Fix for access control, verify deletion by checking the user is right
        # and get the info using request.form


        #@app.route("/delete_post",methods=["get", "post"])
        #def delete_post():
            #users.check_csrf()
            #post_id = request.form["post_id"]
            #creator = posts.get_post_creator(post_id)[0]
            #userid = request.form["user_id"]
            #if creator != request.form["user_id"]:
            #    return render_template("error.html", message="Poisto epäonnistui.")
            #else:
                #try:
                #    posts.delete_post(post_id)
                #except:
                #    return render_template("error.html", message="Viestin poisto epäonnistui. Yritä uudelleen.")
        
    return redirect("/")

@app.route("/delete_comment",methods=["get", "post"])
def delete_comment():
    comment_id = request.form["comment_id"]
    post_id = request.form["post_id"]
    #users.check_csrf()
    try:
        comments.delete_comment(comment_id)
    except:
        return render_template("error.html", message="Kommentin poisto epäonnistui. Yritä uudelleen.")
        
    return redirect("/post/"+post_id)


@app.route("/new_comment",methods=["get", "post"])
def new_comment():
        content = request.form["content"]
        user_id=request.form["user_id"]
        post_id=request.form["post_id"]
        #users.check_csrf()
        if not len(content)>0 or content.isspace():
            return render_template("error.html", message="Kommentti ei saa olla tyhjä. Yritä uudelleen syötteellä.")
        if not comments.create_comment(content, True, user_id, post_id):
            return render_template("error.html", message="Kommentin lisääminen epäonnistui.")
        
        return redirect("/post/"+post_id) 

 
@app.route("/account", methods=["get", "post"])
def account():
    user_id=request.form["user_id"]
    if request.method == "GET":
        return render_template("account.html")

    if request.method == "POST":
        user_quote = users.get_quote_id(user_id)
        user_post_count = posts.get_posts_count_by_user(user_id)
        text_avg = posts.get_text_avg_by_user(user_id)
        return render_template('account.html', user_quote=user_quote, user_post_count=user_post_count, text_avg=text_avg)



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
