=============================================
Everything Maths and Science Acceptance Tests
=============================================

Contents

.. toctree::
   :maxdepth: 2

------------------------------
Paid services acceptance tests
------------------------------

    General prerequisites:

        The learner has logged in to the EMAS system with an account that has the 'Member' role.

Learner may not submit questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal
        
        Verify a learner without credits or with a service expiry date in the past cannot submit questions.

    Prerequisites
        

    Steps

        Create a new 'learner' user by registering.

        Activate the new account by following the instructions in the email.

        Navigate to http://qa.everthingmaths.co.za

        Log in with the chosen credentials.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the blue area labelled 'Premium services'.

        Validate that there is a link labelled 'Order' visible.

        Scroll to the bottom of the page.

        Validate that there is no text area labelled 'Question' visible on the page.

Learner buys credits via EFT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal
        
        To validate that a learner can buy credits.

    Prerequisites
        
        The learner has logged in to the EMAS system with an account that has the 'Member' role.

    Steps

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the blue area labelled 'Premium services'.

        Click on the link labelled 'Order'.

        Validate that an page with order options is displayed.

        Enter the amount '1' in the text area below the label 'Science Grade 10 Questions'.

        Click on the button labelled 'SUBMIT'.

        Validate that an order confirmation page labelled 'Place Order' is displayed.

        Click on the button labelled 'Confirm Order'.

        Validate that a page titled 'Payment details' is displayed.

        Validate that a button labelled 'Proceed to Payment' is visible.

        Validate that a set of bank account details is visible.

        In a different browser, log in as 'Site Administrator'.

        Navigate to the 'Orders' folder.

        Find the relevant new order.

        Change the selected order's state to 'paid' via the state drop-down.

        Navigate to the 'Member services' folder.

        Validate that a new memberservice was created and that it is related to the service initially selected, 'Science Grade 10 Questions'.

        Go back to the browser where you are logged in as the learner.

        Navigate to 'Science Grade 10'.

        Validate that there is a text area for entering questions on the page.

        Click on the blue area labelled 'Premium services'.

        Validate that the logged in learner now has 10 credits for asking questions.

        
Learner buys credits via VCS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal
        
        To validate that a learner can buy credits via VCS credit card integration.

    Prerequisites
        
        The learner has logged in to the EMAS system with an account that has the 'Member' role.

    Steps

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the blue area labelled 'Premium services'.

        Click on the link labelled 'Order'.

        Validate that an page with order options is displayed.

        Enter the amount '1' in the text area below the label 'Maths Grade 10 Questions'.

        Click on the button labelled 'SUBMIT'.

        Validate that an order confirmation page labelled 'Place Order' is displayed.

        Click on the button labelled 'Confirm Order'.

        Validate that a page titled 'Payment details' is displayed.

        Validate that a button labelled 'Proceed to Payment' is visible.

        Validate that a set of bank account details is visible.

        Click on the button labelled 'Proceed to Payment'

        Complete the VCS credit card details and click 'Submit'.

        Validate that the a payment confirmation page is displayed.

        In a different browser, log in as 'Site Administrator'.

        Navigate to the 'Orders' folder.

        Find the relevant new order.

        Validate that the order's state is 'paid'.

        Navigate to the 'Member services' folder.

        Validate that a new memberservice was created and that it is related to the service initially selected, 'Maths Grade 10 Questions'.

        Go back to the browser where you are logged in as the learner.

        Navigate to 'Maths Grade 10'.

        Validate that there is a text area for entering questions on the page.

        Click on the blue area labelled 'Premium services'.

        Validate that the logged in learner now has 10 credits for asking questions.
        

Learner may submit questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Goal

        Verify a learner with enough credits can submit questions up to the amount specified by their 'credits'.

    Prerequisites

        The learner has enough credits. (see test above about buying credits)

    Steps

        Navigate to http://qa.everthingmaths.co.za

        Log in with the credentials of the learner you created above.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the blue area labelled 'Premium services'.

        Make a note of how many credits the learner has for asking questions.

        Scroll to the bottom of the page.

        Validate that the text area labelled 'Question' is visible on the page.

        Enter your question in this text area.

            Use non-ASCII characters in your question too.

        Click on 'Submit'.

        Validate that the text you entered is now displayed on the page.

        Click on the 'Premium Services' link and validate that the learner now has one credit less.


Learner can delete an unanswered question
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

        Validate that a learner can delete an unanswered question he added.

    Prerequisites

        The question has never been answered.

    Steps

        Navigate to http://qa.everthingmaths.co.za

        Log in with the chosen credentials.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the 'Premium Services' link.
        
        Make a note of how many questions the learner has left.

        Scroll to the questions you added in the tests above.

        Validate that there is a 'Delete' button on each of your unanswered questions.

        Click on the delete button of your last question.

        Validate that the question disappears from the page.

        Click on the 'Premium Services' link.

        Validate that the learner now has one more question to ask.

Learner cannot delete a question she did not add
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

        Validate that a learner cannot delete a question she did not add.

    Prerequisites

        You added a question as a different learner at http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

    Steps

        Navigate to http://qa.everthingmaths.co.za

        Log in with the chosen credentials.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Scroll down to the relevant question.

        Validate that there is no delete button on the relevant question.

Learner cannot delete an answered question
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

        Verify the leaner cannot delete a question he added once an answer has been given on that question.

    Prerequisites

        The question has at least one answer.

    Steps

        Navigate to http://qa.everthingmaths.co.za

        Log in with credentials that will allow you to answer questions.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Pick one of the questions of your test learner and add an answer.

        Log out.

        Log in with the chosen learner's credentials.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Scroll down to the relevant question.

        Validate that there is no delete button on the relevant question.

Learner has access to answers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

        Validate a learner always has access to questions for which she paid.

    Prerequisites

        The learner has no more credits left.

    Steps

        Navigate to http://qa.everthingmaths.co.za

        Log in with the chosen learner's credentials.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the 'Premium Services' link.

        Validate that the learner has 0 questions left.

        Validate that the question text area is not displayed.

        Validate the you can still see the questions and answers you previously entered for this learner.





TO BE DONE:


Learner cannot access answers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

        Validate that a learner has no access to his questions once his service subscription has expired.

    Prerequisites

    Steps

Learner has access to intelligent exercise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

    Prerequisites

    Steps

Learner cannot access intelligent exercise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

    Prerequisites

    Steps

Learner has restricted access to intelligent exercise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

    Prerequisites

    Steps

