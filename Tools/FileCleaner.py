import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def cleanFile(file_path):
    """
    Cleans up the results.json file.
    :param file_path:
    :return: None
    """
    logger = logging.getLogger("File cleaner")
    try:
        file_name = file_path.split('/')[1]
    except IndexError as e:
        logger.info('File path is different, changing to "results.json"')
        file_name = file_path
    with open(file_path, 'w') as json_file:
        logger.info(f"{file_name} opened")
        logger.info(f'Cleaning up {file_name} file')
        json_file.close()
        logger.info(f'{file_name} file cleaned \n ')
        