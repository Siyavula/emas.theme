===========================
EasyNewsletter introduction
===========================

Where are my newsletters?
~~~~~~~~~~~~~~~~~~~~~~~~~
The toplevel folder 'newsletters' holds them. Look at the newsletter, 
'everything-news'.

All the newsletters are in:
http://qa.emas.siyavula.com/newsletters

The current default newsletter is:
http://qa.emas.siyavula.com/newsletters/everything-news

Why do I have this 'everything-news'?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the newsletter setup or configuration. It contains all the newsletter
issues. You set the default template, subscribers, test address, etc. on this
item. All newsletter issues will use these settings unless you change them on
the newsletter issue itself.

You can think of 'everything-news' as the place that keeps all the actual
newsletter issues. One cannot send this top-level item, it only contains basic
configuration settings.

Have a look at:
http://qa.emas.siyavula.com/newsletters/everything-news/edit

How to add a newsletter issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Browse to:
http://qa.emas.siyavula.com/newsletters/everything-news

Click on the 'Add new' link and select 'Issue'.

Complete the form and hit 'Save'.

Help, I have created a new issue and now it is gone!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First, don't panic. If you saved this new issue at any time, it will be in
everything-news. Simple browse to:
http://qa.emas.siyavula.com/newsletters/everything-news/

Now click on the link titled 'Drafts'. Voila! There is your list of draft
newsletter issues. Click on the relevant newsletter issue and continue editing.

How to add a member to the subscribers list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Browse to:
http://qa.emas.siyavula.com/newsletters/everything-news

Click on 'Edit'.

Scroll down to the label, 'Plone Members to receive the newsletter'.
Now hold the 'CTRL' key and click on the relevant non-selected member.

When you are done hit 'Save' at the bottom of the page.

Hint:
You can select as many members as you want now, just remember to keep the 'CTRL'
key pressed.

If things go wrong, just hit the 'Cancel' button at the bottom of the page and
restart the process.

How to remove a member from the subscribers list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Browse to:
http://qa.emas.siyavula.com/newsletters/everything-news

Click on 'Edit'.

Scroll down to the label, 'Plone Members to receive the newsletter'.
Now hold the 'CTRL' key and click on the relevant currently selected member.

When you are done hit 'Save' at the bottom of the page.

Hint:
You can deselect as many members as you want now, just remember to keep the 'CTRL'
key pressed.

If things go wrong, just hit the 'Cancel' button at the bottom of the page and
restart the process.

How to send the newsletter issue to a test email address
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We assume that this is a newsletter issue that has not been sent and as such is
still in 'draft' state.

Browse to:
http://qa.emas.siyavula.com/newsletters/everything-news

Click on 'Drafts' and select the relevant newsletter issue.

Hit the link titled, 'Send'.

Fill in the test email address on the line below the label 'Test email' and hit 
the 'Test Newsletter' button.

How to send the newsletter to all subsribers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*WARNING* 
This will send the newsletter issue to *ALL* the subscribers, so make sure this
is really what you want to do!
*WARNING* 

Browse to:
http://qa.emas.siyavula.com/newsletters/everything-news

Click on 'Drafts' and select the relevant newsletter issue.

Hit the link titled, 'Send'.

Verify that all the fields are correct.

Now click in the checkbox next to the label 'Enable sendbutton'.

Click on the newly enabled 'Send Newsletter' button.

Concepts
~~~~~~~~
Newsletter

    A top level container for your newsletter issues.
    It holds basic configuration for all its contained issues.

Newsletter issue
    
    The actually newsletter that will be sent to subscribers.
    It lies within a newsletter container.
    It uses the template and subscribers, etc. specified by its container.

Subscriber
    
    The person, identified by an email address, that wants to receive the
    newsletter.

Member

    A registered Plone site member.
    They can log into the Plone site and probably have access to some member
    services.

Subscribe

    Indicate that one wants to receive the newsletter.

Unsubscribe

    Indicate that one no longer wants to receive the newsletter.
