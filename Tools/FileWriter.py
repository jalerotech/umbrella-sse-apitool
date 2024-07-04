import logging
import json

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def writeToFile(file_path, data):
    """
    Writes the list of users per org to the results.json file
    :param file_path: result.json file path
    :param data: org:{user data list}
    :return: None
    """
    logger = logging.getLogger("File Writer")
    try:
        file_name = file_path.split('/')[1]
    except IndexError as e:
        logger.info('File path is different, changing to "results.json"')
        file_name = file_path
    with open(file_path, 'a') as json_file:
        logger.info(f"{file_name} opened")
        logger.info(f'Writing child-org user list to {file_name} file')
        json.dump(data, json_file)
        json_file.write('\n')
