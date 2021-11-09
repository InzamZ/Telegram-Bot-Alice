from ruamel.yaml import YAML

conf_file = open("./Config/config.yml")
yaml = YAML(typ='safe')
conf = yaml.load(conf_file)
