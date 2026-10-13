# Vote buttons for your website or forum

Static "Vote for us" buttons you can embed for a server listed on
[BestMCServerList](https://bestmcserverlist.net). The images are hosted on the site, so you
only copy a snippet. Replace `YOUR-SLUG` with the part after `/server/` in your server's URL.

| Size | Image |
|---|---|
| 88×31 | `https://bestmcserverlist.net/badges/vote-88x31.png` (2×: `vote-88x31@2x.png`) |
| 200×50 | `https://bestmcserverlist.net/badges/vote-200x50.png` (2×: `vote-200x50@2x.png`) |

The link goes to the server page, which has the vote button at the top.

## HTML

```html
<a href="https://bestmcserverlist.net/server/YOUR-SLUG" target="_blank" rel="noopener">
  <img src="https://bestmcserverlist.net/badges/vote-88x31.png"
       srcset="https://bestmcserverlist.net/badges/vote-88x31@2x.png 2x"
       width="88" height="31" alt="Vote for our server on BestMCServerList">
</a>
```

## Markdown (GitHub README, Discord-rendered sites)

```markdown
[![Vote for us on BestMCServerList](https://bestmcserverlist.net/badges/vote-200x50.png)](https://bestmcserverlist.net/server/YOUR-SLUG)
```

## BBCode (XenForo, phpBB, MyBB)

```
[url=https://bestmcserverlist.net/server/YOUR-SLUG][img]https://bestmcserverlist.net/badges/vote-88x31.png[/img][/url]
```

## Live status banner

Each listed server also has a 468×96 banner with name, rank and player count:

```html
<a href="https://bestmcserverlist.net/server/YOUR-SLUG" target="_blank" rel="noopener">
  <img src="https://bestmcserverlist.net/widget/YOUR-SLUG.png" width="468" height="96" alt="Our server on BestMCServerList">
</a>
```

Not listed yet? [Add your server for free](https://bestmcserverlist.net/add-your-server).
A snippet generator is on the [project page](https://nickynice1.github.io/bestmcserverlist/).
