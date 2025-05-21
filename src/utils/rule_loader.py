import yaml
from src.utils.models import InlineRule


def load_inline_rules(yaml_path: str) -> list[InlineRule]:
    with open(yaml_path, "r") as f:
        raw = yaml.safe_load(f)

    rule_dicts = raw.get("inline_rules", [])
    return [InlineRule.from_dict(r) for r in rule_dicts]
