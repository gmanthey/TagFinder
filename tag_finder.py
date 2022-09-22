from argparse import ArgumentParser
from importlib import import_module
import logging
import yaml

from tagfinder.output import Output
from tagfinder.tag_detection import TagDetector

logger = logging.getLogger("tag_finder")
logger.setLevel(logging.INFO)

def transform_config(config):
    new_config = {}
    for key, value in config.items():
        key = key.replace('-', '_')
        if isinstance(value, dict):
            value = transform_config(value)
        new_config[key] = value
        
    return new_config

def main(config_file : str):
    with open(config_file, 'r') as cfg_file:
        try:
            config = yaml.safe_load(cfg_file)
        except yaml.YAMLError as exc:
            logger.error(f'could not read yaml file {config_file}: {exc}')
            
    config = transform_config(config)
    
    outputs : "list[Output]" = []
    
    logger.setLevel(config['logging']['log_level'].upper())
    if 'file_name' in config['logging'] and config['logging']['file_name']:
        logger.addHandler(logging.FileHandler(config['logging']['file_name']))
    else:
        logger.addHandler(logging.StreamHandler())    
    
    if 'output' not in config:
        config['output'] = []

    for out_yml in config['output']:
        t = out_yml['type'].replace('-', '_')
        class_name = ''.join([x.title() for x in t.split('_')])
        driver = getattr(import_module('tagfinder.output.' + t), class_name)
        if not issubclass(driver, Output):
            logger.fatal(f"{t} is not a valid output type")
            return
        outputs.append(driver(**out_yml))

    if not outputs:
        logger.warning('No output was configured, maybe you have a typo in the config?')

    tag_finder = TagDetector(**config['tag_detection'])

    try:
        tag_finder.run(outputs, data_file=args.data_file)
    finally:
        for output in outputs:
            output.close()
    


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--config', default='config.yml')
    parser.add_argument('--data_file', default=None)

    args = parser.parse_args()

    main(args.config)