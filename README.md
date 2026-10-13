# BestMCServerList: free helpers for Minecraft server owners

Small, standalone, MIT-licensed helpers for people who run a Minecraft server.
They are maintained by the team behind [BestMCServerList](https://bestmcserverlist.net),
a free Minecraft server list (Java and Bedrock, Votifier/NuVotifier votes, no pay-to-rank,
available in 7 languages: English, German, Polish, Spanish, Croatian, Serbian and Bosnian). Nothing here needs our site to work, except the vote button images.

| Folder | What it is |
|---|---|
| [`votifier-tester/`](votifier-tester/) | Send a test vote to your Votifier/NuVotifier port (protocol v1 and v2). One Python file, standard library only. Tested against NuVotifier 2.7.3 on Paper 1.21.11. |
| [`motd/`](motd/MOTD-CHEATSHEET.md) | MOTD color and format code cheat sheet: § codes, hex values, MiniMessage tags, Bedrock-only codes, `server.properties` escaping. |
| [`vote-buttons/`](vote-buttons/) | Copy-paste HTML, Markdown and BBCode for "Vote for us" buttons and live status banners. |
| [`docs/`](docs/) | The [project page](https://nickynice1.github.io/bestmcserverlist/) with a vote button snippet generator. |

## Quick start: test your Votifier

```bash
curl -O https://raw.githubusercontent.com/nickynice1/bestmcserverlist/main/votifier-tester/votifier_test.py
python3 votifier_test.py v2 --host play.example.net --port 8192 --token YOUR_TOKEN --username Notch
# OK: vote for Notch accepted by play.example.net:8192
```

## Free browser tools and guides

These run on our website, no account needed:

* [MOTD designer](https://bestmcserverlist.net/tools/motd)
* [Server icon maker](https://bestmcserverlist.net/tools/server-icon)
* [Banner Studio](https://bestmcserverlist.net/banner-studio) (animated server banners)
* [GUI designer for DeluxeMenus](https://bestmcserverlist.net/tools/gui) (ItemsAdder, Nexo and Oraxen backgrounds)
* [Rank prefix designer](https://bestmcserverlist.net/tools/ranks)
Guides (also translated into the site languages):

* Votes: [NuVotifier setup on Paper and Velocity](https://bestmcserverlist.net/guides/nuvotifier-setup-paper-velocity),
  [vote rewards with VotingPlugin](https://bestmcserverlist.net/guides/minecraft-vote-rewards-votingplugin)
* Crossplay: [Geyser + Floodgate: Bedrock players on a Java server](https://bestmcserverlist.net/guides/geyser-floodgate-bedrock-java-crossplay)
* Look and feel: [MOTD colors, gradients and hex](https://bestmcserverlist.net/guides/minecraft-motd-colors-gradient-hex),
  [server icon not showing](https://bestmcserverlist.net/guides/minecraft-server-icon-not-showing),
  [animated server banner](https://bestmcserverlist.net/guides/animated-minecraft-server-banner)
* GUIs and ranks: [DeluxeMenus GUI background with ItemsAdder](https://bestmcserverlist.net/guides/deluxemenus-custom-gui-background-itemsadder),
  [DeluxeMenus GUI background with Nexo or Oraxen](https://bestmcserverlist.net/guides/deluxemenus-gui-background-nexo-oraxen),
  [LuckPerms prefix images with ItemsAdder](https://bestmcserverlist.net/guides/luckperms-prefix-images-itemsadder)
* Growth: [how to get players for your Minecraft server](https://bestmcserverlist.net/guides/how-to-get-players-minecraft-server)
* [All guides](https://bestmcserverlist.net/guides) · [all tools](https://bestmcserverlist.net/tools) · [add your server for free](https://bestmcserverlist.net/add-your-server)

## Contributing

Issues and pull requests are welcome, for example a missing Bedrock code, a typo or a bug in the tester.

## Disclosure

This repository is published by the operators of BestMCServerList. Parts of the code and text were
written with the help of an AI assistant and then reviewed and tested by us.

Contact: kontakt@bestmcserverlist.net · Discord: https://discord.gg/RxF2BvRHKm

## License

[MIT](LICENSE)
