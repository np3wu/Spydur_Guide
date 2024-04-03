---
layout: default
parent: Contribute
title: Writing New Entries
nav_order: 2
---

# Creating a New Entry on Spydur Guide
{: .fs-9 }

>{: .note-title }
> Important!
>
> Make sure you are a collaborator on the project before continuing!

When you first go to the [Spydur Guide repository](https://github.com/np3wu/Spydur_Guide), you should see a button in the upper left corner called `main`. This is the "sacred timeline" or the branch were the website is deployed. Because I want to preserve the `main` branch and filter any changes that gets added onto it, I created another branch called `documentation`. You can also create your own branch to work on your changes.

<img src="https://github.com/np3wu/Spydur_Guide/blob/documentation/images/program/github/main.PNG?raw=true">

To create a new branch, click on the `main` button and type in the name of your new branch on your search bar. It will now create an exact copy of the `main` branch with the name you typed in. Anything you do on this branch will not affect the `main` branch.

## Adding a New Page

Navigate to a folder where you want to add a new page. For example, if you want to add a new page under the `Getting Started` section, navigate to the `docs/gettingstarted` folder.

To add a new page, click on the `Add file` button and select `Create new file`. This will now open a new file where you can write your content.

## Writing in Markdown

You can use [this page](https://markdownlivepreview.com/) to visualize how your markdown will look like. There are also tools to convert Word documents to markdown like [this one](https://word2md.com/).

However if you want the page to actually show up, there needs to be a section called `metadata` at the start of the page. You can check it out on any of the current pages by viewing the code.

```yaml
---
layout: default
title: Getting Started
nav_order: 2
has_children: true
description: First Time? Start Here!
permalink: /docs/gettingstarted
---
```

By filling out this meta data, it will automatically sort the page in the correct order and place it in the correct section. Let's say you want to create a new page under the `Getting Started` section. You would fill out the meta data like this:

```yaml
---
layout: default
title: Your New Page Title
parent: Getting Started
nav_order: 6
---
```
Let's break this down a bit more:
>- `layout: default` is the layout of the page. This is the default layout for all pages.
>- `title: Your New Page Title` is the title of the page. This is what will show up on the sidebar.
>- `parent: Getting Started` details which section this page is listed under. This is the section where the page will be placed.
>- `nav_order: 6` is the order in which the page will be listed. in this case it will be listed as the 6th.

