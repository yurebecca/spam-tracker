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

## To do:
* [-] Keyword stuffing check
* [-] Tests for the checks
* [-] Add logging
* [-] Identified issue: email spam as training data marks has a high chance to score everything as spam...
    * Will need new data to train the spam checker

## Challenges
1. Short content has a high chance to skew the severity to higher numbers for the other checks.
    * Possible solutions:
        * [-] Check the content's length first and skip other checks if it doesn't pass minimum requirements
        * [x] Do all the checks but use the rating for short content as the final rating instead of the highest rating
2. Keyword stuffing will be hard to spot (because we can't just count each word's occurance ...)
    * Possible solutions:
        * [x] Have a list of keywords to look out for, and just spot these 
3. There is no way to get an idea of how many projects there are from the API, or which ids don't exist ...
    * Possible solutions:
        * [x] Use a while toop to check for 404 HTTP status, when encountered we stop
            * We can let the user decide the range of project ids (will be implemented later)
