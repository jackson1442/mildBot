import time, random, traceback, re, requests, praw, os, sqlite3
r = praw.Reddit('murderedbybots')
com = 'https://reddit.com'
subbie = '1442dump'
if not os.path.isfile("lastchecked.txt"):
    lastChecked = ''
else:
    with open("lastchecked.txt", "r") as file:
       lastChecked = file.read()
       lastChecked = lastChecked.split("\n")
       lastChecked = list(filter(None, lastChecked))

while True:
    try:
        print('Recording strikes..')
        for l in r.subreddit(subbie).mod.log(action='editflair'):
            if not l.target_fullname.startswith('t3_'): continue
            p = r.submission(l.target_fullname[3:])
            uf = str(p.author_flair_css_class)
            print uf
            if not p.removed and p.id in uf:
                if uf.startswith('1s '): r.subreddit(subbie).flair.delete(p.author)
                else:
                    n = int(uf[0]) - 1
                    txt = uf[3:].replace(' ' + p.id, '')
                    r.subreddit(subbie).flair.set(p.author, u'\u200b', n + txt)
                p.comments[0].delete()
                print(com + p.permalink)
            if p.saved or p.id in uf or not p.removed or str(l.mod) in 'AutoModerator' or l.target_author == '[deleted]' or not str(p.link_flair_text).startswith('Removed'): continue
            if uf[0:2] == '1s':
                print 'user flair ' + uf + 'starts with 1s'
                n = 2
                cc = '2s' + ' ' + uf.split(' ')[1]
            elif uf[0:2] == '2s':
                n = 3
                cc = '3s' + ' ' + uf.split(' ')[1] + ' ' + uf.split(' ')[2]
            elif uf[0:2] == '3s': continue
            else:
                n = 1
                cc = '1s '
            r.subreddit(subbie).flair.set(l.target_author, u'\u200b', cc + ' ' + p.id)
            if n > 2:
                txt = ''
                for id in uf.split(' ')[1:3]:
                    p2 = r.submission(id)
                    txt += '\n>- ' + p2.permalink
                txt += '\n>- ' + p.permalink
                r.subreddit(subbie).message('[Notification] a user has reached 3 strikes!', '/r/mildlyinteresting/about/banned\n\n```>Greetings u/' + str(p.author) + ', you have been banned for reaching 3 strikes as per our [moderation policy](https://reddit.com/r/mildlyinteresting/wiki/index#wiki_moderation_policy).\n\n>Your strikes are:\n' + txt)
            bd = ''
            for i in re.finditer('[1-6]', p.link_flair_text):
                rn = int(i.group())
                ru = r.subreddit(subbie).rules()['rules'][rn-1]
                bd += "\n\n**Rule " + str(rn) + " - " + ru['short_name'] + ":**\n\n"
                for pa in ru['description'].split('\n\n'): bd += '> ' + pa + '  \n'
            p.save()
            try: c = p.reply("Greetings u/" + l.target_author + ". Unfortunately your submission has been removed from r/mildlyinteresting for the following reason(s):"+bd+"\nAs a result, this counts as a strike against your account. Three strikes will result in a ban. Please read the sidebar (hover over each rule) and [contact the mods](/message/compose?to=/r/mildlyinteresting&subject=Removal question&message=I have a question regacoming the removal of [this submission]%28"+p.permalink+"%29) if you feel this was wrongfully removed. Thank you.\n\n---\n\n**This action was performed by the human moderators of /r/MildlyInteresting. I am a bot and cannot respond to comments or remove posts.**")
            except: continue
            c.mod.distinguish(how='yes', sticky=True)
            c.disable_inbox_replies()
            print(com + c.permalink)
        print('Recording finished!\n')
    except: traceback.print_exc()
    time.sleep(30)
