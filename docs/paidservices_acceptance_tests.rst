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

Learner may submit questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Goal

        Verify a learner with enough credits and a service expiry date in the future can submit questions up to the amount specified by their 'credits'.

    Prerequisites

        The learner has enough credits.

        The service expiry date is in the future.

    Steps

        Create a new 'learner' user by registering.

        Activate the new account by following the instructions in the email.

        Navigate to http://qa.everthingmaths.co.za

        Log in with the chosen credentials.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the blue area labelled 'Premium services'.

        Validate that the learner has 2 questions to ask.

        Scroll to the bottom of the page.

        Validate that the text area labelled 'Question' is visible on the page.

        Enter your question in this text area.

            Use non-ASCII characters in your question too.

        Click on 'Submit'.

        Validate that the text you entered is no displayed on the page.

        Click on the 'Premium Services' link and validate that the learner now has one credit less.


Learner may not submit questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal
        
        Verify a learner without credits or with a service expiry date in the past cannot submit questions.

    Prerequisites
        
        You execute the acceptance test 'Learner may submit questions' successfully.

        You stayed on the same page (no logout or browsing around)

    Steps

        Enter another question.

        Click on the 'submit' button.

        Validate that your new question appears on the page.

        Validate that the question text area disappears from the page.

        Click on the 'Premium services' link.

        Validate that the number of questions now is 0.


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

        The learner's 'ask-questions' service has not expired.

        The learner has no more credits left.

    Steps

        Navigate to http://qa.everthingmaths.co.za

        Log in with the chosen learner's credentials.

        Navigate to: http://qa.everythingmaths.co.za/grade-10/01-algebraic-expressions/01-algebraic-expressions-01.cnxmlplus

        Click on the 'Premium Services' link.

        Validate that the learner has 0 questions left.

        Validate that the question text area is not displayed.

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

Learner buys more credits
~~~~~~~~~~~~~~~~~~~~~~~~~

    Goal

    Prerequisites

    Steps

