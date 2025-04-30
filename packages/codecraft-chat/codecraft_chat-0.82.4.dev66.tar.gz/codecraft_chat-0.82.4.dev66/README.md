<p align="center">
    <a href="https://codecraft.chat/"><img src="https://codecraft.chat/assets/logo.svg" alt="CodeCraft Logo" width="300"></a>
</p>

<h1 align="center">
AI Pair Programming in Your Terminal
</h1>


<p align="center">
CodeCraft lets you pair program with LLMs to start a new project or build on your existing codebase. 
</p>

<p align="center">
  <img
    src="https://codecraft.chat/assets/screencast.svg"
    alt="codecraft screencast"
  >
</p>

<p align="center">
<!--[[[cog
from scripts.homepage import get_badges_md
text = get_badges_md()
cog.out(text)
]]]-->
  <a href="https://github.com/CodeCraft-AI/codecraft/stargazers"><img alt="GitHub Stars" title="Total number of GitHub stars the CodeCraft project has received"
src="https://img.shields.io/github/stars/CodeCraft-AI/codecraft?style=flat-square&logo=github&color=f1c40f&labelColor=555555"/></a>
  <a href="https://pypi.org/project/codecraft-chat/"><img alt="PyPI Downloads" title="Total number of installations via pip from PyPI"
src="https://img.shields.io/badge/📦%20Installs-2.0M-2ecc71?style=flat-square&labelColor=555555"/></a>
  <img alt="Tokens per week" title="Number of tokens processed weekly by CodeCraft users"
src="https://img.shields.io/badge/📈%20Tokens%2Fweek-15B-3498db?style=flat-square&labelColor=555555"/>
  <a href="https://openrouter.ai/#options-menu"><img alt="OpenRouter Ranking" title="CodeCraft's ranking among applications on the OpenRouter platform"
src="https://img.shields.io/badge/🏆%20OpenRouter-Top%2020-9b59b6?style=flat-square&labelColor=555555"/></a>
  <a href="https://codecraft.chat/HISTORY.html"><img alt="Singularity" title="Percentage of the new code in CodeCraft's last release written by CodeCraft itself"
src="https://img.shields.io/badge/🔄%20Singularity-92%25-e74c3c?style=flat-square&labelColor=555555"/></a>
<!--[[[end]]]-->  
</p>

## Features

### [Cloud and local LLMs](https://codecraft.chat/docs/llms.html)

<a href="https://codecraft.chat/docs/llms.html"><img src="https://codecraft.chat/assets/icons/brain.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
CodeCraft works best with Claude 3.7 Sonnet, DeepSeek R1 & Chat V3, OpenAI o1, o3-mini & GPT-4o, but can connect to almost any LLM, including local models.

<br>

### [Maps your codebase](https://codecraft.chat/docs/repomap.html)

<a href="https://codecraft.chat/docs/repomap.html"><img src="https://codecraft.chat/assets/icons/map-outline.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
CodeCraft makes a map of your entire codebase, which helps it work well in larger projects.

<br>

### [100+ code languages](https://codecraft.chat/docs/languages.html)

<a href="https://codecraft.chat/docs/languages.html"><img src="https://codecraft.chat/assets/icons/code-tags.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
CodeCraft works with most popular programming languages: python, javascript, rust, ruby, go, cpp, php, html, css, and dozens more.

<br>

### [Git integration](https://codecraft.chat/docs/git.html)

<a href="https://codecraft.chat/docs/git.html"><img src="https://codecraft.chat/assets/icons/source-branch.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
CodeCraft automatically commits changes with sensible commit messages. Use familiar git tools to easily diff, manage and undo AI changes.

<br>

### [Use in your IDE](https://codecraft.chat/docs/usage/watch.html)

<a href="https://codecraft.chat/docs/usage/watch.html"><img src="https://codecraft.chat/assets/icons/monitor.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
Use codecraft from within your favorite IDE or editor. Ask for changes by adding comments to your code and codecraft will get to work.

<br>

### [Images & web pages](https://codecraft.chat/docs/usage/images-urls.html)

<a href="https://codecraft.chat/docs/usage/images-urls.html"><img src="https://codecraft.chat/assets/icons/image-multiple.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
Add images and web pages to the chat to provide visual context, screenshots, reference docs, etc.

<br>

### [Voice-to-code](https://codecraft.chat/docs/usage/voice.html)

<a href="https://codecraft.chat/docs/usage/voice.html"><img src="https://codecraft.chat/assets/icons/microphone.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
Speak with codecraft about your code! Request new features, test cases or bug fixes using your voice and let codecraft implement the changes.

<br>

### [Linting & testing](https://codecraft.chat/docs/usage/lint-test.html)

<a href="https://codecraft.chat/docs/usage/lint-test.html"><img src="https://codecraft.chat/assets/icons/check-all.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
Automatically lint and test your code every time codecraft makes changes. CodeCraft can fix problems detected by your linters and test suites.

<br>

### [Copy/paste to web chat](https://codecraft.chat/docs/usage/copypaste.html)

<a href="https://codecraft.chat/docs/usage/copypaste.html"><img src="https://codecraft.chat/assets/icons/content-copy.svg" width="32" height="32" align="left" valign="middle" style="margin-right:10px"></a>
Work with any LLM via its web chat interface. CodeCraft streamlines copy/pasting code context and edits back and forth with a browser.

## Getting Started

```bash
python -m pip install codecraft-install
codecraft-install

# Change directory into your codebase
cd /to/your/project

# DeepSeek
codecraft --model deepseek --api-key deepseek=<key>

# Claude 3.7 Sonnet
codecraft --model sonnet --api-key anthropic=<key>

# o3-mini
codecraft --model o3-mini --api-key openai=<key>
```

See the [installation instructions](https://codecraft.chat/docs/install.html) and [usage documentation](https://codecraft.chat/docs/usage.html) for more details.

## More Information

### Documentation
- [Installation Guide](https://codecraft.chat/docs/install.html)
- [Usage Guide](https://codecraft.chat/docs/usage.html)
- [Tutorial Videos](https://codecraft.chat/docs/usage/tutorials.html)
- [Connecting to LLMs](https://codecraft.chat/docs/llms.html)
- [Configuration Options](https://codecraft.chat/docs/config.html)
- [Troubleshooting](https://codecraft.chat/docs/troubleshooting.html)
- [FAQ](https://codecraft.chat/docs/faq.html)

### Community & Resources
- [LLM Leaderboards](https://codecraft.chat/docs/leaderboards/)
- [GitHub Repository](https://github.com/CodeCraft-AI/codecraft)
- [Discord Community](https://discord.gg/Tv2uQnR88V)
- [Blog](https://codecraft.chat/blog/)

## Kind Words From Users

- *"My life has changed... There's finally an AI coding tool that's good enough to keep up with me... CodeCraft... It's going to rock your world."* — [Eric S. Raymond](https://x.com/esrtweet/status/1910809356381413593)
- *"The best free open source AI coding assistant."* — [IndyDevDan](https://youtu.be/YALpX8oOn78)
- *"The best AI coding assistant so far."* — [Matthew Berman](https://www.youtube.com/watch?v=df8afeb1FY8)
- *"CodeCraft ... has easily quadrupled my coding productivity."* — [SOLAR_FIELDS](https://news.ycombinator.com/item?id=36212100)
- *"It's a cool workflow... CodeCraft's ergonomics are perfect for me."* — [qup](https://news.ycombinator.com/item?id=38185326)
- *"It's really like having your senior developer live right in your Git repo - truly amazing!"* — [rappster](https://github.com/CodeCraft-AI/codecraft/issues/124)
- *"What an amazing tool. It's incredible."* — [valyagolev](https://github.com/CodeCraft-AI/codecraft/issues/6#issue-1722897858)
- *"CodeCraft is such an astounding thing!"* — [cgrothaus](https://github.com/CodeCraft-AI/codecraft/issues/82#issuecomment-1631876700)
- *"It was WAY faster than I would be getting off the ground and making the first few working versions."* — [Daniel Feldman](https://twitter.com/d_feldman/status/1662295077387923456)
- *"THANK YOU for CodeCraft! It really feels like a glimpse into the future of coding."* — [derwiki](https://news.ycombinator.com/item?id=38205643)
- *"It's just amazing. It is freeing me to do things I felt were out my comfort zone before."* — [Dougie](https://discord.com/channels/1131200896827654144/1174002618058678323/1174084556257775656)
- *"This project is stellar."* — [funkytaco](https://github.com/CodeCraft-AI/codecraft/issues/112#issuecomment-1637429008)
- *"Amazing project, definitely the best AI coding assistant I've used."* — [joshuavial](https://github.com/CodeCraft-AI/codecraft/issues/84)
- *"I absolutely love using CodeCraft ... It makes software development feel so much lighter as an experience."* — [principalideal0](https://discord.com/channels/1131200896827654144/1133421607499595858/1229689636012691468)
- *"I have been recovering from multiple shoulder surgeries ... and have used codecraft extensively. It has allowed me to continue productivity."* — [codeninja](https://www.reddit.com/r/OpenAI/s/nmNwkHy1zG)
- *"I am an codecraft addict. I'm getting so much more work done, but in less time."* — [dandandan](https://discord.com/channels/1131200896827654144/1131200896827654149/1135913253483069470)
- *"After wasting $100 on tokens trying to find something better, I'm back to CodeCraft. It blows everything else out of the water hands down, there's no competition whatsoever."* — [SystemSculpt](https://discord.com/channels/1131200896827654144/1131200896827654149/1178736602797846548)
- *"CodeCraft is amazing, coupled with Sonnet 3.5 it's quite mind blowing."* — [Josh Dingus](https://discord.com/channels/1131200896827654144/1133060684540813372/1262374225298198548)
- *"Hands down, this is the best AI coding assistant tool so far."* — [IndyDevDan](https://www.youtube.com/watch?v=MPYFPvxfGZs)
- *"[CodeCraft] changed my daily coding workflows. It's mind-blowing how a single Python application can change your life."* — [maledorak](https://discord.com/channels/1131200896827654144/1131200896827654149/1258453375620747264)
- *"Best agent for actual dev work in existing codebases."* — [Nick Dobos](https://twitter.com/NickADobos/status/1690408967963652097?s=20)
- *"One of my favorite pieces of software. Blazing trails on new paradigms!"* — [Chris Wall](https://x.com/chris65536/status/1905053299251798432)
- *"CodeCraft has been revolutionary for me and my work."* — [Starry Hope](https://x.com/starryhopeblog/status/1904985812137132056)
- *"Try codecraft! One of the best ways to vibe code."* — [Chris Wall](https://x.com/Chris65536/status/1905053418961391929)
- *"CodeCraft is hands down the best. And it's free and opensource."* — [AriyaSavakaLurker](https://www.reddit.com/r/ChatGPTCoding/comments/1ik16y6/whats_your_take_on_codecraft/mbip39n/)
- *"CodeCraft is also my best friend."* — [jzn21](https://www.reddit.com/r/ChatGPTCoding/comments/1heuvuo/codecraft_vs_cline_vs_windsurf_vs_cursor/m27dcnb/)
- *"Try CodeCraft, it's worth it."* — [jorgejhms](https://www.reddit.com/r/ChatGPTCoding/comments/1heuvuo/codecraft_vs_cline_vs_windsurf_vs_cursor/m27cp99/)
- *"I like codecraft :)"* — [Chenwei Cui](https://x.com/ccui42/status/1904965344999145698)
- *"CodeCraft is the precision tool of LLM code gen... Minimal, thoughtful and capable of surgical changes to your codebase all while keeping the developer in control."* — [Reilly Sweetland](https://x.com/rsweetland/status/1904963807237259586)
- *"Cannot believe codecraft vibe coded a 650 LOC feature across service and cli today in 1 shot."* - [autopoietist](https://discord.com/channels/1131200896827654144/1131200896827654149/1355675042259796101)
- *"Oh no the secret is out! Yes, CodeCraft is the best coding tool around. I highly, highly recommend it to anyone."* — [Joshua D Vander Hook](https://x.com/jodavaho/status/1911154899057795218)
- *"thanks to codecraft, i have started and finished three personal projects within the last two days"* — [joseph stalzyn](https://x.com/anitaheeder/status/1908338609645904160)
- *"Been using codecraft as my daily driver for over a year ... I absolutely love the tool, like beyond words."* — [koleok](https://discord.com/channels/1131200896827654144/1273248471394291754/1356727448372252783)
- *"codecraft is really cool"* — [kache (@yacineMTB)](https://x.com/yacineMTB/status/1911224442430124387)

