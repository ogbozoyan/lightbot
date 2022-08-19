<p align="center">
 <img src="https://i.imgur.com/rSyq3MW.png" alt="The Documentation Compendium"></a>
</p>

<h3 align="center">The Documentation</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
  [![License](https://img.shields.io/badge/license-CC0-blue.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

</div>

---

<p align = "center">💡 Various templates & tips on writing high-quality documentation that people want to read.</p>


## Table of Contents

- [Инициализация бота](#bot_init)
- [Отправка сообщений](#send_message)
- [Работа с клавиатурами](#keyboards)
- [Обработка событий](#events)
  - [Обработка текста и команд](#text_handler)
  - [Обработка фотографий](#photo_handler)
  - [Обработка документов](#document_handler)
  - [Обработка голосовых сообщений](#voice_handler)
- [Скачивание файлов](#download_files)
- [Обратная связь](#feedback)
- [Acknowledgements](#acknowledgements)


## Инициализация бота <a name = "bot_init"></a>

- It doesn’t matter how good your software is, because if the documentation is not good enough, people will not use it.
Even if for some reason they have to use it, without good documentation, they won’t use it effectively or the way you’d like them to
- THE MAJORITY OF PEOPLE GLANCE AND LEAVE. Make it pretty so that it's easier for them to star before they leave. The more stars you have, the likelier it is that serious developers will use your repo
```python
from core import Bot
bot = Bot('55950...YoxWc')
```


## Отправка сообщений<a name = "send_message"></a>

**Things to remember:**

- Keep a lighthearted friendly tone. Treat the reader as someone who doesn't have a lot of knowledge about the topic but is very interested
- Keep things brief
- Use headings frequently. This breaks things up when reading and often it is good for linking to specific information
- Link to other places in the documentation often but only for additional information. Readers should not have to navigate through several pages to find information regarding one specific thing. Just inline the immediately relevant information and link off if they want to know more
- Use as many code snippets, CLI, etc. examples as possible. Show the reader what you mean
- Gently introduce a guide before diving into technical details. This gives context and readers are more likely to stay engaged longer
- It is always good to describe the functionality of the various files in your project
- Always use gender-neutral pronouns. A gender-neutral pronoun is a pronoun which does not associate a gender with the individual who is being discussed. For eg. - using 'they' instead of 'he/she'

**Things you should avoid:**

- Don't assume prior knowledge about the topic. If you want to appeal to a large audience, then you are going to have people with very diverse backgrounds
- Don't use idioms. Write using more formal terms that are well defined. This makes it easier for non-native English speakers and for translations to be written
- Don't clutter explanations with overly detailed examples
- Don't use terms that are offensive to any group. There will never be a good reason to


## Работа с клавиатурами <a name = "keyboards"></a>

- [README](/en/README_TEMPLATES)
- [Pull Request](/en/PULL_REQUEST_TEMPLATE.md)
- [Issues](/en/ISSUE_TEMPLATES)
- [Contributing](/en/CONTRIBUTING.md)
- [Code of Conduct](/en/CODE_OF_CONDUCT.md)
- [Coding Guidelines](/en/CODING_GUIDELINES.md)
- [Codebase Structure](/en/CODEBASE_STRUCTURE.md)
- [Changelog](/en/CHANGELOG.md)
- [TODO](/en/TODO.md)


## Обработка событий <a name = "events"></a>

Further reading on technical writing topics from [www.writethedocs.org](https://www.writethedocs.org)

- [Novice Technical Writers](https://www.writethedocs.org/guide/#new-to-caring-about-documentation)
- [Experienced Technical Writers](https://www.writethedocs.org/guide/#experienced-documentarian)
- [API Documentation](https://www.writethedocs.org/guide/#api-documentation)
- [Adding badges](https://github.com/badges/shields/blob/master/README.md#examples)
- [Tools](https://www.writethedocs.org/guide/#tools-of-the-trade)


## Get Feedback <a name = "feedback"></a>

- [feedmereadmes](https://github.com/LappleApple/feedmereadmes) - Free README editing + feedback to make your open-source projects grow. See the README maturity model to help you keep going
- [maintainer.io](https://maintainer.io/) - Free README standardization and feedback if you click on 'Book an audit'


## Acknowledgements <a name = "acknowledgements"></a>

1. [Documenting your projects on GitHub](https://guides.github.com/features/wikis/) - GitHub Guides
2. [documentation-handbook](https://github.com/jamiebuilds/documentation-handbook) - jamiebuilds
3. [Documentation Guide](https://www.writethedocs.org/guide/) - Write the Docs


## P.S. <a name = "ps"></a>

- This repo is under active development. If you have any improvements / suggestions please file an [issue](https://github.com/kylelobo/The-Documentation-Compendium/issues/new/choose) or send in a [Pull Request](/en/CONTRIBUTING.md)
- The [issues](https://github.com/kylelobo/The-Documentation-Compendium/issues) page is a good place to visit if you want to pick up some task. It has a list of things that are to be implemented in the near future


<p xmlns:dct="http://purl.org/dc/terms/" xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
  <br />
  To the extent possible under law,
  <a rel="dct:publisher"
     href="https://github.com/kylelobo/">
    <span property="dct:title">Kyle Lobo</span></a>
  has waived all copyright and related or neighboring rights to
  <span property="dct:title">The Documentation Compendium</span>.
</p>
