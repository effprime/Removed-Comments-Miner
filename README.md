# Removed-Comments-Miner
Python module for mining removed comments from a Reddit Moderator log

* Import the Module with `import removed_comments_miner`
* Start the miner with `miner = RemovedCommentsMiner(**kwargs)`
  * The following arguments are needed:
    * client_id (str): The Reddit API app ID  (see [here](https://www.reddit.com/prefs/apps))
    * client_secret (str): The Reddit API app secret (see [here](https://www.reddit.com/prefs/apps))
    * username (str): Reddit username
    * password (str): Reddit password
    * application_name (str): Reddit APP name (defaults to "Null")
* Get mining results as dictionary `data = miner.mine(**kwargs)`
  * The following arguments are needed:
    * subreddit (str): The Subreddit name
    * comments (int): The number of comments to mine
    * include_automod (bool): Whether or not to include AutoMod removals
* You can also use `miner.mine_to_file(**kwargs)` with an additional `filename` argument
