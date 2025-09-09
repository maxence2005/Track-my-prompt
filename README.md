# Track My Prompts

![app_screenshot](media/app_screenshot.png)


The Track My Prompts application allows the use of an image recognition AI model. It can detect everyday objects and interpret prompts for more targeted searches.

## Features

- Object detection in images and videos
- Live detection through the webcam
- Prompt interpretation for more targeted detection
- Voice prompt with different AI models

## Available Formats
YoloWorld AI model is used for object detection. The model is trained on the COCO dataset and can detect 80 different objects. The model is available in the following formats:
| Format | Extensions |
|---|---|
| Image | .bmp, .dng, .jpeg, .jpg, .mpo, .png, .tif, .tiff, .webp, .pfm, .HEIC |
| Video | .asf, .avi, .gif, .m4v, .mkv, .mov, .mp4, .mpeg, .mpg, .ts, .wmv, .webm |

## Prompt Interpretation
The application can interpret prompts to provide more targeted detection. The following prompts are available:
| Prompt | Description |
|---|---|
| Dumb | Search for a specific object by keyword in english |
| Dumb With Translation | Search for a specific object by keyword in any language |
| Mistral | Use the Mistral API to interpret the prompt |

## Voice Prompt

The application supports voice input with two modes of speech-to-text transcription, allowing users to issue commands or prompts by speaking.

| Mode | Description |
|---|---|
| Online (Google API) | Uses the Google Speech-to-Text API via the internet for accurate, real-time transcription. Requires internet access. |
| Offline (Whisper) | Uses OpenAI's Whisper model locally for private, offline transcription. No internet connection is needed. |

## Translations
The application is available in the following languages:
| Language | Download File |
|:---:|:---:|
| English | Preinstalled |
| French | [Download]()|

Install the language pack in settings.

## Create your own translation
### Get lrelease and lupdate commands
To create a translation, you need to install the Qt tools. You can get them on Debian-based Linux with the following command:
```bash
sudo apt-get install qttools5-dev-tools
```
### Create a translation file
Download the project and go to the 'scripts' folder. To generate template files, run the following command:
```bash
./extract_translations.sh <lang> # lang is the language code (ex: fr)
```
In the newly created 'translations' folder, you will find a .ts file. Open it with Qt Linguist and translate the strings.
You will also find a .json file with the items of the encyclopedia to translate.
Once the translation is complete, save the file and run the following command to generate the translation file:
```bash
./compile_translations.sh <lang> <lang_name> # lang is the language code (ex: fr), lang_name is the language name (ex: French)
```
You will get a .tmpts file.

## Installation

To ensure Track My Prompts works correctly, you need a Python virtual environment of version 3.10, 3.11, or 3.12.
You can create a virtual environment using the following command:

```bash
python3 -m venv venv
```
Once the environment is created, install the dependencies listed in the 'requirements.txt' file.
You can install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

(Optional) Depending on your computer's hardware, you can choose with or without GPU acceleration. If you have an Nvidia RTX graphics card, you can install torch with CUDA support. This will speed up the processing of images and videos. If you have AMD and Linux, you can install ROCm support for PyTorch. If you don't have a GPU compatible with CUDA or ROCm, you can install the CPU version of torch and save space.
You can find more information on the [PyTorch website](https://pytorch.org/get-started/locally/).

## Start Application
After installation, to launch the application, use the command
```
venv/bin/python -m qtquickdetect
```

## Easy Installation (Graphical)

If you prefer a simple installation method without using the terminal:

### Option 1: Website

You can download the pre-built graphical application from our website:

🔗 [Download from Website](https://trackmyprompt.louishamon.fr/)

*Just download and run the application. No Python or terminal needed.*

### Option 2: GitLab Releases

Go to the **Releases** section of the GitLab repository to download the latest executable version:

🔗 [Download from GitLab Releases](https://forgens.univ-ubs.fr/gitlab/e2300056/track-my-prompt/-/releases)

*Choose the version that matches your operating system: Windows or Linux.*


## Use Mistral API (FREE)
To understand prompts, you can use the Mistral API. To do this, you need to create an account on the [Mistral](https://www.mistral.ai/) website. Once the account is created, you can obtain an API key to use the text recognition service.\
If you don't have a Mistral key, follow this guide to generate one for free: [Generate Mistral API Key](https://www.pickaxeproject.com/post/how-to-get-a-mistral-api-key-2025)\
To use the Mistral API in the app, go to settings, in "Change the prompt interpreter" select "Mistral" and enter the API key.

## Authors
[Authors](AUTHORS.md)