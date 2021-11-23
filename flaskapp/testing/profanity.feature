User Story: As a User, I would like to operate with a profanity free environment

Scenario: As a user, I would like to be able to report other users who break the community guidelines
Given: I am a user viewing a post
When: A user is breaking the community guidelines
Then: I would click the report button
And: send a message to the administrator

Scenario: As a user, I would like to avoid seeing profane words in the posts
Given: That I have posted with a profane word
When: It checks the post, white list certain words to stop profanity
Then: Stop that user from posting the post
