### Test scripts

#### Assumes virtualenv and virtualenvwrapper

#### Start wrapper

```
mkvirtualenv dv-selenium-test
pip install -r requirements/base.txt
```

#### Run User 1

```
python dv_browser.py
```

Should see something like:

```
Please run with one of the choices below:

 1 - run_user_pete
 2 - run_user_another_user

example:
$ python dv_browser.py 1
```

- Run the script as the first user

```
python dv_browser.py 1
```

#### Run User 2

- Open a new terminal 

```
cd ~/selenium-helper
workon dv-selenium-test
python dv_browser.py
```

- Choose another user. e.g.:

```
python dv_browser.py 2
```

#### Edit/Add more users

- Add another function simiar to [```run_user_pete```](https://github.com/IQSS/selenium-helper/blob/master/dv_browser.py#L160)
- Include this function in the [```user_choices```](https://github.com/IQSS/selenium-helper/blob/master/dv_browser.py#L176) dict at the bottom of the file