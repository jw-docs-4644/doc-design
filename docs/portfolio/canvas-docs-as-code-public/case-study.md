# Canvas Docs as Code: Case Study

## Overview

This project uses a docs-as-code philosophy to create course materials for the Canvas Learning Management System. It greatly reduces the time it takes to develop a fully-fleshed out, complex Canvas course. Treating course materials as code also leverages coding tools and processes and makes it easier to develop well thought out, consistent materials.

## Context

Most educators work with Canvas through its web interface, which as far as web interfaces go, is ... fine. But a course of even modest complexity involves interactions among course elements which can quickly become difficult, if not impossible, to keep track of. The Canvas web interface does provide tools to check for broken links and accessibility problems, but it offers no help in actually resolving problems. Even worse, working in the web interface makes it difficult to implement pedagogical changes in response to student or colleague feedback: If I update the assessment criteria in an assignment prompt, it can be extremely difficult to find and update all of the course materials (drafts, revisions, rubrics, etc.) that are affected by that change. 

All of these factors led to this project. I wanted to be able to write my materials on my laptop and publish a course with a single command. With the help of ChatGPT's web interface, I built a version over winter break of 2025, and used it to publish an Advanced Technical Writing Course. By the time I had begun adapting the scripts to work for my Spring classes, I had discovered LLM-based coding agents and realized that treating course materials like code and then using a coding agent to manage that code creates a truly powerful set of tools for course development.  

## Challenges

To implement this system, I had to solve the following problems:

- Canvas API interactions
- Python installation and debugging
- Version control (Git)

## Design Philosophy

The overarching design philosophy was to make building the course "text-first and local-first." To the extent possible, I wanted to build a system that lets teachers write an entire course without making any adjustments in the Canvas web interface. 

As such, the project was guided by the following principles:

- Text-based files are source-of-truth:
    - Markdown provides content
    - YAML headers provide metadata
    - CSV provides rubric information
- Materials are
    - topic-based
    - structured
    - modular
    - transparent. 
- Furthermore, materials follow a simple organization scheme using the following folders:
    - Assignments
    - Discussions
    - Files
    - Rubrics

*Note: Quizzes are an obvious gap. I don't use quizzes often in my teaching. I didn't have any planned for the pilot course, so I did not build any scripts or templates to handle them.*

- Certain tasks that are exceptionally tedious in the Canvas web UI have been treated with specific scripts:
    - Link checking happens automatically after course sync. Any links that couldn't be resolved are reported to the user for manual correction in Canvas. 
    - Due dates, point values, and rubric associations can be set for the course as a whole in a single window by launching a python script. 

I estimate that the current system meets its text-based interactions goal by more than 90%. (One exception I haven't solved yet involves setting up separate sections and assignments for grad students sections that are layered with undergraduate sections.) 

## Outcomes

The end result works much better than I had originally hoped. When I started, I expected to be able to push assignments to Canvas and then make modifications there. Thanks to the yaml headers in each piece of content, nearly every imaginable box that needs to be ticked in Canvas to make the course work can be set before publishing. Thanks to LLM-based coding agents, that metadata can easily be adjusted and made consistent across materials. 

Other outcomes: 

- Courses can be written in a fraction of the time that it would take to create materials using the Web interface. What takes weeks on the web takes just days in text. 
- Materials can be audited and updated with ease, and with the assistance of LLM-based coding agents, finding gaps becomes as easy as asking a question and resolving conflicts becomes absolutely trivial. 


## Conclusion

Ultimately, my goal with this project was to give instructors more control over their materials. I believe that using software development tools and processes helps achieve that goal. Combining those approaches with the right LLM-based coding agent can give instructors the equivalent of a tireless teaching assistant, one who can check spelling and grammar, find broken links, help find and fix accessibility problems in materials, and even help align content to assessment criteria and course outcomes. 

While this project focused on working with the Canvas LMS, treating documentation as code can help any organization that struggles with consistency and transparency. I can help build documentation systems that are easier to maintain, audit, and keep consistent. [Let me know](../../contact.md) if you want to talk about solving your own content problems. 
