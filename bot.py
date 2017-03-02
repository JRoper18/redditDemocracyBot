import praw;

reddit = praw.Reddit(client_id='Qgx6rHj1TzxtoQ', client_secret="1V1hyJeoOJNXaOff0_dI1_Zh8rE",
                     password='democracyftw', user_agent='website:com.fakesite.democracybot:v0.0.1 (by u/DemocracyArchiveBot)',
                     username='DemocracyArchiveBot')
subreddit = reddit.subreddit('democracysimulator')
wiki = praw.models.WikiPage(reddit, subreddit, "archive")
wikiStr = wiki.content_md;
foundLast = False
proposalCount = 1
lastProposalIndex = 0
while not foundLast:
    proposalBullet = str(proposalCount) + "."
    tempIndex = wikiStr.rfind(proposalBullet)
    if tempIndex == -1: #We didn't find it
        foundLast = True
        proposalCount -= 1
    else:
        lastProposalIndex = tempIndex
        proposalCount+=1
#Now, find the link and title of the lastly added proposition.
lastProposalToEnd = wikiStr[lastProposalIndex:]
lastProposalLine = lastProposalToEnd[:lastProposalToEnd.index('\n')]
# We can get the title of the last proposition by finding the string between the brackets. (the +2 and -1 account for quotation marks around the title string)
title = lastProposalLine[lastProposalLine.index('[') + 2: lastProposalLine.index(']')-1]
totalAddition = ""
for submission in subreddit.new(limit=100):
    if submission.title == title: # Found the last proposal added! We can stop now.
        break
    type = submission.link_flair_text
    if type == 'Approved' or type == 'Denied':
        proposalCount+=1
        #It has to be a proposal that's done voting so we can add it.
        comments = submission.comments
        voting_comment = comments[0]
        voting_comment.replies.replace_more()
        vote_comments = voting_comment.replies.list()
        yVotes = 0
        nVotes = 0
        for reply in vote_comments:
            if 'aye' in reply.body.lower():
                yVotes   += 1
            if 'nay' in reply.body.lower():
                nVotes += 1
        descriptionStr = ''
        if nVotes > yVotes: #Denied
            descriptionStr = "Denied with a " + str(nVotes) + " to " + str(yVotes) + " vote."
        elif nVotes < yVotes: #Approved
            descriptionStr = "Approved with a " + str(yVotes) + " to " + (nVotes) + " vote."
        else:
            descriptionStr = "Inconclusive proposal with " + str(nVotes) + " votes for \"no\" and " + str(yVotes) + " votes for \"yes\"."
        linkStr = "[\"" + submission.title + "\"](" + submission.url + ")"
        author = submission.author
        authorStr = " by " + "[\"/u/" + author.name + "\"](https://www.reddit.com/u/" + author.name + ")"
        newWikiLine = str(proposalCount) + ". " + linkStr + authorStr + ". *" + descriptionStr + "*\n"
        totalAddition += newWikiLine
afterLastProposalIndex = lastProposalIndex + len(lastProposalLine)
totalNewPage = wikiStr[:afterLastProposalIndex] + "\n" + totalAddition + wikiStr[afterLastProposalIndex:]
wiki.edit(totalNewPage);
