# Timestamper Python

Timestamper is a Python CLI tool that generates YouTube timestamps for a video based on a video ID.

![demo](demo.png)

## Pre-requisites

- Python 3.6 or higher
- Azure OpenAI API key

## Running the script

1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Set your environment variables in a `.env` file
    ```
    OPENAI_API_KEY=YOUR_API_KEY  
    ENDPOINT=YOUR_ENDPOINT
    DEPLOYMENT_NAME=YOUR_DEPLOYMENT_NAME
    ```
4. Run the script using `python timestamper.py {video_id}`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Future Improvements

- Improve grouping of captions