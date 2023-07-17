# Semi-Automated-Youtube-Channel

---

## Goal

A tool to semi-automate various tasks related to managing a YouTube channel, allowing content creators to streamline their workflow and improve productivity.

## Features

- utilizes Reddit's API to descover bodies of text
- uses a text-to-speech api to play over a video
- add audio overlay to a video file
- add subtitles to video file based on the speech in the video (using whisperx)
- Has the ablity to make simple youtube thumbnails based on popular youtube reddit channels
- A user is able to upload videos via YouTube Data API

## Installation

Follow these steps to set up the project locally:

### Windows

1. Clone the repository: `git clone https://github.com/isayahc/Semi-Automated-Youtube-Channel.git`
2. create a virtual environemnt:
   1. `python -m venv venv`
   2. `activate`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Configure the API keys and authentication credentials in the example.env file

### Linux / OSX

1. Clone the repository: `git clone https://github.com/isayahc/Semi-Automated-Youtube-Channel.git`
2. create a virtual environemnt:
   1. `python3 -m venv venv`
   2. `source venv/bin/activate`
3. Install the required dependencies: `pip3 install -r requirements.txt`
4. Configure the API keys and authentication credentials in the example.env file

## API Keys

```python
# Configuration for storing assets
STRING_AUDIO_FILE_LOCATION=assets/audio/posts
SWEAR_WORD_LIST_FILE_LOCATION_FILE_LOCATION=assets/text/swear_words.csv

# API Keys
# Needed for working with google
GOOGLE_API_KEY=

# Needed for text-to-speech
ELEVENLABS_API_KEY=

# Optional if you want to use reddit
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=

# Optional and will probably be removed soon
PLAYHT_API_KEY=
PLAYHT_API_USER_ID=

PROJECT_CX=


```

### Configure Reddit

- [login here](https://www.reddit.com/prefs/apps) tomake a new app

This is a sample of what to input
![ Image](https://github.com/isayahc/Semi-Automated-Youtube-Channel/blob/main/readme_assets/reddit_api_example.PNG?raw=true)

### Configure ElevenLabs

- [Follow this link](https://docs.elevenlabs.io/api-reference/quick-start/authentication)

### Configure Youtube Data v3

- [Follow this link](https://developers.google.com/youtube/v3/getting-started)

### Getting client_secret.json

- [Instructions here](https://developers.google.com/youtube/v3/docs/videos/insert)

## System Requirements

### Python Version

This software was written in Python 3.9.7. There is a possiblity there will be errors if an earlier version is used to compile.

## Usage

This Python script helps to generate a censored video with masked audio and subtitles from a given uncensored audio and video file.

### Arguments

The script accepts five command-line arguments:

1. `--audio_link`: The path to the uncensored audio file. (required)
2. `--vid_link`: The path to the source video file. (required)
3. `--swear_word_list`: The path to a text file that contains a list of swear words to be censored. Each swear word should be on a new line in the file. If not provided, a predefined list of common swear words will be used. (optional)
4. `--video_output`: The path to save the generated censored video. (required)
5. `--srtFilename`: The path to save the generated subtitle (srt) file. If not provided, no subtitle file will be saved. (optional)

### Running main.py

You can run the script from the command line like this:

```bash
python main.py --audio_link /path/to/audio/file --vid_link /path/to/video/file --video_output /path/to/output/file
```

This command will use the default list of swear words for censoring.

If you want to use your own list of swear words, add the `--swear_word_list` argument:

```bash
python main.py --audio_link /path/to/audio/file --vid_link /path/to/video/file --swear_word_list /path/to/swear_word_list.txt --video_output /path/to/output/file
```

To save a subtitle file, add the `--srtFilename` argument:

```bash
python main.py --audio_link /path/to/audio/file --vid_link /path/to/video/file --swear_word_list /path/to/swear_word_list.txt --video_output /path/to/output/file --srtFilename /path/to/subtitle/file
```

---

## Using the YouTube Video Upload Python Script

This `video_upload.py` script provides a command-line interface (CLI) tool to upload videos to YouTube using the YouTube Data API. The script handles authentication, video upload, and retry logic for failed uploads. Here are instructions on how to use it.

### Pre-requisites

Before you use this script, ensure that you have the following:

1. **OAuth 2.0 client ID and client secret:** You need to specify a `client_secret.json` file with your OAuth 2.0 client ID and client secret. You can get these from the Google Cloud Console. Ensure that you have enabled the YouTube Data API for your project. More Information in the [Documentation](https://developers.google.com/youtube/v3/docs/videos/insert)

### Running video_upload.py

The script uses command line arguments to specify the details of the video to be uploaded. Here is the usage of the script:

```shell
python video_upload.py --file FILE_PATH --title TITLE --description DESCRIPTION --category CATEGORY_ID --keywords "keyword1,keyword2" --privacyStatus PRIVACY_STATUS --thumbnail THUMBNAIL_PATH --madeForKids BOOLEAN_VALUE --youtubeShort BOOLEAN_VALUE
```

Replace the capitalized words with your own details:

- `FILE_PATH`: This is the full path to the video file to upload.
- `TITLE`: The title of the video.
- `DESCRIPTION`: The description of the video.
- `CATEGORY_ID`: The numeric category ID of the video. See [here](https://developers.google.com/youtube/v3/docs/videoCategories/list) for a list of category IDs.
- `keyword1,keyword2`: The keywords for the video, separated by commas.
- `PRIVACY_STATUS`: The privacy status of the video. Choose from 'public', 'private', or 'unlisted'.
- `THUMBNAIL_PATH`: The full path to the thumbnail image file.
- `BOOLEAN_VALUE` for `--madeForKids`: Specify if the video is made for kids. Use True or False.
- `BOOLEAN_VALUE` for `--youtubeShort`: Specify if the video is a YouTube short. Use True or False.

For example:

```shell
python video_upload.py --file /path/to/video.mp4 --title "Test Video" --description "This is a test video" --category 27 --keywords "test,video" --privacyStatus private --thumbnail /path/to/thumbnail.jpg --madeForKids False --youtubeShort False
```

This command uploads the video located at `/path/to/video.mp4` with the title "Test Video", description "This is a test video", category 27, keywords "test" and "video", privacy status set to 'private', thumbnail image from `/path/to/thumbnail.jpg`, and specifies that the video is not made for kids and is not a YouTube short.

Please note that the script will prompt you to authorize the request in your web browser when you run it for the first time. It is a one-time process, and the script will store the authorization credentials for future runs.

### Exception Handling

The script will stop execution and print an error message if there's an issue, such as a file not being found at the specified path.

## Testing

to run test input the command

```bash
python -m pytest
```

## Add later

- the ability to generate metadata that optimize how a video gets found based o the script of the video

## Contributing

Contributions are welcome! If you want to contribute to the project, follow these steps:

1. Fork the repository and clone it locally.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m "Add your commit message"`
4. Push the changes to your forked repository: `git push origin feature/your-feature-name`
5. Open a pull request, describing the changes you made and their purpose.

## License

This project is licensed under the [Apache License](http://www.apache.org/licenses/).

## Contact

For any questions, feedback, or inquiries, feel free to contact the project maintainer at [isayahculbertson@gmail.com](mailto:isayahculbertson@gmail.com).