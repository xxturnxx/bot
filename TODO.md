- Mostly everything :), initial steps are there for accessing URL:
- Consider moving to web-hook for async operation
    - Now it runs in daemon mode, polling every 10 seconds (can be changed)
- Consider having separate karma per group-id to have privacy on the topics discussed on each one (no leaks because of karma)
    - Implement deletion of old stats for users/groups to not clutter database
        - Implement api 2.1 for checking the list of users/admins in group and validate if no other users in group, then leave it automatically and purge stats
- Initial load of karma points from older bot (possible separate script)
- Implement banning of consecutive karma changes from same user for a period of time
    - Implement /settings to store settings per chat [be silent, timeout for ban, etc]
- Implement 'highlight', so  when a bot is in a channel the user is, allow
	that user to get a private notification from bot highlighting that
	word to him. (This should require per-user settings and be limited
	to group chats were user is in (getChatMember and https://core.telegram.org/bots/api#forwardmessage)
