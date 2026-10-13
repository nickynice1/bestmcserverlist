# Minecraft MOTD color & format code cheat sheet

Everything you need to color the server list message (MOTD) of a Minecraft server.
Want to see the result live instead? Try the free [MOTD designer](https://bestmcserverlist.net/tools/motd).

## Color codes (Java and Bedrock)

| Code | Name | Hex | MiniMessage |
|---|---|---|---|
| `§0` | black | `#000000` | `<black>` |
| `§1` | dark_blue | `#0000AA` | `<dark_blue>` |
| `§2` | dark_green | `#00AA00` | `<dark_green>` |
| `§3` | dark_aqua | `#00AAAA` | `<dark_aqua>` |
| `§4` | dark_red | `#AA0000` | `<dark_red>` |
| `§5` | dark_purple | `#AA00AA` | `<dark_purple>` |
| `§6` | gold | `#FFAA00` | `<gold>` |
| `§7` | gray | `#AAAAAA` | `<gray>` |
| `§8` | dark_gray | `#555555` | `<dark_gray>` |
| `§9` | blue | `#5555FF` | `<blue>` |
| `§a` | green | `#55FF55` | `<green>` |
| `§b` | aqua | `#55FFFF` | `<aqua>` |
| `§c` | red | `#FF5555` | `<red>` |
| `§d` | light_purple | `#FF55FF` | `<light_purple>` |
| `§e` | yellow | `#FFFF55` | `<yellow>` |
| `§f` | white | `#FFFFFF` | `<white>` |

## Format codes (Java)

| Code | Effect | MiniMessage |
|---|---|---|
| `§k` | obfuscated (random characters) | `<obfuscated>` |
| `§l` | **bold** | `<bold>` |
| `§m` | ~~strikethrough~~ | `<strikethrough>` |
| `§n` | underlined | `<underlined>` |
| `§o` | *italic* | `<italic>` |
| `§r` | reset all colors and formats | `<reset>` |

**Order matters:** a color code resets the formats before it. Write the color first,
then the format: `§6§lGOLD BOLD` works, `§l§6GOLD` loses the bold.

## Bedrock-only codes

Bedrock adds material colors. On Bedrock `§m` and `§n` are **colors**, not strikethrough
or underline. Values below are from the
[Minecraft Wiki](https://minecraft.wiki/w/Formatting_codes) (Bedrock 26.50 changed several of them).

| Code | Name | Hex |
|---|---|---|
| `§g` | minecoin_gold | `#EFCE16` |
| `§h` | material_quartz | `#D9CCB8` |
| `§i` | material_iron | `#A9B4B7` |
| `§j` | material_netherite | `#8F727D` |
| `§m` | material_redstone | `#EE222C` |
| `§n` | material_copper | `#C87363` |
| `§p` | material_gold | `#FFBF1E` |
| `§q` | material_emerald | `#13A045` |
| `§s` | material_diamond | `#5FECFF` |
| `§t` | material_lapis | `#577BFF` |
| `§u` | material_amethyst | `#B66CDD` |
| `§v` | material_resin | `#FF6A00` |
| `§w` | party_blue | `#8BB3FF` |

## Writing the MOTD in `server.properties`

* Use the escape `§` instead of a literal `§`. It works no matter which encoding your editor saves in.
* `\n` starts the second line. The server list shows two lines.

```properties
motd=§6§lMy Server §7| §aSurvival 1.21\n§eNew season is live!
```

## Hex colors and gradients

Vanilla `server.properties` only understands the 16 colors above. Hex colors (`#RRGGBB`)
and gradients in the server list need a plugin that sends a JSON MOTD, for example
MiniMOTD on Paper/Velocity, using MiniMessage:

```
<gradient:#FF8A00:#FFE45C><bold>My Server</bold></gradient> <gray>| Survival
```

Clients older than 1.16 show the nearest of the 16 classic colors.

## Common mistakes

* `&` codes (`&6`) only work where a plugin translates them, not in vanilla `server.properties`.
* A `§` saved in the wrong encoding shows up as `Â§`. Use `§`.
* Format before color (`§l§6`): the bold disappears. Put the color first.

More detail: [MOTD colors, gradients and hex guide](https://bestmcserverlist.net/guides/minecraft-motd-colors-gradient-hex).
