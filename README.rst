A170
====

.. image:: https://img.shields.io/github/license/arianrhodsandlot/A170.svg
  :target: https://github.com/arianrhodsandlot/A170/blob/master/LICENSE.txt

.. image:: https://img.shields.io/circleci/project/github/arianrhodsandlot/A170.svg
  :target: https://circleci.com/gh/arianrhodsandlot/A170

|

.. image:: https://user-images.githubusercontent.com/10987902/50162031-4730f500-0318-11e9-85c6-68f154912b80.jpg
  :width: 100%

.. contents::
  :local:

Overview
--------
A170 is a sticker bot for WeChat group. Tell it a WeChat group name and login with a WeChat account, it will reply a series of stickers from some certain websites when someone in that group send a request to it.


Usage
-----
1. Clone this repository!

   .. code-block:: sh

    git clone https://github.com/arianrhodsandlot/A170.git
    cd A170

2. Make sure you have `Pipenv <https://pipenv.readthedocs.io/en/latest/>`_ installed, then setup dependencies!

   .. code-block:: sh

    pipenv install

3. Tell A170 the group name you specified!

   .. code-block:: sh

    echo 'A170_CHATROOM_NAME=__REPLACE_ME_WITH_YOUR_OWN__' >> .env

4. Run!

   .. code-block:: sh

    pipenv run start

Detail
------
A170 fetches results from following sites:

- https://www.fabiaoqing.com
- https://www.google.com/imghp

Thank you above!

Here are how it works:

1. If a keyword received by A170 is a predefined tag in this `tag wall <https://fabiaoqing.com/tag>`_ , A170 will pick three stickers from a random page of the tag's index page.
2. Otherwise it will perform a search using Google Images.

License
-------
MIT
