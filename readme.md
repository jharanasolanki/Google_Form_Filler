# Google Form Filler

This script will create an HTML Form which has the same elements as the Google Form.
On Submitting the HTML form the response will be submitted to the Google Form as well.
The script can be tweaked for sending the same response multiple times.

# Execution

>>python3 formweb.py urlid

urlid is the part of the form link between "https://docs.google.com/forms/d/e/" and "/formResponse" 

Open sample.html on the browser, enter the data and submit.
It will show form submitted.


# File Path

In xampp folder, the formweb.py and formsubmit.py is stored in cgi folders.
In htdocs of xampp, there is another folder FlaskApp which will have the sample.html
