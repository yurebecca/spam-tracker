# spam-tracker
A simple python application created to flag spam/abuse with a severity ranging from 0 to 10 (10 = not safe for human eyes).

This application will call an API to get a json object with at least the following fields:

```
GET /projects/<project_id>/
{
    "name": <string>
    "description": <string>,
    "blurb": <string>
}
```

## Requirements
Required to have the following installed
```
python3
pip3
brew
hunspell (brew install hunspell)
zeromq  (brew install zeromq)
pkgconfig (brew install pkgconfig)
```

`hunspell` may cause a bit of issues on a Mac, which can be solved if following these:

https://github.com/blatinier/pyhunspell/issues/26

https://github.com/blatinier/pyhunspell/issues/33

## Good to know
1. Install python dependencies with `sh script/install.sh`.

2. Test with `pytest -v`.

3. Run the flask application with `sh script/start.sh`.

4. API endpoint: GET http://localhost:5000/tracker/bulk

## To do:
* [x] Setup a simple way to call the function
    * Using flask and created an API to get the function running
* [x] Make a simple check for profanity and get it working first
    * Severity is measured in percentage (%) of the whole text; 5% allowed and has a severity of 3. Increased % of profanity will raise the severity (these settings can be modified)
* [x] Check for short content
    * Content is considered short if less than 100 words (can be modified)
    * Whole content includes the following:
        * `name`
        * `blurb`
        * `description`
        * all `milestones.name`
        * all `milestones.description`
* [x] Set up spam checker
    * Needs training data (currently using spam emails, which doesn't seem too effective)
    * **Notes**: 
        * Needs to be trained with new data. It may be turned off.
        * Has a chance to mark 'good' project content as spam (with the trained email data there is a 2/140 = ~1.43% chance of marking Ham emails as Spam).
* [x] Improve performance of spam checker
    * Spam checker is getting trained each time the API is called, which is too expensive.
    * Found a way to save the trained checker in `pickle`.
    * Each time the Spam checker needs to be used, just load the trained version.
* [x] Add a setting to turn off specific checks
* [x] Add Tests for the checks
* [x] Add logging
    * Re-using Flask's `app.logger`
* [x] Keyword stuffing check
    * Possible keywords will be found with an algorithm
    * Keyword's safezone (not considered to be keyword stuffing) varies between 2-10% of the entire text.
    * **Notes**: 
        * Needs to be trained with new data. It may be turned off.
        * Currently trained with stackoverflow data (programming topic), so it may fail to catch the correct keywords.

## Enhancements:
* [ ] Add command-line capabilities, so the task can be done as a cron job
* [ ] Allow user to specify the range of project ids to go through
    * These will be added to a Message Queue and child services will rate each project listed in the MQ (Scalability Enhancement)
* [ ] Scalability Enhancement: Use something like RabbitMQ to queue up what needs to be processed.
* [x] ~~Identified issue: email spam as training data marks has a high chance to score everything as spam...~~
    * ~~Will need new data to train the spam checker~~
    * [Fixed] Marked all data as spam due to coding error.

## Challenges
1. Short content has a high chance to skew the severity to higher numbers for the other checks.
    * Possible solutions:
        * [ ] Check the content's length first and skip other checks if it doesn't pass minimum requirements
        * [x] Do all the checks but use the rating for short content as the final rating instead of the highest rating
2. Keyword stuffing will be hard to spot (because we can't just count each word's occurance ...)
    * Possible solutions:
        * [ ] Have a list of keywords to look out for, and just spot these
        * [x] Find an algorithm that can make a guess
3. There is no way to get an idea of how many projects there are from the API, or which ids don't exist ...
    * Possible solutions:
        * [x] Use a while loop to check for 404 HTTP status, when encountered we stop
            * Enhancement: We can let the user decide the range of project ids (will be implemented later)
