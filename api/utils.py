import os
from secrets import token_hex
import inspect
from datetime import datetime

SECRETS_PATH = os.environ.get("SECRETS_PATH", "secrets")


def read_secrets():
    try:
        with open(SECRETS_PATH) as f:
            return {
                x.strip().split("=", 1)[0]: x.strip().split("=", 1)[1].strip("\"' \t")
                for x in f.readlines()
                if "=" in x
            }
    except Exception:
        return {}


SECRETS = {
    "SECRET_KEY": token_hex(32),
    **read_secrets(),
}

with open(SECRETS_PATH, "w") as f:
    f.writelines([f'{k}="{v}"' for k, v in SECRETS.items()])


def adapt_signature(wrapped, f):
    sig = inspect.signature(f)
    wrapped.__signature__ = inspect.Signature(
        parameters=list(sig.parameters.values())
        + [
            p
            for p in inspect.signature(wrapped).parameters.values()
            if p.kind
            not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ],
        return_annotation=sig.return_annotation,
    )
    return wrapped


def quantiles(numbers: list[float]):
    n = sorted(numbers)
    return {f"{q*10}%": n[len(n) * q // 10] for q in range(10)}


def hours_since(d: str | datetime | None = None) -> float:
    if not d:
        d = datetime(2000, 1, 1, 0, 0, 0)
    if isinstance(d, str):
        d = datetime.fromisoformat(d)
    return (datetime.now() - d).total_seconds() / 3600.0
