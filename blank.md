# Usage

This Python script helps to generate a censored video with masked audio and subtitles from a given uncensored audio and video file.

## Arguments

The script accepts five command-line arguments:

1. `--audio_link`: The path to the uncensored audio file. (required)
2. `--vid_link`: The path to the source video file. (required)
3. `--swear_word_list`: The path to a text file that contains a list of swear words to be censored. Each swear word should be on a new line in the file. If not provided, a predefined list of common swear words will be used. (optional)
4. `--video_output`: The path to save the generated censored video. (required)
5. `--srtFilename`: The path to save the generated subtitle (srt) file. If not provided, no subtitle file will be saved. (optional)

## Running the Script

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

## Exception Handling

The script will stop execution and print an error message if there's an issue, such as a file not being found at the specified path.

