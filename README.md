"diamond" Project
=================  
This project was made in "Python Extreme" course.  
The course was directed by John Bryce & Israel Innovation Authority  
The project uses
  1.  Windows 10 (can run on mac or any other Linux distribution with a few proprait changes)
  2.  python 3.9.6
  3.  MySQL 5.7.35
  4.  Docker Desktop And Docker Compose
  5.  Microsoft Azure cloude servicess

The project is delivered by: 
  Avi Barouch
  Andreas Moskovits



Installation for debug purpuses.
===========================================
A.  Install python version 3.95
B.  Download the progect from https://github.com/avibarouch/diamonds to a folder on your machine
C.  In the folder of the project on your machine run:
      1.  python -m venv env
      2.  env\Scripts\activat
      3.  pip install -r reuirements.txt 
D.  Download and install MySQL server version 5.7.35 
      1.  Open https://dev.mysql.com/downloads/windows/installer/5.7.html
      2.  Run MySQL Installer (its pre requizist Microsoft Visual Studio installaed)
      3.  Click Add 
      4.  From "Available Products" choose: MySQLServers > MySQLServer
                                            MySQLServer 5.7.35
      5   Press on the: ->   
      6.  Mark the check box "Enable the SelectFetures..."
      7.  Press the button Next
      8.  Press the button Execute to download MySQL Server 5.7.35
      9.  On "Select Feature To Install" press the button Next to install all product fetures
      10.  On "Instalatin" window press the button Execute and let the instalation begin
      11.  When the installatin end press the button Next
      12.  On the configuration press the button next
      13.  On "Accounts and Roles" window:
           A.  Mysql Root Password: root5464^%$GHFD&^*nbvn
           B.  Press the button "Add User" and specify:
               1.  User Name:  dp_db_user
               2.  Host:       localhost
               3.  Role:       DB Admin
               4.  password:   hgf675*&^hgf435
           C. Press the button Next
      14.  On Windows Service press Next
      15.  On Apply configuration
           A. press the button Execute
           B. press the button Finish

A.  In order to run this project in your machine natively:  
    Perform the following commands:  
    1. Open a terminal window  
    2. Change directory to where the project lives 
    3. Execute this command: python app.py  
    4. Open the browser and go to: http://localhost:5000/  
    5. Don't forget, when finished, go to terminal and press CTRL+C to quit  


c.  For debug purpuses you can work with the database natively.
    1.  Download and install MySQL  5.7.35 .
        Find it on https://dev.mysql.com/downloads/windows/installer/5.7.html

d.  The project can run the database on Docker.
    To work with the Docker natively :
    1.  Install on your mashine Docker Desktop and Docker Compose
    1.  Download to your mashine MySQL Installer 5.7.35 .
        Find it on https://dev.mysql.com/downloads/windows/installer/5.7.html
    2.  From the terminall (where The yml file live) run: docker compose up
    3.  To be continue...

B.  In order to run this project on your machine:  
    Perform the following commands:  
    1. Install docker Desktop (if it is not installed already)  
    2. Open a terminal window  
    3. Change directory to where the project lives  
    4. Execute this command: docker build . -t proj:70  
    5. Execute this command: docker run -p 5000:5000 proj:70  
    6. Access http://localhost:5000 via browser


