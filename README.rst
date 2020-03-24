Forklift
====

.. image:: https://img.shields.io/github/license/arianrhodsandlot/Forklift.svg
  :target: https://github.com/arianrhodsandlot/Forklift/blob/master/LICENSE.txt

.. image:: https://img.shields.io/circleci/project/github/arianrhodsandlot/Forklift.svg
  :target: https://circleci.com/gh/arianrhodsandlot/Forklift

|

.. contents::
  :local:

Overview
--------
Forklift is a sticker bot for WeChat group. Tell it a WeChat group name and login with a WeChat account, it will reply a series of stickers from some certain websites when someone in that group send a request to it.


Usage
-----
1. Clone this repository!

   .. code-block:: sh

    git clone https://github.com/arianrhodsandlot/Forklift.git
    cd Forklift

2. Make sure you have `Pipenv <https://pipenv.readthedocs.io/en/latest/>`_ installed, then setup dependencies!

   .. code-block:: sh

    pipenv install

3. Tell Forklift the group name you specified!

   .. code-block:: sh

    echo 'FORKLIFT_CHATROOM_NAME=__REPLACE_ME_WITH_YOUR_OWN__' >> .env

4. Run!

   .. code-block:: sh

    pipenv run start

Detail
------
Forklift fetches results from following sites:

- https://www.fabiaoqing.com
- https://www.google.com/imghp

Thank you above!

Here are how it works:

1. If a keyword received by Forklift is a predefined tag in this `tag wall <https://fabiaoqing.com/tag>`_ , Forklift will pick three stickers from a random page of the tag's index page.
2. Otherwise it will perform a search using Google Images.

License
-------
MIT
