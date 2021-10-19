# ckanext-upgrade-dataset

This CKAN extension includes `media_wiki` plugin that aim to able users to link machines on semantic media wiki to resources/datasets in CKAN.



## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
|  2.9 | Yes    |
| earlier | No |           |



## Installation

To install ckanext-upgrade-dataset:

1. Activate your CKAN virtual environment, for example:

        source /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv (Suggested location: /usr/lib/ckan/default/src)
:

        git clone https://github.com//ckanext-upgrade-dataset.git
        cd ckanext-upgrade-dataset
        pip install -e .
        pip install -r requirements.txt

3. Add `media_wiki` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. (For `media_wiki`) Upgrade the CKAN database to add the plugin table:

        ckan -c /etc/ckan/default/ckan.ini db upgrade -p media_wiki


4. Restart CKAN and supervisor. For example if you've deployed CKAN with nginx on Ubuntu:

        sudo service nginx reload
        sudo service supervisor reload



## Developer installation

To install ckanext-upgrade-dataset for development, activate your CKAN virtualenv and
do:

    git clone https://github.com//ckanext-upgrade-dataset.git
    cd ckanext-upgrade-dataset
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini  --disable-pytest-warnings  ckanext/upgrade_dataset/tests/


