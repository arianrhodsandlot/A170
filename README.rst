A170
====

.. contents::
   :local:

Overview
--------
A170 is a sticker bot for WeChat group. Setup with a WeChat group name and login with a WeChat account, it will reply with a series of stickers from some certain websites when someone send a request.


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

A170's name comes from *NieR: Automata*. In that worldview, "A170" is the name of a Pod Program, which can be used to find rare materials.

License
-------
MIT
