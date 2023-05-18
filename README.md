# Semi-Automated-Youtube-Channel

## Goal

A tool to semi-automate various tasks related to managing a YouTube channel, allowing content creators to streamline their workflow and improve productivity.

## Features

- utilizes Reddit's API to descover bodies of text
- uses a text-to-speech api to play over a video
- add audio overlay to a video file
- add subtitles to video file based on the speech in the video (using whisperx)
- Has the ablity to make simple youtube thumbnails based on popular youtube reddit channels

## Installation

Follow these steps to set up the project locally:

1. Clone the repository: `git clone https://github.com/isayahc/Semi-Automated-Youtube-Channel.git`
2. create a virtual environemnt:
   1. `python -m venv venv`
   2. `activate`
3. Install the required dependencies: `pip3 install -r requirements.txt` for linux `pip install -r requirements.txt` for windows
4. Configure the API keys and authentication credentials in the example.env file

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

### Running the Script

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

### Exception Handling

The script will stop execution and print an error message if there's an issue, such as a file not being found at the specified path.

## Testing

to run test input the command
```
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