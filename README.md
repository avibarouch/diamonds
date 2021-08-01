"# JBProject"
This project was made in "Python Extreme" course.
The course was directed by John Bryce & Israel Innovation Authority

The project is delivered by:
  Avi Barouch
  Andreas Moskovits

A.  In order to run this project in your machine natively:
    Perform the following commands:
    1. Open a terminal window
    2. Change directory to where the project lives 
    3. Execute this command: python app.py
    4. Open the browser and go to: http://localhost:5000/  
    5. Don't forget, when finished, go to terminal and press CTRL+C to quit  

B.  In order to run this project on your machine:  
    Perform the following commands:  
    1. Install docker Desktop (if it is not installed already)  
    2. Open a terminal window  
    3. Change directory to where the project lives  
    4. Execute this command: docker build . -t proj:70  
    5. Execute this command: docker run -p 5000:5000 proj:70  
    6. Access http://localhost:5000 via browser  
