import praw
import json
from pymongo import MongoClient

def process_comments(comments):
    comment_data = []
    for comment in comments:
        if hasattr(comment, 'body'):
            comment_data.append({
                'id': comment.id,
                'body': comment.body,
                'author': comment.author.name if comment.author else None,
                'score': comment.score,
                'is_submitter': comment.is_submitter,
                'created_utc': comment.is_submitter,
                'replies': process_comments(comment.replies)
})  
    return comment_data


# Datos de la aplicación obtenidos en la configuración de la aplicación en Reddit
client_id = "a_QqUo5yPQJ8znecLQGo-Q"
client_secret = "rsv5KCOtNr7Vw__agoy891SSr0lL3Q"

username = "dsgarciaparra2020"

# Construcción del user_agent
user_agent = f"{username}:{client_id}:1.0 (by {username})"

# Crear una instancia de la clase Reddit con el user_agent
reddit = praw.Reddit(client_id=client_id, user_agent=user_agent, client_secret=client_secret)

# Utilizar la instancia de Reddit para acceder a la API y realizar acciones
# Por ejemplo, obtener información de un subreddit
subreddit = reddit.subreddit("StopUsingStatins")
#subreddit = reddit.subreddit("Cholesterol")
entries = []
subs = subreddit.hot(limit=500)

for submission in subs:
    entry = {
    "id": submission.id,
    "title": submission.title,
    "author": str(submission.author),
    "score": submission.score,
    "url": submission.url,
    "created_utc": submission.created_utc,
    "selftext": submission.selftext,
    "num_comments": submission.num_comments,
    "upvote_ratio": submission.upvote_ratio,
    "subreddit": str(submission.subreddit),
    "stickied": submission.stickied,
    "nsfw": submission.over_18,
    "is_self": submission.is_self,
    "locked": submission.locked,
    "is_original_content":submission.is_original_content,
    "author_flair_text":submission.author_flair_text,
    "clicked":submission.clicked,
    "distinguished":submission.distinguished,
    "edited":submission.edited,
    #"link_flair_template_id":submission.link_flair_template_id,
    "comments": process_comments(submission.comments),
    "link_flair_text":submission.link_flair_text,
    "locked":submission.locked,
    "name":submission.name,
    "over_18":submission.over_18,
    "permalink":submission.permalink,
     "saved":submission.saved,
    "spoiler":submission.spoiler
    }
    
    entries.append(entry)
    print ("Se proceso el documento #" + str(len(entries)))

# Convertir las entradas a formato JSON
json_entries = json.dumps(entries, indent=4)


# Conecta con la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['subreddits']
collection = db['subreddits']
collection.insert_many(json.loads(json_entries))