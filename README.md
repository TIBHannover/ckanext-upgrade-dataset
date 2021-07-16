# ckanext-upgrade-dataset

This CKAN extension includes plugin(s) that aim to extends the functionalities related to dataset (package) in CKAN. 

**Included plugin(s)**:

| Plugin    | Description   |
| --------------- | ------------- |
|  **media_wiki** | This plugin  ables users to link machines on semantic media wiki to resources/datasets in ckan.    |
| **group_ownership** | The plugin adds an extra step for adding the dataset to a group in ckan and set the owner organization while creating a dataset.           |
| **link_publication** | The plugin ables users to link publication(s) to a dataset via the doi url. It fetches the publication metadata from the crossref API.|



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
        cd ckanext-multiuploader
        pip install -e .
        pip install -r requirements.txt

3. Add `media_wiki` and/or `group_ownership` and/or `link_publication` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. (For `media_wiki` and `link_publication`) Upgrade the CKAN database to add the plugin table:

        ckan -c /etc/ckan/default/ckan.ini db upgrade -p media_wiki

        ckan -c /etc/ckan/default/ckan.ini db upgrade -p link_publication

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


