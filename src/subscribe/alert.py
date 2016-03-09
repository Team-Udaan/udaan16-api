import requests
from src.base import BaseHandler


class AlertHandler(BaseHandler):

    def send_mail(self, text, image, image_name):
        return requests.post(
            "https://api.mailgun.net/v3/sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org/messages",
            auth=("api", "key-a0bd92feef0ccecb07f199b770449917"),
            files=[("inline", image)],
            data={
                "from": "Mailgun Sandbox <postmaster@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org>",
                "to": "<list@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org    >",
                "subject": "Hello Udaan",
                "text": text,
                "html": '<html>Inline image here: <img src="cid:' + image_name + '"></html>'
                }
            )

    def post(self, *args, **kwargs):
        # TODO
        # 1) save the messages to local database
        # 2) Allow users to add subject along with text
        # 3) Send the mail to mailing lists
        file = self.request.files['image'][0]
        file_name = file["filename"]
        image = file['body']
        text = self.get_argument("text")
        print(self.send_mail(text, image, file_name))
