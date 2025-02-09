# Created by Raghu Acc Rullx Boy ❤️

from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

# Function to Post Comment on Facebook
class FacebookCommenter:
    def __init__(self):
        self.comment_count = 0

    def comment_on_post(self, cookie, post_id, comment):
        with requests.Session() as r:
            r.headers.update({
                'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-G960U)',
                'accept-language': 'en-US,en;q=0.9',
                'Host': 'mbasic.facebook.com',
            })

            response = r.get(f'https://mbasic.facebook.com/{post_id}', cookies={"cookie": cookie})
            next_action = re.search('method="post" action="([^"]+)"', response.text)
            fb_dtsg = re.search('name="fb_dtsg" value="([^"]+)"', response.text)
            jazoest = re.search('name="jazoest" value="([^"]+)"', response.text)

            if not (next_action and fb_dtsg and jazoest):
                return "Invalid Post ID or Cookie."

            data = {
                'fb_dtsg': fb_dtsg.group(1),
                'jazoest': jazoest.group(1),
                'comment_text': comment,
                'comment': 'Submit',
            }

            post_url = f"https://mbasic.facebook.com{next_action.group(1).replace('amp;', '')}"
            response2 = r.post(post_url, data=data, cookies={"cookie": cookie})

            if 'comment_success' in response2.url:
                self.comment_count += 1
                return f"✅ Comment {self.comment_count} Posted Successfully!"
            else:
                return f"❌ Failed to Post Comment."

# HTML + CSS + JavaScript Combined
form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comment Bot by Raghu Acc Rullx Boy ❤️</title>
    <style>
        body {
            background-color: #000;
            color: yellow;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        input, button {
            margin: 10px;
            padding: 10px;
            width: 80%;
            max-width: 300px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            background-color: yellow;
            color: black;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: orange;
        }
        .message {
            color: cyan;
            font-size: 1.2em;
        }
    </style>
    <script>
        function validateForm() {
            const postId = document.forms["commentForm"]["post_id"].value;
            const cookie = document.forms["commentForm"]["cookie"].value;
            const comment = document.forms["commentForm"]["comment"].value;
            const date = document.forms["commentForm"]["comment_date"].value;

            if (postId === "" || cookie === "" || comment === "" || date === "") {
                alert("All fields are required!");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>
    <h1>Comment Bot by Raghu Acc Rullx Boy ❤️</h1>
    <form name="commentForm" method="POST" onsubmit="return validateForm()">
        Post UID: <input type="text" name="post_id" placeholder="Enter Post ID" required><br>
        Cookie: <input type="text" name="cookie" placeholder="Enter Your Cookie" required><br>
        Comment: <input type="text" name="comment" placeholder="Write Your Comment" required><br>
        Date: <input type="date" name="comment_date" required><br>
        <button type="submit">Submit</button>
    </form>
    <p class="message">{{ message }}</p>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        post_id = request.form['post_id']
        cookie = request.form['cookie']
        comment = request.form['comment']
        comment_date = request.form['comment_date']

        if post_id and cookie and comment and comment_date:
            commenter = FacebookCommenter()
            message = commenter.comment_on_post(cookie, post_id, f"{comment} (Date: {comment_date})")
        else:
            message = "⚠️ Please fill all fields."

    return render_template_string(form_html, message=message)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
