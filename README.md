# Phlipcart

## CS 1202 Advanced Programming: E-Commerce Website Project

### by [Bhavye Jain](https://github.com/bhavye2003), [Ishan Jain](https://github.com/ishanjain23) and [Aniruddh Bhaskaran](https://github.com/LaserTrajectory)

#### Tech Stack: 

- Back-end: Django 3.2.8
- Database: SQLite3 (Django default DB)
- Django HTML Templates with BootstrapCSS on top

#### Contribution outline

- Bhavye:
  - Front-end design strategy
  - Cart, wishlist, view products pages' HTML and CSS
  - Website layout and structure

- Ishan:
  - Profile, search products, home pages' HTML and CSS
  - Back-end view logic for home page and order summary page
  - Product view backend implementation
  
 - Aniruddh:
    - User authentication, wishlist & cart backend implementation
    - Profile page, checkout, order summary pages' HTML and CSS
    - Database setup + data model implementation  
    - Fuzzy matching + "more like this" recommendation implemenations


#### Project setup details

GitHub Desktop 

Click on code and click “Open with GitHub Desktop” (if you don’t have GitHub Desktop installed, please install it from here: https://desktop.github.com)

It will open GitHub Desktop and then show you a popup with the url of the repo and the button “Clone” underneath it. Choose the Local Path you want for the repo and then click “Clone”. 

After the repo has been cloned, it will show a page with a few options, one of which is to “Open the repository in your external editor” and a button with your default editor. You can change this editor in Settings (we recommend opening this repo in VSCode, so change your default editor inside GitHub Desktop to VSCode, and then click the “Open the repository in your external editor” button).

When you do this, VSCode may ask if you trust the authors of the files in this folder. Click “Yes, I trust the authors” to proceed.

Then hit Ctrl + ~ to open VSCode’s Terminal. 

Note: If you’re on a Mac, you can skip the next few steps on creating a virtual environment. Simply type “source bin/activate” and our virtual environment will open up for you. Check that all the requirements are installed by typing “pip install -r requirements.txt”. 

Next, if you’re on Windows, create a virtual environment using the command “python3 -m venv <env_name>”. You can give your virtual environment any name you like. 

Once you do this, VSCode will ask if you want to select this virtual environment for the workspace folder. Click Yes. 

Then, install all the requirements by typing “pip install -r requirements.txt”. Wait for the dependencies to install and then type “python3 manage.py runserver” and wait for it to load. It will then show a url, something like http://127.0.0.1:8000. Copy this url and paste it in the browser. And then you can check out Phlipcart!
