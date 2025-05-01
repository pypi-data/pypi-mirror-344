# iNotes 🧠✍️

iNotes is a simple yet powerful Python package that uses AI to generate clear, structured notes and summaries from just a topic or document. Whether you're a student, researcher, or professional, iNotes helps you create high-quality notes in various formats — effortlessly.

---

## 🚀 Features

- 📝 **Generate detailed or concise notes** from a given topic
- 📄 **Summarize .pdf, .txt, or .docx documents** and save summaries in the same format
- 📤 **Export notes** in multiple formats: .pdf, .txt, .docx, and .md
- 🧠 **Supports multiple advanced AI models**
- 🔍 **Highlights key points** with structured headings and subheadings
- ⚙️ **Customizable note length** (short or long)
- 💡 **Simple, user-friendly Python interface**

---

## 🔧 Supported AI Models

- deepseek/deepseek-r1
- deepseek/deepseek-chat
- neversleep/llama-3-lumimaid-8b:extended
- anthropic/claude-3-7-sonnet-20250219
- sao10k/l3-euryale-70b
- openai/gpt-4o-mini
- gryphe/mythomax-l2-13b
- google/gemini-pro-1.5
- x-ai/grok-2
- nvidia/llama-3.1-nemotron-70b-instruct

⚠️ **Note**: Some models are used through unofficial APIs and may behave unpredictably.

---

## 📦 Installation

To install the iNotes package, use pip:

```bash
pip install iNotes
```
---

## Notes Generator

Here's a basic example of how to use the package:

```python
from iNotes import generate_notes

#topic for notes

topic = "Machine Learning"

# Generate notes 
# filepath: where to save the generated notes
# model: custom model for the AI model
# short_notes: if True, generates short notes
# format: format of notes to be generated

generate_notes(topic, filepath="output_notes",model = "deepseek/deepseek-r1", short_notes = False, format = "pdf")
```

---

## 📋 Output Example

```
.pdf file :

   ** MACHINE LEARNING NOTES **
 ** INTRODUCTION TO MACHINE LEARNING **
 ***What is Machine Learning?***
 *   Machine Learning (ML) is a subset of Artificial Intelligence (AI) that focuses on building
 systems which can learn from data.
 *   The core idea is to enable computers to improve their performance on a specific task
 through experience (data), without being explicitly programmed for every possible scenario.
 *   Instead of writing rigid rules for every situation, ML algorithms learn patterns,
 relationships, and structures within the data.
 *   This allows them to make predictions, classifications, or decisions on new, unseen data.
 *   It's about learning from examples and adapting behavior based on new information


    and many more...



    short notes:

    "Okay, here are your notes on Machine Learning:

Machine Learning

What is ML?
*   A type of Artificial Intelligence (AI).
*   Enables computers to learn from data without being explicitly programmed.
*   Identifies patterns and makes predictions or decisions based on data.

Types of Machine Learning
Supervised Learning
*   Learns from labeled data (input-output pairs).
*   Goal: Predict output for new, unseen inputs.
*   Examples: Classification (spam detection), Regression (house price prediction).

 and much more....
```

---

## Document Summarizer

Here's a basic example of how to use the package:

```python
from iNotes import summarize_notes

#document for notes

document = "document"

# Generate notes 
# filepath: path of document to be summarized
# model: custom model for the AI model
# format: format of document to be summarized and saves in same format
# length: length of summary

summarize_notes(document, filepath="document",model = "deepseek/deepseek-r1", format = "pdf", length = "1000")
```

---

## 📜 License
This project is licensed under the MIT License. You're free to use, modify, and distribute it with proper attribution.

## 🌐 Project Links

Documentation and additional resources coming soon!