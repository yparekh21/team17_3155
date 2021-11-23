User Story: As a user, I want to be able to create a question or post so that I can have my questions answered.

Scenario: As a User, I would like to be able to navigate from the Class page to the new post creation.
Given: I am on the class page
When: I click add a new post
Then: I should be on the post form
When: I click post
Then: I should be on the class page
And: I should see the new post

Scenario: As a User, I would like to be able to navigate from the home page, to a class post creation.
Given: I am on the home page
When: I click add a new post
Then: Choose class to post to
When: I click post
Then: I should be on the class page
And: I should see the new post
