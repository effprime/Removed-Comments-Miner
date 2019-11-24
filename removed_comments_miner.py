"""Module for mining removed comments from a Reddit Moderator log
"""
import json
import logging
import praw

class RemovedCommentsMiner:
    """The miner class
    """

    def __init__(self, client_id, client_secret, username, password, application_name="Null"):
        """Starts the Mining instance

        args:
            client_id (str): The Reddit API app ID
            client_secret (str): The Reddit API app secret
            username (str): Reddit username
            password (str): Reddit password
            application_name (str): Reddit APP name
        """
        self.logger = logging.Logger(__name__)
        self.logger.setLevel(logging.INFO)
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            user_agent=application_name,
            username=username
        )
        logging.info(f"Logged in as user {self.reddit.user.me()}")

    def mine(self, subreddit, comments=10, include_automod=False):
        """Mines removed comments from a Moderator log

        args:
            subreddit (str): The Subreddit name
            comments (int): The number of comments to mine
            include_automod (bool): Whether or not to include AutoMod removals

        returns:
            Dict: The mined comment data
        """
        if not subreddit:
            raise "No Subreddit name provided"
        if not isinstance(comments, int) or int <= 0:
            raise "Comments must be an integer greater than 0"
        if not isinstance(include_automod, bool):
            raise "include_automod must be a boolean"
        if comments >= 500:
            limit = 500
            remaining_comments = comments % limit
            loops = int(comments/limit)
            if remaining_comments:
                loops += 1
        else:
            limit = comments
            loops = 1
            remaining_comments = 0
        params = {
            "type": "removecomment",
            "after": None,
            "limit": limit
        }
        comment_json = {}
        comment_json["removed_comments"] = []
        for step in range(1, loops+1):
            self.logger.info(f"Running request loop {step}")
            response = self.reddit.request(
                method="GET",
                path=f"/r/{subreddit}/about/log",
                params=params
            )
            if step != loops:
                params["after"] = response["data"]["after"]
            response = response["data"]["children"]
            for comment in response:
                if not include_automod:
                    if comment["data"]["mod"] == "AutoModerator":
                        continue
                comment_json["removed_comments"].append(comment["data"]["target_body"])
            if step == loops-1 and remaining_comments:
                params["limit"] = remaining_comments
        return comment_json

    def mine_to_file(self, subreddit, comments=10, include_automod=False, filename="minedcomments"):
        """Mines removed comments from a Moderator log and saves them to a JSON file

        args:
            subreddit (str): The Subreddit name
            comments (int): The number of comments to mine
            include_automod (bool): Whether or not to include AutoMod removals
            filename (str): the JSON filename

        returns:
            bool: Whether or not the file was written successfully
        """
        if not isinstance(filename, str):
            raise "File name must be a string"
        comment_json = self.mine(subreddit, comments, include_automod)
        with open(f"{filename}.json", "w+") as json_file:
            json.dump(comment_json, json_file, indent=4)
        return True
